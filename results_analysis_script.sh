#!/bin/bash

# Results checking and analysis script for Ternary Search Tree benchmarks
# This script analyzes benchmark results and generates a summary report.

# Color codes for better output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to analyze job results from JSON file
analyze_job_results() {
    local json_file="benchmark_results.json"
    local output_file="tst_performance_report.txt"

    if [ ! -f "$json_file" ]; then
        echo -e "${RED}Error: JSON results file not found at: $json_file${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Analyzing results from $json_file...${NC}"
    
    # Use python to pretty-print the JSON and extract key metrics
    python3 -c "
import json
from pprint import pprint

with open('$json_file', 'r') as f:
    data = json.load(f)

print('\\n${GREEN}Performance Summary from JSON:${NC}')
print('------------------------------------')
if 'insert' in data:
    insert_data = data['insert']
    print(f'Total words inserted: {insert_data['counts'][-1]}')
    print(f'Total insert time:    {sum(insert_data['times']):.4f}s')
    print(f'Peak memory usage:    {insert_data['memory'][-1]:.2f}MB')

if 'search' in data:
    search_data = data['search']
    print(f'Total searches:       {search_data['counts'][-1]}')
    print(f'Total search time:    {sum(search_data['times']):.4f}s')

if 'worst_case' in data:
    print('\\n${BLUE}Worst-Case Scenarios:${NC}')
    for scenario, times in data['worst_case'].items():
        print(f'  {scenario.replace('_', ' ').title()}:')
        print(f'    Insert time: {times['insert_time']:.4f}s')
        print(f'    Search time: {times['search_time']:.4f}s')

if 'comparison' in data:
    print('\\n${BLUE}Comparison with Built-ins:${NC}')
    comparison_data = data['comparison']
    print(f'  TST:    Insert={comparison_data['tst_insert']:.4f}s, Search={comparison_data['tst_search']:.4f}s')
    print(f'  Set:    Insert={comparison_data['set_insert']:.4f}s, Search={comparison_data['set_search']:.4f}s')
    print(f'  List:   Insert={comparison_data['list_insert']:.4f}s, Search={comparison_data['list_search']:.4f}s')
"
    # Display generated report if it exists
    if [ -f "$output_file" ]; then
        echo ""
        echo -e "${BLUE}Generated Report (tst_performance_report.txt):${NC}"
        echo "----------------------------------------------------"
        cat "$output_file"
    fi
}

# Main script logic
case "$1" in
    -a|--analyze)
        analyze_job_results
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        echo "Usage: $0 [-a|--analyze]"
        exit 1
        ;;
esac
