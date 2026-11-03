/*
{
    "problem_name": "Prefix",
    "category": "Math / Greedy",
    "time_complexity": "O(N) -> State space collapse to tracking min/max prefix sums",
    "space_complexity": "O(1) -> Bare-metal constant space",
    "formula_used": "s_new ∈ {a_i, s + a_i, 2s + a_i}; track only min_s and max_s"
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func max(a, b int64) int64 {
	if a > b {
		return a
	}
	return b
}

func min(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n int
	fmt.Fscan(in, &n)

	var a int64
	fmt.Fscan(in, &a)

	ans := a
	minS := a
	maxS := a

	for i := 1; i < n; i++ {
		fmt.Fscan(in, &a)

		// Test the newly generated elements using our extreme prefix sums
		e1 := a - minS
		e2 := a - maxS
		e3 := a
		e4 := a + minS
		e5 := a + maxS

		// Update our global maximum element found so far
		ans = max(ans, max(e1, max(e2, max(e3, max(e4, e5)))))

		// Generate all possible new prefix sums from our current extremes
		// s_new ∈ {a, s + a, 2s + a}
		s1 := a
		s2 := minS + a
		s3 := 2*minS + a
		s4 := maxS + a
		s5 := 2*maxS + a

		// Collapse the state space back into just the new extremes
		minS = min(s1, min(s2, min(s3, min(s4, s5))))
		maxS = max(s1, max(s2, max(s3, max(s4, s5))))
	}

	fmt.Fprintln(out, ans)
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
		// Standard buffered I/O is blazing fast for N <= 50
		in = bufio.NewReaderSize(os.Stdin, 65536)
		out = bufio.NewWriterSize(os.Stdout, 65536)
	}
	defer out.Flush()

	var t int
	if _, err := fmt.Fscan(in, &t); err != nil {
		return
	}
	for tc := 0; tc < t; tc++ {
		solve(in, out)
	}
}