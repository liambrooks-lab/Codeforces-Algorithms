#!/usr/bin/env python3
"""
scripts/cleaner.py - Repository Artifact Cleaning Engine
Recursively cleans stray .exe, .out, temp_bin, temp_bin.exe, temp_go_bin.exe, and __pycache__ artifacts.
"""

import os
import pathlib
import shutil
import sys

# Terminal styling constants
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[92m"
COLOR_CYAN = "\033[96m"
COLOR_RED = "\033[91m"
COLOR_DIM = "\033[2m"

if os.name == "nt":
    os.system("")


def clean_repo(repo_root: pathlib.Path) -> int:
    patterns = [
        "**/*.exe",
        "**/*.out",
        "**/temp_bin",
        "**/temp_bin.exe",
        "**/temp_go_bin.exe",
        "**/temp_go_bin",
    ]

    removed_files = 0
    removed_dirs = 0

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}  Codeforces Repository Cleanup                     {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"Scanning from: {COLOR_DIM}{repo_root}{COLOR_RESET}\n")

    for pat in patterns:
        for file_path in repo_root.glob(pat):
            # Do not delete files inside .git
            if ".git" in file_path.parts:
                continue
            if file_path.is_file():
                try:
                    rel = file_path.relative_to(repo_root)
                    file_path.unlink()
                    removed_files += 1
                    print(f"  {COLOR_GREEN}[REMOVED FILE]{COLOR_RESET} {rel}")
                except Exception as e:
                    print(f"  {COLOR_RED}[FAILED]{COLOR_RESET} {file_path}: {e}")

    for pycache_dir in repo_root.glob("**/__pycache__"):
        if ".git" in pycache_dir.parts:
            continue
        if pycache_dir.is_dir():
            try:
                rel = pycache_dir.relative_to(repo_root)
                shutil.rmtree(pycache_dir)
                removed_dirs += 1
                print(f"  {COLOR_GREEN}[REMOVED DIR]{COLOR_RESET}  {rel}")
            except Exception as e:
                print(f"  {COLOR_RED}[FAILED]{COLOR_RESET} {pycache_dir}: {e}")

    total = removed_files + removed_dirs
    print(f"\n{COLOR_BOLD}Cleanup completed:{COLOR_RESET} {COLOR_GREEN}{total} artifact(s) removed{COLOR_RESET} "
          f"({removed_files} files, {removed_dirs} dirs).\n")
    return 0


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    return clean_repo(repo_root)


if __name__ == "__main__":
    sys.exit(main())
