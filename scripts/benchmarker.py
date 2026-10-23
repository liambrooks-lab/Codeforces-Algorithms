#!/usr/bin/env python3
"""
scripts/benchmarker.py - High-Precision Competitive Programming Benchmarking Engine
Measures standard I/O execution latency across iterations and writes results to benchmarks/results.json.
"""

import argparse
import datetime
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

# Ensure scripts directory is on path for modular imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tester import SolutionTest, find_solutions, normalize_output

# Terminal styling constants
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_GREEN = "\033[92m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_MAGENTA = "\033[95m"


def benchmark_solution(solution: SolutionTest, runs: int = 5, timeout: float = 10.0) -> Dict[str, Any]:
    """Runs a single solution multiple times and returns execution latency stats in ms."""
    if not solution.has_test_fixtures():
        return {
            "file": str(solution.rel_path).replace("\\", "/"),
            "language": solution.language,
            "status": "SKIPPED",
            "reason": "Missing test fixtures (input.txt or expected.txt)",
        }

    with open(solution.input_file, "r", encoding="utf-8", errors="replace") as f:
        input_data = f.read()

    with open(solution.expected_file, "r", encoding="utf-8", errors="replace") as f:
        expected_data = f.read()

    # Initial verification run
    norm_expected = normalize_output(expected_data)
    cmd = solution.get_command()

    try:
        proc = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout,
            cwd=str(solution.repo_root),
        )
        if proc.returncode != 0 or normalize_output(proc.stdout) != norm_expected:
            # Check fallback to output.txt if stdout was empty
            actual = normalize_output(proc.stdout)
            if not actual:
                local_out = solution.dir_path / "output.txt"
                if local_out.is_file():
                    with open(local_out, "r", encoding="utf-8", errors="replace") as f:
                        actual = normalize_output(f.read())

            if actual != norm_expected:
                return {
                    "file": str(solution.rel_path).replace("\\", "/"),
                    "language": solution.language,
                    "status": "FAILED",
                    "reason": "Failed correctness verification prior to benchmarking",
                }
    except Exception as e:
        return {
            "file": str(solution.rel_path).replace("\\", "/"),
            "language": solution.language,
            "status": "ERROR",
            "reason": str(e),
        }

    durations: List[float] = []

    for _ in range(runs):
        start = time.perf_counter()
        try:
            subprocess.run(
                cmd,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=str(solution.repo_root),
            )
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            durations.append(elapsed_ms)
        except Exception as e:
            return {
                "file": str(solution.rel_path).replace("\\", "/"),
                "language": solution.language,
                "status": "ERROR",
                "reason": f"Run failed: {e}",
            }

    avg_ms = statistics.mean(durations)
    median_ms = statistics.median(durations)
    min_ms = min(durations)
    max_ms = max(durations)
    stdev_ms = statistics.stdev(durations) if len(durations) > 1 else 0.0

    return {
        "file": str(solution.rel_path).replace("\\", "/"),
        "language": solution.language,
        "status": "PASSED",
        "runs": runs,
        "avg_ms": round(avg_ms, 2),
        "median_ms": round(median_ms, 2),
        "min_ms": round(min_ms, 2),
        "max_ms": round(max_ms, 2),
        "stdev_ms": round(stdev_ms, 2),
        "durations_ms": [round(d, 2) for d in durations],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Codeforces Performance Benchmarking Engine")
    parser.add_argument("--runs", type=int, default=5, help="Number of benchmark iterations (default: 5)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-run timeout in seconds (default: 10.0)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    benchmarks_dir = repo_root / "benchmarks"
    results_file = benchmarks_dir / "results.json"

    # Ensure benchmarks directory exists
    benchmarks_dir.mkdir(parents=True, exist_ok=True)

    # Initialize a dummy/starter file if it does not exist
    if not results_file.exists():
        dummy_data = {
            "benchmark_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "runs_per_solution": args.runs,
            "results": [],
            "notes": "Initial benchmark placeholder file.",
        }
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=2)

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}  Codeforces Solution Benchmarker                   {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"Iterations per solution: {COLOR_BOLD}{args.runs}{COLOR_RESET}\n")

    solutions = find_solutions(repo_root)
    results: List[Dict[str, Any]] = []

    print(f"{'Solution':<40} {'Lang':<8} {'Status':<10} {'Avg (ms)':<10} {'Min (ms)':<10} {'Max (ms)':<10}")
    print("-" * 92)

    for sol in solutions:
        res = benchmark_solution(sol, runs=args.runs, timeout=args.timeout)
        results.append(res)

        status_str = res["status"]
        if status_str == "PASSED":
            color = COLOR_GREEN
            avg_str = f"{res['avg_ms']:.2f}"
            min_str = f"{res['min_ms']:.2f}"
            max_str = f"{res['max_ms']:.2f}"
        elif status_str == "SKIPPED":
            color = COLOR_YELLOW
            avg_str = min_str = max_str = "N/A"
        else:
            color = COLOR_RED
            avg_str = min_str = max_str = "ERR"

        file_display = res["file"]
        if len(file_display) > 38:
            file_display = "..." + file_display[-35:]

        print(
            f"{file_display:<40} "
            f"{res['language']:<8} "
            f"{color}{status_str:<10}{COLOR_RESET} "
            f"{avg_str:<10} "
            f"{min_str:<10} "
            f"{max_str:<10}"
        )

    # Structured payload
    payload = {
        "benchmark_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runs_per_solution": args.runs,
        "total_solutions": len(solutions),
        "results": results,
    }

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("-" * 92)
    print(f"\n{COLOR_BOLD}{COLOR_GREEN}Benchmark results saved to:{COLOR_RESET} {results_file}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
