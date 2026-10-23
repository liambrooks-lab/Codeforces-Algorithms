# Contributing Guidelines

This document outlines the strict operational standards for managing the `Codeforces-Algorithms` repository. 

## 1. Language Standards

* Only **Go (1.22+)** and **Python (3.12+)** are authorized.
* C++ legacy code is deprecated and will not be maintained.

## 2. Code Structure & Templates

* All submissions must utilize the standardized fast I/O boilerplate located in the `Templates/` directory.
* Do not hardcode file paths or use standard `input()` / `fmt.Scan` without the buffer templates. The code must fall back to standard I/O seamlessly on the Codeforces servers.
* Ensure variables handling large sums use 64-bit integers (`int64` in Go) to prevent overflow errors.

## 3. Version Control Restrictions

* **NEVER** commit compiled binaries (`*.exe`, `*.out`, binary executables).
* **NEVER** commit local test files (`input.txt`, `output.txt`).
* Ensure the local `.gitignore` rules are active before staging.

## 4. Naming Conventions

* Problem files must follow the format: `<ProblemID>_<ShortName>.<ext>`
  * *Example:* `2269B_KiaKio.go`
* Files must be placed in their exact rating directory (e.g., `Practice_800/`, `Practice_1200/`).

## 5. Commit Guidelines

Use semantic commit messages to maintain a clean history.

* `feat:` for adding a new problem solution (e.g., `feat: add solution for 2269B`).
* `refactor:` for optimizing an existing solution.
* `chore:` for updating templates, structures, or configurations.