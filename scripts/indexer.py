#!/usr/bin/env python3
"""
scripts/indexer.py - Automated Algorithmic Catalog & Indexing Engine
Scans topic directories for Go and C++ solutions, parses top JSON metadata,
generates index/index.json and overwrites README.md matching the leetcode-stack standard.
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

README_PREFIX = """# leetcode-stack

[हिंदी में पढ़ें](https://github.com/liambrooks-lab/leetcode-stack/blob/master/README.md)

---
> **A zero-to-one algorithmic infrastructure, independently architected for state-space optimization, advanced data structure engineering, and computational efficiency.**

Engineered entirely from the ground up, this repository serves as a systematic archive of rigorous problem-solving. Every algorithmic module is strictly authored to enforce minimal auxiliary space and optimal asymptotic time complexities, reflecting continuous deployment from the LeetCode platform.

---

## Execution Stack

Solutions are implemented across three runtime environments based on architectural characteristics:

* **`C++`** (C++17) &mdash; Direct memory control, pointer arithmetic, and deterministic execution performance.
* **`Python 3`** &mdash; Standard library data structures, concise algorithm orchestration, and mathematical modeling.
* **`Golang`** (Go 1.22) &mdash; Static typing, explicit memory allocation, pre-allocated slices to minimize garbage collection overhead, and native testing tooling.

---

## Architecture & Taxonomy

The repository is maintained autonomously and structured strictly by algorithmic taxonomy. Each isolated module typically contains:
* The raw source code implementation.
* Problem constraints and edge-case definitions.
* Execution metrics (Time & Space complexity, synchronized in real-time).
"""

README_SNIPPETS = """### Snippets

**Arrays &mdash; In-Place Two-Pointer Partitioning:**
```go
// Partitions slice in-place around a predicate in O(N) time and O(1) auxiliary space
func partition(nums []int, pivot int) int {
\tleft := 0
\tfor right := 0; right < len(nums); right++ {
\t\tif nums[right] < pivot {
\t\t\tnums[left], nums[right] = nums[right], nums[left]
\t\t\tleft++
\t\t}
\t}
\treturn left
}
```

**Backtracking &mdash; State-Space Search & Branch Pruning:**
```python
# Generic backtracking engine with state pruning
def backtrack(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    candidates.sort()

    def dfs(start: int, remaining: int, path: list[int]):
        if remaining == 0:
            result.append(list(path))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            path.append(candidates[i])
            dfs(i + 1, remaining - candidates[i], path)
            path.pop()

    dfs(0, target, [])
    return result
```

**Binary Search &mdash; Monotonic Predicate Lower Bound:**
```cpp
// Returns the first index where predicate is satisfied; O(log N) time, O(1) space
int lower_bound(const std::vector<int>& nums, int target) {
    int left = 0, right = static_cast<int>(nums.size());
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] >= target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    return left;
}
```

**Binary Indexed Tree (Fenwick Tree) &mdash; Prefix Accumulation & Point Mutation:**
```cpp
// O(log N) point update and prefix query on 1-based indexing
class FenwickTree {
    std::vector<int> tree;
    int size;
public:
    explicit FenwickTree(int n) : size(n), tree(n + 1, 0) {}

    void add(int i, int delta) {
        for (; i <= size; i += i & -i) tree[i] += delta;
    }

    int query(int i) const {
        int sum = 0;
        for (; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }
};
```

**Bit Manipulation &mdash; Mask Operations & Lowest Set Bit:**
```go
// Pure bitwise operations bypassing arithmetic overhead; O(1) time and space
func bitwiseOperations(n int, mask int) (lowestBit int, isPowerOfTwo bool, clearedBit int) {
\tlowestBit = n & -n                      // Isolate lowest set bit
\tisPowerOfTwo = n > 0 && (n&(n-1)) == 0 // Check power of two
\tclearedBit = n & ^(1 << mask)          // Clear specific bit at mask position
\treturn
}
```

**Cyclic Sort &mdash; In-Place 1-to-N Index Mapping:**
```python
# Aligns positive integers to their 0-indexed positions in O(N) time and O(1) space
def cyclic_sort(nums: list[int]) -> list[int]:
    i, n = 0, len(nums)
    while i < n:
        correct_idx = nums[i] - 1
        if 0 <= correct_idx < n and nums[i] != nums[correct_idx]:
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
    return nums
```

**Dynamic Programming &mdash; Space-Optimized Rolling State Tabulation:**
```go
// Computes recurrence using rolling buffer; O(N) time and O(1) auxiliary space
func rollingDP(cost []int) int {
\tn := len(cost)
\tif n <= 1 {
\t\treturn 0
\t}
\tprev2, prev1 := 0, 0
\tfor i := 2; i <= n; i++ {
\t\tc1 := prev1 + cost[i-1]
\t\tc2 := prev2 + cost[i-2]
\t\tcurrent := c1
\t\tif c2 < current {
\t\t\tcurrent = c2
\t\t}
\t\tprev2, prev1 = prev1, current
\t}
\treturn prev1
}
```

**Game Theory &mdash; Minimax Terminal State Evaluation:**
```python
# Evaluates symmetric zero-sum terminal conditions in O(N) time and O(1) space
def evaluate_game(state: list[int]) -> bool:
    balance = sum(state[:len(state)//2]) - sum(state[len(state)//2:])
    return balance != 0
```

**Graphs &mdash; Breadth-First Search & Level-Order Traversal:**
```cpp
// Traverses unweighted graph via BFS; O(V + E) time, O(V) space
std::vector<int> bfs_traversal(int start, const std::vector<std::vector<int>>& adj) {
    std::vector<int> order;
    std::vector<bool> visited(adj.size(), false);
    std::queue<int> q;

    visited[start] = true;
    q.push(start);

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);

        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
    return order;
}
```

**Greedy &mdash; Monotonic Frontier Expansion:**
```python
# Expands furthest reachable frontier in a single linear pass; O(N) time, O(1) space
def greedy_jump_frontier(nums: list[int]) -> int:
    jumps = current_end = furthest = 0
    for i in range(len(nums) - 1):
        furthest = max(furthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = furthest
    return jumps
```

**Hashing &mdash; Constant-Time State Deduplication & Frequency Tracking:**
```python
# Single-pass frequency mapping for target resolution; O(N) time, O(N) space
def find_pair_sum(nums: list[int], target: int) -> list[int]:
    lookup = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in lookup:
            return [lookup[complement], i]
        lookup[x] = i
    return []
```

**Intervals &mdash; In-Place Boundary Sweep & Merging:**
```python
# Merges overlapping intervals after O(N log N) sort; O(N) space
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**Linked Lists &mdash; Fast and Slow Pointer Cycle Detection:**
```go
// Detects cycle existence via Floyd's tortoise and hare; O(N) time, O(1) space
func hasCycle(head *ListNode) bool {
\tslow, fast := head, head
\tfor fast != nil && fast.Next != nil {
\t\tslow = slow.Next
\t\tfast = fast.Next.Next
\t\tif slow == fast {
\t\t\treturn true
\t\t}
\t}
\treturn false
}
```

**Math &mdash; Binary Exponentiation with Modulo:**
```cpp
// Computes (base^exp) % mod in O(log exp) time and O(1) space
long long modular_pow(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}
```

**Matrices &mdash; Directional Boundary Shrink Scan:**
```python
# Traverses a 2D matrix in spiral boundary order; O(M * N) time, O(1) auxiliary space
def matrix_boundary_scan(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result = []

    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result
```

**Prefix Sum &mdash; Auxiliary Range Accumulation for O(1) Queries:**
```go
// Pre-allocates prefix sum array for O(1) range sum queries; O(N) time and space
func buildPrefixSum(nums []int) []int {
\tn := len(nums)
\tprefix := make([]int, n+1)
\tfor i := 0; i < n; i++ {
\t\tprefix[i+1] = prefix[i] + nums[i]
\t}
\treturn prefix // Range [i, j] sum is prefix[j+1] - prefix[i]
}
```

**Segment Tree &mdash; Point Update & Range Aggregation:**
```cpp
// Range sum segment tree; O(N) construction, O(log N) query and update
class SegmentTree {
    std::vector<int> tree;
    int n;
public:
    explicit SegmentTree(const std::vector<int>& data) : n(data.size()), tree(4 * data.size(), 0) {
        build(data, 1, 0, n - 1);
    }

    void build(const std::vector<int>& data, int node, int l, int r) {
        if (l == r) { tree[node] = data[l]; return; }
        int mid = (l + r) / 2;
        build(data, 2 * node, l, mid);
        build(data, 2 * node + 1, mid + 1, r);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    void update(int node, int l, int r, int idx, int val) {
        if (l == r) { tree[node] = val; return; }
        int mid = (l + r) / 2;
        if (idx <= mid) update(2 * node, l, mid, idx, val);
        else update(2 * node + 1, mid + 1, r, idx, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    int query(int node, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tree[node];
        if (r < ql || l > qr) return 0;
        int mid = (l + r) / 2;
        return query(2 * node, l, mid, ql, qr) + query(2 * node + 1, mid + 1, r, ql, qr);
    }
};
```

**Sliding Window &mdash; Dynamic Two-Pointer Contraction:**
```go
// Maintains variable-size sliding window with frequency bounds; O(N) time, O(K) space
func longestDistinctSubstr(s string) int {
\tlastPos := make(map[byte]int)
\tmaxLen, left := 0, 0
\tfor right := 0; right < len(s); right++ {
\t\tif prev, exists := lastPos[s[right]]; exists && prev >= left {
\t\t\tleft = prev + 1
\t\t}
\tlastPos[s[right]] = right
\tcurLen := right - left + 1
\tif curLen > maxLen {
\t\tmaxLen = curLen
\t}
\t}
\treturn maxLen
}
```

**Sorting &mdash; Three-Way In-Place Dutch National Flag Partition:**
```cpp
// Partitions array into three regions (0, 1, 2) in-place; O(N) time, O(1) space
void three_way_partition(std::vector<int>& nums) {
    int low = 0, mid = 0, high = static_cast<int>(nums.size()) - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            std::swap(nums[low++], nums[mid++]);
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            std::swap(nums[mid], nums[high--]);
        }
    }
}
```

**Stacks &mdash; Monotonic Next-Greater Element Resolution:**
```go
// Finds next greater element index for each position; O(N) time, O(N) space
func nextGreaterIndices(nums []int) []int {
\tn := len(nums)
\tres := make([]int, n)
\tfor i := range res {
\t\tres[i] = -1
\t}
\tstack := make([]int, 0, n) // Monotonic decreasing index stack

\tfor i := 0; i < n; i++ {
\t\tfor len(stack) > 0 && nums[i] > nums[stack[len(stack)-1]] {
\t\t\ttop := stack[len(stack)-1]
\t\t\tstack = stack[:len(stack)-1]
\t\t\tres[top] = i
\t\t}
\t\tstack = append(stack, i)
\t}
\treturn res
}
```

**Strings &mdash; Two-Pointer Palindrome Boundary Expansion:**
```python
# Expands around centers in-place; O(N^2) time, O(1) auxiliary space
def longest_palindrome_span(s: str) -> str:
    start, max_len = 0, 0
    for i in range(len(s)):
        for l, r in ((i, i), (i, i + 1)):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            span = r - l - 1
            if span > max_len:
                max_len = span
                start = l + 1
    return s[start:start + max_len]
```

**Trees &mdash; Post-Order Subtree Aggregation & State Propagation:**
```python
# Traverses binary tree in post-order aggregating subtree metrics; O(N) time, O(H) space
def evaluate_subtree_metrics(root) -> tuple[int, int]:
    if not root:
        return 0, 0 # (sum, count)
    left_sum, left_count = evaluate_subtree_metrics(root.left)
    right_sum, right_count = evaluate_subtree_metrics(root.right)
    total_sum = root.val + left_sum + right_sum
    total_count = 1 + left_count + right_count
    return total_sum, total_count
```

**Two Pointers &mdash; Inward Convergence with Redundant Boundary Pruning:**
```go
// Inward two-pointer search with redundant boundary skipping; O(N) time, O(1) space
func maxAreaContainer(height []int) int {
\tleft, right := 0, len(height)-1
\tmaxArea := 0
\tfor left < right {
\t\thL, hR := height[left], height[right]
\t\th := hL
\t\tif hR < h {
\t\t\th = hR
\t\t}
\t\tarea := h * (right - left)
\t\tif area > maxArea {
\t\t\tmaxArea = area
\t\t}
\t\tif hL < hR {
\t\t\tfor left < right && height[left] <= hL {
\t\t\t\tleft++
\t\t\t}
\t\t} else {
\t\t\tfor left < right && height[right] <= hR {
\t\t\t\tright--
\t\t\t}
\t\t}
\t}
\treturn maxArea
}
```
"""

README_SUFFIX = """---

## Engineering Standards

All modules are engineered with a strict focus on system-level constraints:
* **Time Complexity:** Optimized for minimal asymptotic upper bounds.
* **Space Complexity:** Emphasis on strictly in-place modifications and zero-overhead auxiliary space allocation.
* **Taxonomy:** Comprehensive coverage across Arrays, Backtracking, Binary Search, Bit Manipulation, Cyclic Sort, Dynamic Programming, Game Theory, Graphs, Greedy, Hashing, Intervals, Linked Lists, Math, Matrices, Prefix Sum, Segment Tree, Sliding Window, Stacks, Strings, Trees, and Two Pointers.

---

## Automation Pipeline

This infrastructure relies on zero manual indexing. Solutions are integrated, compiled, and pushed in real-time upon successful boundary validation on the master platform via automated CI/CD synchronization workflows. Our custom test, linting, and bare-metal benchmarking architecture operates flawlessly through GitHub Actions.

---

## Computational Paradigms & Micro-Optimizations

Beyond adhering to standard asymptotic limits, this repository enforces execution constraints to minimize runtime overheads (e.g., runtime garbage collection overhead and heap allocation latency):

* **State-Space Pruning:** Mathematical termination of duplicate recursive branches and overlapping subproblems prior to execution.
* **In-Place Mutability:** Minimization of auxiliary tracking structures via pointer manipulation, cyclic swapping, and bitwise state shifts.
* **Runtime-Agnostic Arithmetic:** Utilizing direct ASCII memory access and bit-level operations to avoid type-conversion latency.

---

## Local Execution

To benchmark implementations locally, deploy the following standard execution protocols:

**C++**
```bash
g++ -O3 -std=c++17 filename.cpp -o executable
./executable
```

**Python**
```bash
python3 filename.py
```

**Golang**
```bash
go run filename.go
```

---

## Fault Tolerance

These modules are architected as isolated algorithmic functions stripped of redundant boilerplate. Local execution may encounter expected integration faults. Deploy the following protocols to override them:

* **Missing Entry Point (Execution Halt):** Core modules omit driver code. You must manually instantiate the `Solution` class within a standard `main()` function prior to local C++ compilation.
* **Memory Anomalies & Segmentation Faults:** To diagnose uninitialized pointers, out-of-bounds access, or stack smashing during local testing, enforce GCC memory sanitization:
  ```bash
  g++ -O3 -Wall -Wextra -fsanitize=address filename.cpp -o debug_exec
  ./debug_exec
  ```
* **Package Main & Entry Point:** Core modules are organized into functional packages without main driver functions. For isolated execution via `go run`, define a main package and entry point, or execute tests via `go test -v`.

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
 Leetcode · DSA · Python3 · C++ · Golang
</p>
"""


def extract_metadata(file_path: Path) -> Dict[str, str]:
    """
    Parses a multi-line comment at the very top of .go and .cpp files
    containing a JSON block formatted as:
    /*
    {
        "problem_name": "...",
        "category": "...",
        "time_complexity": "...",
        "space_complexity": "...",
        "formula_used": "..."
    }
    */
    Gracefully falls back to default/empty values without crashing.
    """
    defaults = {
        "problem_name": "",
        "category": "",
        "time_complexity": "",
        "space_complexity": "",
        "formula_used": "",
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
                    "formula_used": str(data.get("formula_used", "")),
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
    category = meta["category"] if meta["category"] else dir_category.replace("_", " ")
    time_complexity = meta["time_complexity"]
    space_complexity = meta["space_complexity"]
    formula_used = meta["formula_used"]

    return {
        "problem_id": problem_id,
        "problem_name": problem_name,
        "title": problem_name,
        "category": category,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "formula_used": formula_used,
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


def escape_table_cell(text: str) -> str:
    """Escapes pipes in table cells to preserve markdown table formatting."""
    return text.replace("|", "\\|").replace("\n", " ")


def generate_readme(catalog: Dict[str, Any], repo_root: Path) -> str:
    """
    Generates a README.md formatted exactly like the leetcode-stack specification.
    Includes Markdown tables grouped by directory/topic:
    Columns: Problem, Category, Time, Space, Formula/Notes.
    """
    lines = [README_PREFIX.rstrip(), ""]

    categories = catalog.get("categories", {})
    for folder_name in sorted(categories.keys()):
        problems = categories[folder_name]
        display_topic = folder_name.replace("_", " ")
        lines.append(f"### {display_topic}")
        lines.append("")
        lines.append("| Problem | Category | Time | Space | Formula/Notes |")
        lines.append("|---|---|---|---|---|")
        for p in problems:
            prob_link = f"[{p['problem_name']}]({p['file']})"
            cat_str = escape_table_cell(p["category"])
            time_str = escape_table_cell(p["time_complexity"])
            space_str = escape_table_cell(p["space_complexity"])
            formula_str = escape_table_cell(p["formula_used"])
            lines.append(f"| {prob_link} | {cat_str} | {time_str} | {space_str} | {formula_str} |")
        lines.append("")

    lines.append(README_SNIPPETS.strip())
    lines.append("")
    lines.append(README_SUFFIX.strip())
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    index_dir = repo_root / "index"
    index_file = index_dir / "index.json"
    readme_file = repo_root / "README.md"
    index_readme_file = index_dir / "README.md"

    index_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}  Algorithmic Repository Indexer (Go & C++)         {COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_CYAN}===================================================={COLOR_RESET}")
    print(f"Scanning root: {COLOR_DIM}{repo_root}{COLOR_RESET}\n")

    catalog = scan_and_index(repo_root)

    # 1. Write index/index.json
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    # 2. Generate and write root README.md
    readme_content = generate_readme(catalog, repo_root)
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 3. Also generate index/README.md for index package parity
    index_readme_content = "# Algorithmic Repository Index\n\n"
    index_readme_content += "Automated problem index categorized by algorithmic taxonomy.\n\n"
    for folder_name in sorted(catalog.get("categories", {}).keys()):
        display_topic = folder_name.replace("_", " ")
        index_readme_content += f"## {display_topic}\n\n"
        index_readme_content += "| Problem | Category | Time | Space | Formula/Notes |\n"
        index_readme_content += "|---|---|---|---|---|\n"
        for p in catalog["categories"][folder_name]:
            prob_link = f"[{p['problem_name']}](../{p['file']})"
            index_readme_content += f"| {prob_link} | {escape_table_cell(p['category'])} | {escape_table_cell(p['time_complexity'])} | {escape_table_cell(p['space_complexity'])} | {escape_table_cell(p['formula_used'])} |\n"
        index_readme_content += "\n"
    with open(index_readme_file, "w", encoding="utf-8") as f:
        f.write(index_readme_content)

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
            formula_note = f" (Formula: {item['formula_used'][:40]}...)" if item['formula_used'] else ""
            print(f"    - {COLOR_BOLD}{item['problem_id']}{COLOR_RESET}: {item['problem_name']} ({item['language']}){complexity_str}{formula_note} {tests_badge}")

    print(f"\n{COLOR_BOLD}{COLOR_GREEN}Index written successfully to:{COLOR_RESET} {index_file}")
    print(f"{COLOR_BOLD}{COLOR_GREEN}README generated successfully at:{COLOR_RESET} {readme_file}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
