/*
{
    "problem_name": "The Projections of Paco",
    "category": "Math",
    "time_complexity": "O(N)",
    "space_complexity": "O(1)",
    "formula_used": "pos = 2 * a_i - pos; solve for initial p giving final pos = 0"
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

	// We calculate the effect of all a_i reflections assuming starting pos is 0
	// Effectively calculating the constant term in the reflection equation
	pos := 0
	for i := 0; i < n; i++ {
		var a int
		fmt.Fscan(in, &a)
		pos = 2*a - pos
	}

	// The total number of reflections is n + 1 (the first one is p)
	// If (n+1) is even (meaning n is odd): final_pos = -2p + pos
	// We want final_pos = 0, so 2p = pos  => p = pos / 2
	
	// If (n+1) is odd (meaning n is even): final_pos = 2p + pos
	// We want final_pos = 0, so 2p = -pos => p = -pos / 2

	var p int
	if n%2 != 0 { // n is odd -> n+1 is even
		p = pos / 2
	} else {      // n is even -> n+1 is odd
		p = -pos / 2
	}

	fmt.Fprintln(out, p)
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
		// Buffered I/O is fast enough for 10^5 constraints
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