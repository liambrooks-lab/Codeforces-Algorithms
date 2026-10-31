/*
{
    "problem_name": "Perfect Sandwiches",
    "category": "Math",
    "time_complexity": "O(1) -> Pure mathematical derivation, zero loops.",
    "space_complexity": "O(1) -> Only primitive variables used.",
    "formula_used": "min(b, a - b) if a > b else -1"
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

// min returns the smaller of two integers
func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func solve(in *bufio.Reader, out *bufio.Writer) {
	var a, b int
	fmt.Fscan(in, &a, &b)

	// If cheese is less than or equal to sausage, it's mathematically impossible
	if a <= b {
		fmt.Fprintln(out, -1)
		return
	}

	// The maximum sandwiches is constrained by either total sausages (b) 
	// or the surplus of cheese over sausages (a - b)
	ans := min(b, a-b)
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