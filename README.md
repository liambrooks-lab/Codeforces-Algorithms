# leetcode-stack

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

### Game Theory

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Hey It's Me Souvlakity](Game_Theory/2261A_Souvlakity.go) | Game Theory | O(N) | O(1) | Binary string ownership range evaluation; score = lastIndex('1') - firstIndex('1') for count >= 3, with base states for count <= 2 |
| [I Know About a Million Things](Game_Theory/2261C_i_know_about_a_million_things.go) | Game Theory | O(N) -> Pure byte-level custom parser. Zero reflection overhead. | O(1) -> Absolute bare-metal. Slices bypassed entirely. | Parity state-space reduction; terminal losing states: (evens == 0 && odds == 3) \|\| (evens == 1 && odds == 1) |

### Math

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Monocarp and Projects](Math/2260B_monocarp_and_projects.go) | Math | O(min(k, y - x)) | O(1) | (y + i) % (x + i) == (y - x) % (x + i); early termination with remaining * (y - x) when x + i > y - x |
| [KiaKio](Math/2269B_KiaKio.go) | Math | O(N) | O(N) | Sum of digit squares cycle convergence followed by combinatorics sum(c * (c - 1) / 2) over equivalence classes |
| [In Search of Convenience](Math/2275A_in_search_of_convenience.go) | Math | O(1) | O(1) | (x - x0)^2 + (y - y0)^2 = R^2; setting y = y0 simplifies to (x0 + R, y0) |
| [Perfect Sandwiches](Math/2276A_Perfect_Sandwiches.go) | Math | O(1) -> Pure mathematical derivation, zero loops. | O(1) -> Only primitive variables used. | min(b, a - b) if a > b else -1 |

### Matrices

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Min Matrices](Matrices/2263B_Min_Matrices.go) | Matrices | O(N^2) | O(1) | Constructive matrix filling: diagonal mins i+1 for i < x where x = 2n - k, row/col mins for >= x, and sequential filler |

### Sorting

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Unrequited Love](Sorting/2275C_Unrequited_Love.go) | Sorting | O(N log N) -> Standard sorting for frequency counting. Simple, clean, and cache-friendly. | O(N) -> Single slice allocation, no map overhead. | Triad mapping v[i] = a[i] + a[i+2] - a[i+4], sorted frequency count sum(c * (c - 1) / 2) minus overlapping distance-2 and distance-4 pairs |

### Stacks

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Did Not Go to Print](Stacks/2275B_did_not_go_to_print.go) | Stacks | O(N) | O(N) | Monotonic stack simulation for document cancellation ('1' push, '2' pop/print, '3' print) |

### Strings

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Replace and Compress](Strings/2276B_Replace_and_Compress.go) | Strings | O(N) -> Single pass string scan. Zero actual compression simulations. | O(N) -> To store the string in memory, optimal for 3*10^5 constraints. | String invariance scan: total unique lengths = 1 + canIncrease (if s[i-1]==s[i]==s[i+1]) + canDecrease (if s[i-1]!=s[i]!=s[i+1]) |

### Snippets

**Arrays &mdash; In-Place Two-Pointer Partitioning:**
```go
// Partitions slice in-place around a predicate in O(N) time and O(1) auxiliary space
func partition(nums []int, pivot int) int {
	left := 0
	for right := 0; right < len(nums); right++ {
		if nums[right] < pivot {
			nums[left], nums[right] = nums[right], nums[left]
			left++
		}
	}
	return left
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
	lowestBit = n & -n                      // Isolate lowest set bit
	isPowerOfTwo = n > 0 && (n&(n-1)) == 0 // Check power of two
	clearedBit = n & ^(1 << mask)          // Clear specific bit at mask position
	return
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
	n := len(cost)
	if n <= 1 {
		return 0
	}
	prev2, prev1 := 0, 0
	for i := 2; i <= n; i++ {
		c1 := prev1 + cost[i-1]
		c2 := prev2 + cost[i-2]
		current := c1
		if c2 < current {
			current = c2
		}
		prev2, prev1 = prev1, current
	}
	return prev1
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
	slow, fast := head, head
	for fast != nil && fast.Next != nil {
		slow = slow.Next
		fast = fast.Next.Next
		if slow == fast {
			return true
		}
	}
	return false
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
	n := len(nums)
	prefix := make([]int, n+1)
	for i := 0; i < n; i++ {
		prefix[i+1] = prefix[i] + nums[i]
	}
	return prefix // Range [i, j] sum is prefix[j+1] - prefix[i]
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
	lastPos := make(map[byte]int)
	maxLen, left := 0, 0
	for right := 0; right < len(s); right++ {
		if prev, exists := lastPos[s[right]]; exists && prev >= left {
			left = prev + 1
		}
	lastPos[s[right]] = right
	curLen := right - left + 1
	if curLen > maxLen {
		maxLen = curLen
	}
	}
	return maxLen
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
	n := len(nums)
	res := make([]int, n)
	for i := range res {
		res[i] = -1
	}
	stack := make([]int, 0, n) // Monotonic decreasing index stack

	for i := 0; i < n; i++ {
		for len(stack) > 0 && nums[i] > nums[stack[len(stack)-1]] {
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			res[top] = i
		}
		stack = append(stack, i)
	}
	return res
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
	left, right := 0, len(height)-1
	maxArea := 0
	for left < right {
		hL, hR := height[left], height[right]
		h := hL
		if hR < h {
			h = hR
		}
		area := h * (right - left)
		if area > maxArea {
			maxArea = area
		}
		if hL < hR {
			for left < right && height[left] <= hL {
				left++
			}
		} else {
			for left < right && height[right] <= hR {
				right--
			}
		}
	}
	return maxArea
}
```

---

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
