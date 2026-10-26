package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var x, y, k int64
	fmt.Fscan(in, &x, &y, &k)

	// FORMULA & CALCULATION:
	// We need to sum (y+i) % (x+i) for i from 0 to k-1.
	// Since (y+i) = (x+i) + (y-x), let d = y - x.
	// Therefore, (y+i) % (x+i) == d % (x+i).
	// Loop through months. When our divisor (x+i) becomes strictly greater than d,
	// the modulo d % (x+i) will always just be d.
	// At that point, we mathematically calculate the rest to bypass the O(k) TLE trap.

	d := y - x
	var total int64 = 0

	for i := int64(0); i < k; i++ {
		cur := x + i
		if cur > d {
			// If current divisor is greater than d, all remaining months yield exactly 'd'
			remMonths := k - i
			total += remMonths * d
			break
		}
		total += d % cur
	}

	fmt.Fprintln(out, total)
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
		in = bufio.NewReader(os.Stdin)
		out = bufio.NewWriter(os.Stdout)
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