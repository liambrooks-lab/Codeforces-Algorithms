#!/usr/bin/env python3
"""
scripts/indexer.py - Automated Competitive Programming Catalog & Indexing Engine
Scans problem directories (e.g., Practice_*, Virtual_Contests) and builds structured index in index/index.json.
"""

import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

# Terminal styling constants
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_GREEN = "\033[92m"
COLOR_CYAN = "\033[96m"
COLOR_YELLOW = "\033[93m"
COLOR_MAGENTA = "\033[95m"

FILENAME_REGEX = re.compile(r"^([0-9]+[A-Za-z][0-9]*)(?:_(.*))?\.(go|py)$", re.IGNORECASE)

IGNORED_TOP_DIRS = {
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


def parse_solution(file_path: Path, repo_root: Path) -> Dict[str, Any]:
    """Extracts problem metadata from filename and directory structure."""
    rel_path = file_path.relative_to(repo_root)
    category = rel_path.parts[0] if len(rel_path.parts) > 1 else "Root"
    filename = file_path.name

    match = FILENAME_REGEX.match(filename)
    if match:
        problem_id = match.group(1).upper()
        raw_name = match.group(2)
        problem_title = raw_name.replace("_", " ") if raw_name else problem_id
        ext = match.group(3).lower()
    else:
        stem = file_path.stem
        problem_id = stem
        problem_title = stem.replace("_", " ")
        ext = file_path.suffix.lstrip(".").lower()

    language = "Go" if ext == "go" else ("Python" if ext == "py" else ext.upper())
    dir_path = file_path.parent
    has_tests = (dir_path / "input.txt").is_file() and (dir_path / "expected.txt").is_file()

    return {
        "problem_id": problem_id,
        "title": problem_title,
        "category": category,
        "language": language,
        "file": str(rel_path).replace("\\", "/"),
        "has_tests": has_tests,
    }


def scan_and_index(repo_root: Path) -> Dict[str, Any]:
    index_by_category: Dict[str, List[Dict[str, Any]]] = {}
    by_language: Dict[str, int] = {"Go": 0, "Python": 0}
    total_problems = 0

    for item in sorted(repo_root.iterdir()):
        if not item.is_dir():
            continue
        folder_name = item.name
        if folder_name.lower() in IGNORED_TOP_DIRS or folder_name.startswith("."):
            continue

        # We primarily scan Practice_* and Virtual_Contest* or any non-ignored directories
        category_problems: List[Dict[str, Any]] = []

        for root, dirs, files in os.walk(item):
            # Prune hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in IGNORED_TOP_DIRS]

            for file in sorted(files):
                if file.startswith("."):
                    continue
                if file.endswith((".go", ".py")):
                    file_path = Path(root) / file
                    parsed = parse_solution(file_path, repo_root)
                    category_problems.append(parsed)

                    lang = parsed["language"]
                    by_language[lang] = by_language.get(lang, 0) + 1
                    total_problems += 1

        if category_problems:
            category_problems.sort(key=lambda x: (x["problem_id"], x["title"]))
            index_by_category[folder_name] = category_problems

    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "stats": {
            "total_solved": total_problems,
            "by_language": by_language,
            "categories_count": len(index_by_category),
        },
        "categories": index_by_category,
    }

    return payload


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    index_dir = repo_root / "index"
    index_file = index_dir / "index.json"

    index_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}  Codeforces Repository Indexer                     {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"Scanning root: {COLOR_DIM}{repo_root}{COLOR_RESET}\n")

    catalog = scan_and_index(repo_root)

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    stats = catalog["stats"]
    print(f"{COLOR_BOLD}Total Solved:{COLOR_RESET} {COLOR_GREEN}{stats['total_solved']}{COLOR_RESET}")
    for lang, count in stats["by_language"].items():
        print(f"  - {COLOR_MAGENTA}{lang}{COLOR_RESET}: {count}")

    print(f"\n{COLOR_BOLD}Categories Cataloged:{COLOR_RESET}")
    for cat, items in catalog["categories"].items():
        print(f"  [{cat}] ({len(items)} problems)")
        for item in items:
            tests_badge = f"{COLOR_GREEN}[TESTS: YES]{COLOR_RESET}" if item["has_tests"] else f"{COLOR_DIM}[TESTS: NO]{COLOR_RESET}"
            print(f"    - {COLOR_BOLD}{item['problem_id']}{COLOR_RESET}: {item['title']} ({item['language']}) {tests_badge}")

    print(f"\n{COLOR_BOLD}{COLOR_GREEN}Index written successfully to:{COLOR_RESET} {index_file}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
