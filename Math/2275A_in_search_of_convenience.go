/*
{
    "problem_name": "In Search of Convenience",
    "category": "Math",
    "time_complexity": "O(1)",
    "space_complexity": "O(1)",
    "formula_used": "(x - x0)^2 + (y - y0)^2 = R^2; setting y = y0 simplifies to (x0 + R, y0)"
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var x0, y0, r int
	fmt.Fscan(in, &x0, &y0, &r)

	// FORMULA & CALCULATION:
	// We need any point on (x - x0)^2 + (y - y0)^2 = R^2.
	// By setting y = y0, the equation simplifies to (x - x0)^2 = R^2.
	// Taking the square root: x - x0 = R => x = x0 + R.
	// Since R is an integer, x will always be a valid integer coordinate.
	// This entirely bypasses any loops, arrays, or float calculations.
	
	fmt.Fprintln(out, x0+r, y0)
}

func main() {
	var in *bufio.Reader
	var out *bufio.Writer

	// Auto-detect local testing environment
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
