#!/bin/bash
#SBATCH --job-name=tst_benchmark
#SBATCH --output=tst_benchmark_%j.out
#SBATCH --error=tst_benchmark_%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8GB
#SBATCH --partition=batch

# This script runs the performance benchmarks for the Ternary Search Tree
# on the HPC cluster. It first runs correctness tests, then the main
# benchmark, and finally provides a summary of the results.

# ========================================
# TST BENCHMARK JOB STARTED
# ========================================
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "Start Time: $(date)"
echo ""
echo "Loading required modules..."

# Load required modules (adjust based on your HPC environment)
# Using 'module purge' is a good practice to ensure a clean environment.
module purge
module load cluster/genius/batch
module load Python/3.13.1-GCCcore-14.2.0

# Ensure the Python environment is set up correctly
export PYTHONPATH=$PYTHONPATH:$PWD

# Navigate to the job submission directory
cd $SLURM_SUBMIT_DIR || { echo "Failed to cd to SLURM_SUBMIT_DIR"; exit 1; }

echo "Installing required Python packages to local user directory..."
pip install --user matplotlib numpy

echo ""
echo "========================================"
echo "RUNNING TST CORRECTNESS TESTS"
echo "========================================"

# Run unit tests first to ensure correctness before running the main benchmark
python test_ternary_search_tree.py

# Check the exit status of the previous command
if [ $? -eq 0 ]; then
    echo "All tests passed! Proceeding with benchmarks..."
else
    echo "Tests failed! Stopping benchmark execution."
    exit 1
fi

echo ""
echo "========================================"
echo "RUNNING PERFORMANCE BENCHMARKS"
echo "========================================"

# Run the comprehensive benchmark suite
# The benchmark script will handle loading the large word list.
python benchmark_tst.py

echo ""
echo "========================================"
echo "BENCHMARK RESULTS SUMMARY"
echo "========================================"

# Display key result files
echo "Generated files:"
ls -la *.png *.txt *.json 2>/dev/null || echo "No output files found"

# Check if the report file exists and display a summary
if [ -f "tst_performance_report.txt" ]; then
    echo ""
    echo "Performance Report Summary (first 50 lines):"
    echo "---------------------------"
    head -50 tst_performance_report.txt
fi

echo ""
echo "========================================"
echo "TST BENCHMARK JOB COMPLETED"
echo "End Time: $(date)"
echo "========================================"