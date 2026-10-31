/*
{
    "problem_name": "Unrequited Love",
    "category": "Combinatorics / Sorting",
    "time_complexity": "O(N log N) -> Standard sorting for frequency counting. Simple, clean, and cache-friendly.",
    "space_complexity": "O(N) -> Single slice allocation, no map overhead."
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n int
	fmt.Fscan(in, &n)
	
	a := make([]int, n)
	for i := 0; i < n; i++ {
		fmt.Fscan(in, &a[i])
	}

	m := n - 4
	v := make([]int, m)
	for i := 0; i < m; i++ {
		// Triad value formula: a_x + a_{x+2} - a_{x+4}
		v[i] = a[i] + a[i+2] - a[i+4]
	}

	// Make a copy to sort, keeping the original 'v' intact for distance checking
	vSorted := make([]int, m)
	copy(vSorted, v)
	sort.Ints(vSorted)

	var ans int64 = 0

	// 1. Count ALL globally matching pairs using the sorted array
	for i := 0; i < m; {
		j := i
		for j < m && vSorted[j] == vSorted[i] {
			j++
		}
		count := int64(j - i)
		ans += count * (count - 1) / 2
		i = j
	}

	// 2. Subtract overlapping pairs directly from the original sequence.
	// Only triads at exactly distance 2 or 4 share keys.
	for i := 0; i < m-2; i++ {
		if v[i] == v[i+2] {
			ans--
		}
	}
	for i := 0; i < m-4; i++ {
		if v[i] == v[i+4] {
			ans--
		}
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
		// Fast buffered I/O without the risky manual byte parsing
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