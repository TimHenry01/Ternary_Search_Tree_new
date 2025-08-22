import time
import random
import string
import sys
import os
import gc
import tracemalloc
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib

matplotlib.use("Agg")   # non-GUI backend for HPC
import matplotlib.pyplot as plt

# Add the parent directory to the path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ternary_search_tree import TernarySearchTree

# Comprehensive benchmarking suite for Ternary Search Tree.
class TSTBenchmark:
    
    def __init__(self):
        self.results = defaultdict(dict)
        
    # Load words from a specified file path.
    def load_words_from_file(self, file_path, num_words=None):
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        if num_words and num_words < len(words):
            return words[:num_words]
        return words
    
    # Generate random words for testing.
    def generate_random_words(self, count, min_length=3, max_length=10):
        words = []
        for _ in range(count):
            length = random.randint(min_length, max_length)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        return list(set(words))  # Remove duplicates
    
    # Generate sequential words (worst case for some operations).
    def generate_sequential_words(self, count):
        return [f"word{i:06d}" for i in range(count)]
    
    # Generate words with similar prefixes (specific case analysis).
    def generate_similar_words(self, count, base="test"):
        words = [base]
        for i in range(1, count):
            suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 5)))
            words.append(f"{base}{suffix}")
        return words
    
    # Benchmark insert operation performance scaling.
    def benchmark_insert_performance(self, words, benchmark_name="insert"):
        print(f"Benchmarking {benchmark_name.capitalize()} performance...")

        word_counts_to_test = [1000, 5000, 10000, 20000, 40000]
        
        insert_times = []
        memory_usage = []
        word_counts = []
        
        for count in word_counts_to_test:
            if count > len(words):
                break
            subset_words = words[:count]
            tst = TernarySearchTree()

            tracemalloc.start()
            gc.collect()
            
            start_time = time.perf_counter()
            for word in subset_words:
                tst.insert(word)
            end_time = time.perf_counter()
            
            total_time = end_time - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            peak_memory = peak / 1024 / 1024  # Convert to MB
            
            insert_times.append(total_time)
            memory_usage.append(peak_memory)
            word_counts.append(count)
            
            print(f"  Testing with {count} words. Time: {total_time:.4f}s, Memory: {peak_memory:.2f}MB")
        
        self.results[benchmark_name] = {
            'counts': word_counts,
            'times': insert_times,
            'memory': memory_usage
        }
        
    # Benchmark search operation performance scaling.
    def benchmark_search_performance(self, words, benchmark_name="search"):
        print(f"Benchmarking {benchmark_name.capitalize()} performance...")

        word_counts_to_test = [1000, 5000, 10000, 20000, 40000]
        
        search_times = []
        word_counts = []

        for count in word_counts_to_test:
            if count > len(words):
                break
            
            subset_words = words[:count]
            tst = TernarySearchTree()
            for word in subset_words:
                tst.insert(word)

            start_time = time.perf_counter()
            for word in subset_words:
                tst.search(word)
            end_time = time.perf_counter()

            total_time = end_time - start_time
            
            search_times.append(total_time)
            word_counts.append(count)
            
            print(f"  Testing with {count} searches. Time: {total_time:.4f}s")
            
        self.results[benchmark_name] = {
            'counts': word_counts,
            'times': search_times,
        }
    
    # Test best-case scenarios for TST operations.
    def benchmark_best_case_scenarios(self):
        print("Benchmarking best-case scenarios...")
        
        # A small, well-distributed set of random words
        words = self.generate_random_words(100)
        tst = TernarySearchTree()

        # Measure insertion time for a well-balanced tree
        start_time = time.perf_counter()
        for word in words:
            tst.insert(word)
        insert_time = time.perf_counter() - start_time
        
        # Measure search time for existing words
        start_time = time.perf_counter()
        for word in words:
            tst.search(word)
        search_time = time.perf_counter() - start_time
        
        # Store results
        self.results['best_case'] = {
            'insert_time': insert_time,
            'search_time': search_time
        }
        
        print(f"    Insert time: {insert_time:.4f}s")
        print(f"    Search time: {search_time:.4f}s")

    # Test worst-case scenarios for TST operations.
    def benchmark_worst_case_scenarios(self):
        print("Benchmarking worst-case scenarios...")
        
        scenarios = {
            'sequential_worst_case': self.generate_sequential_words(1000),
            'similar_prefixes_worst_case': self.generate_similar_words(1000, "commonprefix"),
        }
        
        for scenario_name, words in scenarios.items():
            print(f"  Testing {scenario_name.replace('_', ' ').title()} scenario...")
            
            tst = TernarySearchTree()
            
            # Measure insertion time
            start_time = time.perf_counter()
            for word in words:
                tst.insert(word)
            insert_time = time.perf_counter() - start_time
            
            # Measure search time
            start_time = time.perf_counter()
            for word in words:
                tst.search(word)
            search_time = time.perf_counter() - start_time
            
            # Store results
            self.results['worst_case'][scenario_name] = {
                'insert_time': insert_time,
                'search_time': search_time
            }
            
            print(f"    Insert: {insert_time:.4f}s, Search: {search_time:.4f}s")
    
    # Compare TST performance with Python's built-in data structures.
    def compare_with_builtin_structures(self, word_count):
        print(f"Comparing with built-in structures ({word_count} words)...")
        
        words = self.generate_random_words(word_count)
        
        # Test TST
        tst = TernarySearchTree()
        start_time = time.perf_counter()
        for word in words:
            tst.insert(word)
        tst_insert_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for word in words:
            tst.search(word)
        tst_search_time = time.perf_counter() - start_time
        
        # Test Python set
        python_set = set()
        start_time = time.perf_counter()
        for word in words:
            python_set.add(word)
        set_insert_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for word in words:
            word in python_set
        set_search_time = time.perf_counter() - start_time
        
        # Test Python list (worst case)
        python_list = []
        start_time = time.perf_counter()
        for word in words:
            if word not in python_list:
                python_list.append(word)
        list_insert_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for word in python_list:
            word in python_list
        list_search_time = time.perf_counter() - start_time
        
        # Store comparison results
        self.results['comparison'] = {
            'tst_insert': tst_insert_time,
            'tst_search': tst_search_time,
            'set_insert': set_insert_time,
            'set_search': set_search_time,
            'list_insert': list_insert_time,
            'list_search': list_search_time
        }
        
        print(f"  TST    - Insert: {tst_insert_time:.4f}s, Search: {tst_search_time:.4f}s")
        print(f"  Set    - Insert: {set_insert_time:.4f}s, Search: {set_search_time:.4f}s")
        print(f"  List   - Insert: {list_insert_time:.4f}s, Search: {list_search_time:.4f}s")
    
    def create_performance_plots(self):
        print("Creating performance plots...")
        
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot Insert Performance
        if 'insert' in self.results and self.results['insert']:
            counts = self.results['insert']['counts']
            times = self.results['insert']['times']
            axs[0, 0].plot(counts, times, 'bo-', label='Insert Time')
            axs[0, 0].set_title('Insert Performance Scaling')
            axs[0, 0].set_xlabel('Number of Words')
            axs[0, 0].set_ylabel('Time (seconds)')
            axs[0, 0].grid(True)
            axs[0, 0].legend()
        
        # Plot Search Performance
        if 'search' in self.results and self.results['search']:
            counts = self.results['search']['counts']
            times = self.results['search']['times']
            axs[0, 1].plot(counts, times, 'ro-', label='Search Time')
            axs[0, 1].set_title('Search Performance Scaling')
            axs[0, 1].set_xlabel('Number of Words')
            axs[0, 1].set_ylabel('Time (seconds)')
            axs[0, 1].grid(True)
            axs[0, 1].legend()

        # Plot Memory Usage
        if 'insert' in self.results and self.results['insert']:
            counts = self.results['insert']['counts']
            memory = self.results['insert']['memory']
            axs[1, 0].plot(counts, memory, 'go-', label='Memory Usage')
            axs[1, 0].set_title('Memory Usage Scaling')
            axs[1, 0].set_xlabel('Number of Words')
            axs[1, 0].set_ylabel('Memory (MB)')
            axs[1, 0].grid(True)
            axs[1, 0].legend()
        
        # Plot Comparison with Built-in Structures
        if 'comparison' in self.results:
            comp = self.results['comparison']
            structures = ['TST', 'Set', 'List']
            insert_times = [comp['tst_insert'], comp['set_insert'], comp['list_insert']]
            search_times = [comp['tst_search'], comp['set_search'], comp['list_search']]
            
            x = np.arange(len(structures))
            width = 0.35
            
            axs[1, 1].bar(x - width/2, insert_times, width, label='Insert', alpha=0.8)
            axs[1, 1].bar(x + width/2, search_times, width, label='Search', alpha=0.8)
            axs[1, 1].set_ylabel('Time (seconds)')
            axs[1, 1].set_title('Performance Comparison')
            axs[1, 1].set_xticks(x)
            axs[1, 1].set_xticklabels(structures)
            axs[1, 1].legend()
            axs[1, 1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('tst_performance_analysis.png', dpi=300, bbox_inches='tight')
        print("  Saved performance plots to 'tst_performance_analysis.png'")
    
    # Generate a comprehensive performance report.
    def generate_report(self):
        print("\nGenerating performance report...")
        
        report = []
        report.append("=" * 60)
        report.append("TERNARY SEARCH TREE PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Insert performance analysis
        if 'insert' in self.results and self.results['insert']:
            report.append("INSERT PERFORMANCE:")
            report.append("-" * 20)
            for i, (count, time_taken) in enumerate(zip(self.results['insert']['counts'], self.results['insert']['times'])):
                 report.append(f"  Total time for {count} words: {time_taken:.4f}s")
            
            if 'memory' in self.results['insert']:
                report.append(f"  Peak memory usage (for {self.results['insert']['counts'][-1]} words): {self.results['insert']['memory'][-1]:.2f}MB")
            report.append("")
        
        # Search performance analysis
        if 'search' in self.results and self.results['search']:
            report.append("SEARCH PERFORMANCE:")
            report.append("-" * 19)
            for count, time_taken in zip(self.results['search']['counts'], self.results['search']['times']):
                report.append(f"  Total time for {count} searches: {time_taken:.4f}s")
            report.append("")
        
        # Best case scenarios
        if 'best_case' in self.results and self.results['best_case']:
            report.append("BEST CASE SCENARIOS:")
            report.append("-" * 20)
            data = self.results['best_case']
            report.append(f"  Insert time (small, random sample): {data['insert_time']:.4f}s")
            report.append(f"  Search time (small, random sample): {data['search_time']:.4f}s")
            report.append("")
        
        # Worst case scenarios
        if 'worst_case' in self.results and self.results['worst_case']:
            report.append("WORST CASE SCENARIOS:")
            report.append("-" * 21)
            for scenario_name, data in self.results['worst_case'].items():
                report.append(f"  {scenario_name.replace('_', ' ').title()}:")
                report.append(f"    Insert: {data['insert_time']:.4f}s")
                report.append(f"    Search: {data['search_time']:.4f}s")
            report.append("")
        
        # Comparison with built-in structures
        if 'comparison' in self.results:
            comp = self.results['comparison']
            report.append("COMPARISON WITH BUILT-IN STRUCTURES:")
            report.append("-" * 37)
            report.append(f"  TST    - Insert: {comp['tst_insert']:.4f}s, Search: {comp['tst_search']:.4f}s")
            report.append(f"  Set    - Insert: {comp['set_insert']:.4f}s, Search: {comp['set_search']:.4f}s")
            report.append(f"  List   - Insert: {comp['list_insert']:.4f}s, Search: {comp['list_search']:.4f}s")
            report.append("")
        
        # Save results to a JSON file for analysis script
        json_path = "benchmark_results.json"
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"  Saved raw results to '{json_path}'")
        
        # Save report to a text file
        report_path = "tst_performance_report.txt"
        with open(report_path, 'w') as f:
            f.write("\n".join(report))
        
        print(f"  Saved performance report to '{report_path}'")

def run_all_benchmarks(word_source='file'):
    """Main function to run all benchmark tests."""
    benchmark = TSTBenchmark()
    
    words_to_insert = []
    if word_source == 'file':
        words_to_insert = benchmark.load_words_from_file('corncob_lowercase.txt')
    else:
        # Fallback to random word generation
        words_to_insert = benchmark.generate_random_words(60000)

    # Run insert benchmark
    benchmark.benchmark_insert_performance(words_to_insert)
    
    # Run search benchmark
    benchmark.benchmark_search_performance(words_to_insert)
    
    # Run best case scenarios benchmark
    benchmark.benchmark_best_case_scenarios()
    
    # Run worst case scenarios benchmark
    benchmark.benchmark_worst_case_scenarios()
    
    # Compare with built-in structures
    # The comparison benchmark will run with the full dataset size
    benchmark.compare_with_builtin_structures(len(words_to_insert))
    
    # Create plots and generate textual report
    benchmark.create_performance_plots()
    benchmark.generate_report()

if __name__ == "__main__":
    run_all_benchmarks()