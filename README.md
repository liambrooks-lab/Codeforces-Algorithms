<div align="center">

# Codeforces Algorithms

**A structured archive of competitive programming solutions for Codeforces.**

[![Go Version](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat&logo=go)](https://golang.org/)
[![C++ Version](https://img.shields.io/badge/C%2B%2B-17%2F20-00599C?style=flat&logo=c%2B%2B)](https://isocpp.org/)
[![Platform](https://img.shields.io/badge/Platform-Codeforces-1F8ACB?style=flat&logo=codeforces)](https://codeforces.com/)

</div>

---

## Overview

This repository serves as a centralized, version-controlled workspace for Codeforces problem-solving. Solutions are strictly categorized by difficulty rating and contest structure. The infrastructure is optimized for performance, utilizing Go and C++ with custom fast I/O templates, and is backed by a custom CI/CD automation pipeline.

## Repository Structure

The directory architecture is designed for scalability and automated testing:

```text
Codeforces-Algorithms/
├── Practice_<Rating>/  # Rating-specific directories (e.g., Practice_800, Practice_1500)
├── Virtual_Contests/   # Solutions from simulated contest environments
├── Templates/          # Standardized fast I/O boilerplate for Go and C++
├── scripts/            # CI/CD automation, testing, benchmarking, and indexing
├── benchmarks/         # Automated performance benchmarks (results.json)
└── index/              # Problem index and difficulty catalog (index.json)
```

## CI/CD & Automation Infrastructure

The repository integrates a continuous integration and deployment pipeline powered by GitHub Actions, designed with strict security boundaries.

* **Automated Standard I/O Testing:** On every `push` and `pull_request`, the DevOps suite automatically compiles and tests all C++ and Go solutions against their respective local `input.txt` and `expected.txt` environments. Failures prevent the pipeline from passing.
* **Security-Restricted Auto-Commits:** For direct pushes to the `main` branch, the `github-actions[bot]` automatically executes benchmarking and indexing scripts, committing updated `results.json` and `index.json` files back to the repository. Write-access is strictly blocked for external pull requests to prevent unauthorized code execution.

## Local Execution Environment

The codebase utilizes a conditional I/O setup. Solutions automatically detect the local execution environment to seamlessly switch between local text files and standard I/O streams required by the Codeforces servers.

### Prerequisites
-   **Go:** `1.22` or higher
-   **C++:** GCC / G++ (`g++` supporting C++17 / C++20)
-   **Python:** `3.12` or higher (reserved strictly for DevOps automation and tooling scripts)

### Running Locally

1. Ensure `input.txt` and `output.txt` exist in the respective problem directory.
2. Paste the test cases into `input.txt`.
3. Execute the solution:

**For Go:**
```bash
go run solution.go
```

**For C++:**
```bash
g++ -O3 solution.cpp -o solution && ./solution
```
Outputs are routed directly to `output.txt`.

### Automation Commands

```bash
make test        # Run the Standard I/O test suite across solutions
make benchmark   # Measure multi-iteration runtime latency into benchmarks/results.json
make index       # Catalog all solved problems into index/index.json
make clean       # Remove stray binaries, temp executables, and cache
```

---
<br>
<div align="right">
  <b>Rudranarayan Jena</b><br>
  <i>Founder @ Voxion Labs</i>
</div>

---
<div align="center">
  (c) 2026 Rudranarayan Jena
</div>
<p align="center">
  Codeforces · Algorithms · C++ · Go
</p>