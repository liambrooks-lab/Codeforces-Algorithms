/*
{
    "problem_name": "Rumb Needs a Hand",
    "category": "Two Pointers",
    "time_complexity": "O(N) -> Single inward pass using two pointers.",
    "space_complexity": "O(N) -> Array storage, O(1) auxiliary space.",
    "formula_used": "Symmetric matching for misplaced elements: p[left] == right && p[right] == left"
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

	// 1-based indexing for direct value-to-index comparison
	p := make([]int, n+1)
	for i := 1; i <= n; i++ {
		fmt.Fscan(in, &p[i])
	}

	left := 1
	right := n
	possible := true

	for left < right {
		// Skip correctly placed elements from the left
		for left < right && p[left] == left {
			left++
		}
		// Skip correctly placed elements from the right
		for left < right && p[right] == right {
			right--
		}

		if left >= right {
			break // All remaining elements are perfectly placed
		}

		// The misplaced pair MUST cross-match their target indices
		if p[left] != right || p[right] != left {
			possible = false
			break
		}

		// Move inwards to check the next pair of misplaced elements
		left++
		right--
	}

	if possible {
		fmt.Fprintln(out, "YES")
	} else {
		fmt.Fprintln(out, "NO")
	}
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
		// Buffered I/O for safety on max constraints
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
