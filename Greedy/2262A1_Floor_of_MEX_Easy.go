/*
	{
	    "problem_name": "Floor of MEX (Easy Version)",
	    "category": "Greedy / Constructive Algorithms",
	    "time_complexity": "O(N) -> Constructive maximal subset using difference array.",
	    "space_complexity": "O(N) -> Single difference array allocation.",
	    "formula_used": "diff[a_k * k]++, diff[min(n, (a_k+1)*k)]--; Maximal subset bypasses forbidden ranges"
	}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n int
	fmt.Fscan(in, &n)

	// Difference array to mark forbidden ranges in O(1) time per operation
	diff := make([]int, n+1)

	for k := 1; k <= n; k++ {
		var ak int
		fmt.Fscan(in, &ak)

		// Calculate the forbidden range [L, R] for the current k
		L := ak * k
		if L >= n {
			continue // Entire forbidden range is outside our domain [0, n-1]
		}

		R := (ak+1)*k - 1
		if R >= n {
			R = n - 1
		}

		// Mark the range [L, R] as forbidden using difference array technique
		diff[L]++
		diff[R+1]--
	}

	ans := make([]int, 0)
	currentOverlaps := 0

	// Sweep through the difference array to build the maximal valid subset
	for i := 0; i < n; i++ {
		currentOverlaps += diff[i]
		if currentOverlaps == 0 {
			ans = append(ans, i)
		}
	}

	// Output the size of the subset and the elements
	fmt.Fprintln(out, len(ans))
	for i, val := range ans {
		if i > 0 {
			fmt.Fprint(out, " ")
		}
		fmt.Fprint(out, val)
	}
	fmt.Fprintln(out)
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
		// Buffered I/O is crucial for O(N) performance on 10^5 constraints
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
