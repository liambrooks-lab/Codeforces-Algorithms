#!/usr/bin/env python3
"""
scripts/tester.py - Production-Grade Competitive Programming Testing Engine
Validates Standard I/O solutions (Go and C++) against local test fixtures.
"""

import os
import sys
import difflib
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Enable ANSI escape sequences on Windows consoles
if os.name == "nt":
    os.system("")

# Terminal styling constants
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"

# Subprocess timeout threshold to prevent antivirus overhead timeouts on Windows
DEFAULT_TIMEOUT = 25.0

PASS_BADGE = f"{COLOR_BOLD}{COLOR_GREEN}[ PASS ]{COLOR_RESET}"
FAIL_BADGE = f"{COLOR_BOLD}{COLOR_RED}[ FAIL ]{COLOR_RESET}"
SKIP_BADGE = f"{COLOR_BOLD}{COLOR_YELLOW}[ SKIP ]{COLOR_RESET}"

IGNORED_DIRS = {
    "templates",
    "scripts",
    "benchmarks",
    "index",
    ".git",
    ".github",
    ".system_generated",
    "__pycache__",
    ".vscode",
    ".idea",
}


def normalize_output(text: str) -> str:
    """Normalize text by stripping trailing whitespace per line and overall trailing newlines."""
    if not text:
        return ""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned_lines = [line.rstrip() for line in lines]
    while cleaned_lines and cleaned_lines[-1] == "":
        cleaned_lines.pop()
    return "\n".join(cleaned_lines)


class SolutionTest:
    def __init__(self, file_path: Path, repo_root: Path):
        self.file_path = file_path.resolve()
        self.rel_path = file_path.relative_to(repo_root)
        self.repo_root = repo_root
        self.dir_path = self.file_path.parent
        self.language = "Go" if file_path.suffix == ".go" else "C++"
        self.stem = file_path.stem
        self.problem_id = self.stem.split("_")[0] if "_" in self.stem else self.stem

        self.input_file, self.expected_file = self._resolve_fixtures()

    def _resolve_fixtures(self) -> Tuple[Optional[Path], Optional[Path]]:
        """Resolves test fixtures using problem-specific naming or directory-level fallback."""
        # 1. Exact stem: e.g., 2269B_KiaKio_input.txt & 2269B_KiaKio_expected.txt
        stem_in = self.dir_path / f"{self.stem}_input.txt"
        stem_exp = self.dir_path / f"{self.stem}_expected.txt"
        if stem_in.is_file() and stem_exp.is_file():
            return stem_in, stem_exp

        # 2. Problem ID prefix: e.g., 2269B_input.txt & 2269B_expected.txt
        id_in = self.dir_path / f"{self.problem_id}_input.txt"
        id_exp = self.dir_path / f"{self.problem_id}_expected.txt"
        if id_in.is_file() and id_exp.is_file():
            return id_in, id_exp

        # 3. Directory-level fallback: input.txt & expected.txt
        dir_in = self.dir_path / "input.txt"
        dir_exp = self.dir_path / "expected.txt"
        if dir_in.is_file() and dir_exp.is_file():
            solutions_in_dir = [
                f for f in self.dir_path.iterdir()
                if f.is_file() and f.suffix in (".go", ".cpp") and not f.name.startswith(".")
            ]
            if len(solutions_in_dir) <= 1:
                return dir_in, dir_exp

            # For backward compatibility when multiple solutions exist in the folder,
            # assign generic input.txt to the first alphabetical solution
            solutions_in_dir.sort(key=lambda p: p.name)
            if solutions_in_dir and solutions_in_dir[0] == self.file_path:
                return dir_in, dir_exp

        return None, None

    def has_test_fixtures(self) -> bool:
        return (
            self.input_file is not None
            and self.expected_file is not None
            and self.input_file.is_file()
            and self.expected_file.is_file()
        )

    def run(self, timeout: float = DEFAULT_TIMEOUT) -> Tuple[bool, str, float, Optional[str]]:
        """
        Executes the solution passing input.txt to stdin.
        For C++: Compiles with `g++ -O3 <file> -o temp_bin`, runs `temp_bin`, and deletes `temp_bin`.
        For Go: Compiles with `go build -o temp_go_bin.exe <file>`, runs `temp_go_bin.exe`, and strictly deletes `temp_go_bin.exe`.
        Returns: (passed, actual_output, elapsed_ms, error_message)
        """
        if not self.has_test_fixtures():
            return False, "", 0.0, "Missing input.txt or expected.txt"

        try:
            with open(self.input_file, "r", encoding="utf-8-sig", errors="replace") as f:
                input_data = f.read()
        except Exception as e:
            return False, "", 0.0, f"Cannot read input file: {e}"

        try:
            with open(self.expected_file, "r", encoding="utf-8-sig", errors="replace") as f:
                expected_data = f.read()
        except Exception as e:
            return False, "", 0.0, f"Cannot read expected file: {e}"

        temp_bin = self.repo_root / "temp_bin"
        temp_bin_exe = self.repo_root / "temp_bin.exe"
        temp_go_bin = self.repo_root / "temp_go_bin.exe"

        def cleanup_temp_bin():
            for p in (temp_bin, temp_bin_exe, temp_go_bin):
                if p.is_file():
                    for _ in range(5):
                        try:
                            p.unlink()
                            break
                        except Exception:
                            time.sleep(0.05)

        cleanup_temp_bin()

        try:
            if self.language == "C++":
                compile_cmd = ["g++", "-O3", str(self.file_path), "-o", str(temp_bin)]
                try:
                    comp_proc = subprocess.run(
                        compile_cmd,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        cwd=str(self.repo_root),
                        timeout=timeout,
                    )
                except subprocess.TimeoutExpired:
                    return False, "", timeout * 1000.0, f"C++ Compilation timed out (> {timeout}s)"

                if comp_proc.returncode != 0:
                    return (
                        False,
                        "",
                        0.0,
                        f"C++ Compilation failed:\n{comp_proc.stderr.strip()}",
                    )

                exec_target = temp_bin_exe if temp_bin_exe.is_file() else temp_bin
                run_cmd = [str(exec_target)]
            else:
                compile_cmd = ["go", "build", "-o", str(temp_go_bin), str(self.file_path)]
                try:
                    comp_proc = subprocess.run(
                        compile_cmd,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        cwd=str(self.repo_root),
                        timeout=timeout,
                    )
                except subprocess.TimeoutExpired:
                    return False, "", timeout * 1000.0, f"Go Compilation timed out (> {timeout}s)"

                if comp_proc.returncode != 0:
                    return (
                        False,
                        "",
                        0.0,
                        f"Go Compilation failed:\n{comp_proc.stderr.strip()}",
                    )

                run_cmd = [str(temp_go_bin)]

            start_time = time.perf_counter()
            try:
                proc = subprocess.run(
                    run_cmd,
                    input=input_data,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    timeout=timeout,
                    cwd=str(self.repo_root),
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            except subprocess.TimeoutExpired:
                return False, "", timeout * 1000.0, f"Execution timed out (> {timeout}s)"
            except Exception as e:
                return False, "", 0.0, f"Execution error: {e}"

            actual_stdout = proc.stdout

            # Fallback check: if stdout is empty but output.txt was produced in problem dir
            if not actual_stdout.strip():
                local_out = self.dir_path / "output.txt"
                if local_out.is_file():
                    try:
                        with open(local_out, "r", encoding="utf-8-sig", errors="replace") as f:
                            file_out = f.read()
                            if file_out.strip():
                                actual_stdout = file_out
                    except Exception:
                        pass

            if proc.returncode != 0:
                err_msg = (
                    f"Process exited with non-zero code {proc.returncode}.\n"
                    f"STDERR:\n{proc.stderr.strip()}"
                )
                return False, actual_stdout, elapsed_ms, err_msg

            norm_actual = normalize_output(actual_stdout)
            norm_expected = normalize_output(expected_data)

            if norm_actual == norm_expected:
                return True, norm_actual, elapsed_ms, None

            # Generate unified diff
            diff_lines = list(
                difflib.unified_diff(
                    [line + "\n" for line in norm_expected.splitlines()],
                    [line + "\n" for line in norm_actual.splitlines()],
                    fromfile="expected.txt",
                    tofile="actual_stdout",
                )
            )
            diff_str = "".join(diff_lines) if diff_lines else f"Expected: {repr(norm_expected)}\nGot: {repr(norm_actual)}"
            return False, norm_actual, elapsed_ms, f"Mismatch:\n{diff_str}"

        finally:
            cleanup_temp_bin()


def find_solutions(repo_root: Path) -> List[SolutionTest]:
    """Recursively scans repository exclusively for .go and .cpp solution files."""
    solutions: List[SolutionTest] = []
    for root, dirs, files in os.walk(repo_root):
        rel_root = Path(root).relative_to(repo_root)
        parts = [p.lower() for p in rel_root.parts]

        if any(p in IGNORED_DIRS or p.startswith(".") for p in parts):
            continue

        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d.lower() not in IGNORED_DIRS
        ]

        for file in files:
            if file.startswith("."):
                continue
            if file.endswith((".go", ".cpp")):
                file_path = Path(root) / file
                solutions.append(SolutionTest(file_path, repo_root))

    solutions.sort(key=lambda s: str(s.rel_path))
    return solutions


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}  Codeforces Standard I/O Test Runner (Go & C++)    {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"Repository Root: {COLOR_DIM}{repo_root}{COLOR_RESET}\n")

    solutions = find_solutions(repo_root)

    if not solutions:
        print(f"{COLOR_YELLOW}No solution files (.go / .cpp) discovered.{COLOR_RESET}")
        return 0

    passed_count = 0
    failed_count = 0
    skipped_count = 0

    print(f"{COLOR_BOLD}Discovered {len(solutions)} solution(s):{COLOR_RESET}\n")

    for sol in solutions:
        lang_color = COLOR_MAGENTA if sol.language == "Go" else COLOR_BLUE
        lang_badge = f"{lang_color}[{sol.language}]{COLOR_RESET}"
        target_display = f"{lang_badge} {COLOR_BOLD}{sol.rel_path}{COLOR_RESET}"

        if not sol.has_test_fixtures():
            skipped_count += 1
            print(f"  {SKIP_BADGE} {target_display}")
            print(f"         {COLOR_DIM}No test fixtures found (requires input.txt and expected.txt){COLOR_RESET}")
            continue

        passed, actual, elapsed, error = sol.run(timeout=DEFAULT_TIMEOUT)

        if passed:
            passed_count += 1
            time_str = f"{elapsed:.1f}ms"
            print(f"  {PASS_BADGE} {target_display} {COLOR_DIM}({time_str}){COLOR_RESET}")
        else:
            failed_count += 1
            print(f"  {FAIL_BADGE} {target_display}")
            if error:
                indented_error = "\n".join("         " + line for line in error.splitlines())
                print(f"{COLOR_RED}{indented_error}{COLOR_RESET}")

    # Summary
    print(f"\n{COLOR_BOLD}----------------------------------------------------{COLOR_RESET}")
    print(f"Summary: {COLOR_GREEN}{passed_count} Passed{COLOR_RESET}, "
          f"{COLOR_RED}{failed_count} Failed{COLOR_RESET}, "
          f"{COLOR_YELLOW}{skipped_count} Skipped{COLOR_RESET} "
          f"(Total: {len(solutions)})")
    print(f"{COLOR_BOLD}----------------------------------------------------{COLOR_RESET}\n")

    if failed_count > 0:
        print(f"{COLOR_BOLD}{COLOR_RED}FAILED: Some test cases failed.{COLOR_RESET}\n")
        return 1

    print(f"{COLOR_BOLD}{COLOR_GREEN}SUCCESS: All tested solutions passed!{COLOR_RESET}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
