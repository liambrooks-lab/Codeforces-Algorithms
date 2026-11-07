/*
	{
	    "problem_name": "K Is Important",
	    "category": "Greedy / Math",
	    "time_complexity": "O(N) -> Pure mathematical reduction of the state space.",
	    "space_complexity": "O(N) -> Array storage, O(1) auxiliary space.",
	    "formula_used": "ops = min(k-1, n-k+1); score = sum(max(pairs)) + sum(middle_removals_if_any)"
	}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

// Helper function for O(1) bare-metal max evaluation
func max(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n, k int
	fmt.Fscan(in, &n, &k)

	// 1-based indexing to align perfectly with the formula
	a := make([]int64, n+1)
	for i := 1; i <= n; i++ {
		fmt.Fscan(in, &a[i])
	}

	// Calculate the maximum number of symmetric pairs we can process
	ops := k - 1
	if n-k+1 < ops {
		ops = n - k + 1
	}

	var maxScore int64 = 0

	// 1. Process the symmetric pairs from the outer edges
	// We are guaranteed to be able to pick EXACTLY the max of each pair
	for c := 1; c <= ops; c++ {
		maxScore += max(a[c], a[n-c+1])
	}

	// 2. The Fix: ONLY add the middle elements if we actually have operations left!
	// If n < 2k - 1, the middle elements are the "immune core" and are NEVER removed.
	// Total operations allowed = n - k + 1. Operations used on pairs = ops.
	if n-k+1 > ops {
		for i := ops + 1; i <= n-ops; i++ {
			maxScore += a[i]
		}
	}

	fmt.Fprintln(out, maxScore)
}

func main() {
	var in *bufio.Reader
	var out *bufio.Writer

	if _, err := os.Stat("input.txt"); err == nil {
		inFile, _ := os.Open("input.txt")
		outFile, _ := os.Create("output.txt")
		defer inFile.Close()
		defer outFile.Close()
		in = bufio.NewReader(inFile)
		out = bufio.NewWriter(outFile)
	} else {
		// Buffered I/O for safety on max constraints (10^5)
		in = bufio.NewReaderSize(os.Stdin, 65536)
		out = bufio.NewWriterSize(os.Stdout, 65536)
	}
	defer out.Flush()

	var t int
	if _, err := fmt.Fscan(in, &t); err != nil {
		return
	}
	for i := 0; i < t; i++ {
		solve(in, out)
	}
}
