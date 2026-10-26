# Contributing Guidelines

This document outlines the strict operational standards for managing the `Codeforces-Algorithms` repository. 

## 1. Language Standards

* Only **Go (1.22+)** and **C++ (C++17/20)** are authorized for problem solutions.
* Python is reserved strictly for DevOps automation and tooling scripts in `scripts/`.

## 2. Code Structure & Templates

* All submissions must utilize the standardized fast I/O boilerplate located in the `Templates/` directory (`template.go` and `template.cpp`).
* Do not hardcode file paths or use unbuffered I/O without the boilerplate templates. The code must fall back to standard I/O seamlessly on Codeforces servers.
* Ensure variables handling large sums use 64-bit integers (`int64` in Go, `long long` in C++) to prevent overflow errors.

## 3. Version Control Restrictions

* **NEVER** commit compiled binaries (`*.exe`, `*.out`, `temp_bin`, `temp_bin.exe`).
* **NEVER** commit scratch run files (`output.txt`).
* Ensure `.gitignore` rules are active before staging.

## 4. Naming Conventions

* Problem files must follow the format: `<ProblemID>_<ShortName>.<ext>`
  * *Example:* `2269B_KiaKio.go` or `2269B_KiaKio.cpp`
* Files must be placed in their exact rating directory (e.g., `problem_set_800/`, `problem_set_1200/`).

## 5. Commit Guidelines

Use semantic commit messages to maintain a clean history.

* `feat:` for adding a new problem solution (e.g., `feat: add solution for 2269B`).
* `refactor:` for optimizing an existing solution.
* `chore:` for updating templates, structures, or configurations.
