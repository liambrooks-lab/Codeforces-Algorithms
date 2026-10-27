#!/usr/bin/env python3
"""
scripts/indexer.py - Automated Competitive Programming Catalog & Indexing Engine
Scans problem directories for Go and C++ solutions and generates index/index.json.
Parses top JSON metadata comment blocks for problem details and complexity.
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
COLOR_BLUE = "\033[94m"

FILENAME_REGEX = re.compile(r"^([0-9]+[A-Za-z][0-9]*)(?:_(.*))?\.(go|cpp)$", re.IGNORECASE)

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


def extract_metadata(file_path: Path) -> Dict[str, str]:
    """
    Parses a multi-line comment at the very top of .go and .cpp files
    containing a JSON block formatted as:
    /*
    {
        "problem_name": "...",
        "category": "...",
        "time_complexity": "...",
        "space_complexity": "..."
    }
    */
    Gracefully falls back to default/empty values without crashing.
    """
    defaults = {
        "problem_name": "",
        "category": "",
        "time_complexity": "",
        "space_complexity": "",
    }
    if not file_path.is_file():
        return defaults

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(4096)

        # Match JSON block wrapped in /* and */ at the top of the file
        match = re.search(r"/\*\s*(\{.*?\})\s*\*/", content, re.DOTALL)
        if match:
            json_text = match.group(1).strip()
            data = json.loads(json_text)
            if isinstance(data, dict):
                return {
                    "problem_name": str(data.get("problem_name", "")),
                    "category": str(data.get("category", "")),
                    "time_complexity": str(data.get("time_complexity", "")),
                    "space_complexity": str(data.get("space_complexity", "")),
                }
    except Exception:
        pass

    return defaults


def parse_solution(file_path: Path, repo_root: Path) -> Dict[str, Any]:
    """Extracts problem metadata from filename, directory structure, and top JSON header."""
    rel_path = file_path.relative_to(repo_root)
    dir_category = rel_path.parts[0] if len(rel_path.parts) > 1 else "Root"
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

    language = "Go" if ext == "go" else "C++"
    dir_path = file_path.parent
    stem = file_path.stem

    # Check problem-specific fixtures first, then directory-level
    has_tests = (
        ((dir_path / f"{stem}_input.txt").is_file() and (dir_path / f"{stem}_expected.txt").is_file())
        or ((dir_path / f"{problem_id}_input.txt").is_file() and (dir_path / f"{problem_id}_expected.txt").is_file())
    )
    if not has_tests:
        dir_in = dir_path / "input.txt"
        dir_exp = dir_path / "expected.txt"
        if dir_in.is_file() and dir_exp.is_file():
            solutions_in_dir = sorted(
                [f for f in dir_path.iterdir() if f.is_file() and f.suffix in (".go", ".cpp") and not f.name.startswith(".")],
                key=lambda p: p.name,
            )
            if len(solutions_in_dir) <= 1 or (solutions_in_dir and solutions_in_dir[0] == file_path):
                has_tests = True

    # Parse metadata from top JSON comment block
    meta = extract_metadata(file_path)
    problem_name = meta["problem_name"] if meta["problem_name"] else problem_title
    category = meta["category"] if meta["category"] else dir_category
    time_complexity = meta["time_complexity"]
    space_complexity = meta["space_complexity"]

    return {
        "problem_id": problem_id,
        "problem_name": problem_name,
        "title": problem_name,
        "category": category,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "language": language,
        "file": str(rel_path).replace("\\", "/"),
        "has_tests": has_tests,
    }


def scan_and_index(repo_root: Path) -> Dict[str, Any]:
    index_by_category: Dict[str, List[Dict[str, Any]]] = {}
    by_language: Dict[str, int] = {"Go": 0, "C++": 0}
    total_problems = 0

    for item in sorted(repo_root.iterdir()):
        if not item.is_dir():
            continue
        folder_name = item.name
        if folder_name.lower() in IGNORED_TOP_DIRS or folder_name.startswith("."):
            continue

        category_problems: List[Dict[str, Any]] = []

        for root, dirs, files in os.walk(item):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in IGNORED_TOP_DIRS]

            for file in sorted(files):
                if file.startswith("."):
                    continue
                # Strictly index .go and .cpp solution files
                if file.endswith((".go", ".cpp")):
                    file_path = Path(root) / file
                    parsed = parse_solution(file_path, repo_root)
                    category_problems.append(parsed)

                    lang = parsed["language"]
                    by_language[lang] = by_language.get(lang, 0) + 1
                    total_problems += 1

        if category_problems:
            category_problems.sort(key=lambda x: (x["problem_id"], x["problem_name"]))
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
    print(f"{COLOR_BOLD}{COLOR_CYAN}  Codeforces Repository Indexer (Go & C++)          {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"Scanning root: {COLOR_DIM}{repo_root}{COLOR_RESET}\n")

    catalog = scan_and_index(repo_root)

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    stats = catalog["stats"]
    print(f"{COLOR_BOLD}Total Solved:{COLOR_RESET} {COLOR_GREEN}{stats['total_solved']}{COLOR_RESET}")
    for lang, count in stats["by_language"].items():
        lang_color = COLOR_MAGENTA if lang == "Go" else COLOR_BLUE
        print(f"  - {lang_color}{lang}{COLOR_RESET}: {count}")

    print(f"\n{COLOR_BOLD}Categories Cataloged:{COLOR_RESET}")
    for cat, items in catalog["categories"].items():
        print(f"  [{cat}] ({len(items)} problems)")
        for item in items:
            tests_badge = f"{COLOR_GREEN}[TESTS: YES]{COLOR_RESET}" if item["has_tests"] else f"{COLOR_DIM}[TESTS: NO]{COLOR_RESET}"
            complexity_str = f" [{item['time_complexity']} / {item['space_complexity']}]" if item['time_complexity'] or item['space_complexity'] else ""
            print(f"    - {COLOR_BOLD}{item['problem_id']}{COLOR_RESET}: {item['problem_name']} ({item['language']}){complexity_str} {tests_badge}")

    print(f"\n{COLOR_BOLD}{COLOR_GREEN}Index written successfully to:{COLOR_RESET} {index_file}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
