#!/bin/bash

# Job monitoring script for Ternary Search Tree benchmarks
# This script provides various utilities for monitoring SLURM jobs

# Color codes for better output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo "Ternary Search Tree Job Monitoring Script"
    echo "Usage: $0 [OPTION] [JOB_ID]"
    echo ""
    echo "Options:"
    echo "  -s, --status      Show current job status"
    echo "  -q, --queue       Show all jobs in queue"
    echo "  -c, --cancel      Cancel specific job"
    echo "  -w, --watch       Watch job status (updates every 30 seconds)"
    echo "  -l, --log         Show job log in real-time"
    echo "  -r, --report      Run analysis script for a finished job"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -s 12345       Show status of job 12345"
    echo "  $0 -q             Show all your jobs"
    echo "  $0 -r 12345       Run analysis on job 12345 output"
}

# Function to check job status
check_job_status() {
    local job_id=$1
    if [ -z "$job_id" ]; then
        echo -e "${YELLOW}Showing all your jobs:${NC}"
        squeue -u $USER
    else
        echo -e "${BLUE}Status for job $job_id:${NC}"
        squeue -j $job_id
        if [ $? -ne 0 ]; then
            echo -e "${RED}Job $job_id not found in queue. It may have completed or been cancelled.${NC}"
            if [ -f "tst_benchmark_${job_id}.out" ]; then
                echo -e "${GREEN}Found output file: tst_benchmark_${job_id}.out${NC}"
                echo "Use '$0 -r $job_id' to view the full report"
            fi
        fi
    fi
}

# Function to show job queue
show_queue() {
    echo -e "${YELLOW}Current job queue for user $USER:${NC}"
    echo ""
    squeue -u $USER
}

# Function to cancel job
cancel_job() {
    local job_id=$1
    if [ -z "$job_id" ]; then
        echo -e "${RED}Error: Job ID required for cancellation${NC}"
        echo "Usage: $0 -c JOB_ID"
        return 1
    fi
    
    echo -e "${YELLOW}Cancelling job $job_id...${NC}"
    scancel $job_id
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Job $job_id cancelled successfully${NC}"
    else
        echo -e "${RED}Failed to cancel job $job_id${NC}"
    fi
}

# Function to show real-time log
show_log() {
    local job_id=$1
    if [ -z "$job_id" ]; then
        echo -e "${RED}Error: Job ID required for log display${NC}"
        echo "Usage: $0 -l JOB_ID"
        return 1
    fi
    
    local output_file="tst_benchmark_${job_id}.out"
    if [ -f "$output_file" ]; then
        echo -e "${BLUE}Following log for job $job_id (Press Ctrl+C to stop):${NC}"
        echo "File: $output_file"
        echo "========================================"
        tail -f "$output_file"
    else
        echo -e "${RED}Log file not found: $output_file${NC}"
        echo "Job may not have started yet."
    fi
}

# Function to analyze results of a finished job
run_analysis() {
    local job_id=$1
    if [ -z "$job_id" ]; then
        echo -e "${RED}Error: Job ID required for report generation${NC}"
        echo "Usage: $0 -r JOB_ID"
        return 1
    fi
    
    local output_file="tst_benchmark_${job_id}.out"
    local json_file="benchmark_results.json"
    
    # Check if the output and JSON files exist
    if [ ! -f "$output_file" ] || [ ! -f "$json_file" ]; then
        echo -e "${RED}Error: Output file ($output_file) or JSON file ($json_file) not found.${NC}"
        echo "Please check if the job has completed and if the files are in the current directory."
        return 1
    fi
    
    echo -e "${BLUE}Running analysis for job $job_id...${NC}"
    ./"Results analysis script" -a
}

# Main script logic
case "$1" in
    -s|--status)
        check_job_status "$2"
        ;;
    -q|--queue)
        show_queue
        ;;
    -c|--cancel)
        cancel_job "$2"
        ;;
    -w|--watch)
        echo -e "${YELLOW}Watching jobs for user $USER (Press Ctrl+C to stop)${NC}"
        while true; do
            clear
            echo "=== Job Monitor - $(date) ==="
            show_queue
            echo ""
            echo -e "${BLUE}Press Ctrl+C to stop monitoring${NC}"
            sleep 30
        done
        ;;
    -l|--log)
        show_log "$2"
        ;;
    -r|--report)
        run_analysis "$2"
        ;;
    -h|--help|'')
        show_help
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
esac
