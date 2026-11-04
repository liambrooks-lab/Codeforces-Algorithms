/*
{
    "problem_name": "Robot Odd Moves",
    "category": "Math",
    "time_complexity": "O(1) -> Pure mathematical parity evaluation.",
    "space_complexity": "O(1) -> Bare-metal constant space.",
    "formula_used": "if b > a+1 { -1 } else if a%2 == b%2 { a } else { a+1 }"
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var a, b int
	fmt.Fscan(in, &a, &b)

	// If target Y is completely out of reach for X = a
	if b > a+1 {
		fmt.Fprintln(out, -1)
	} else if (a % 2) == (b % 2) {
		// Parity matches, reachable precisely at the end of operation 'a'
		fmt.Fprintln(out, a)
	} else {
		// Parity mismatch, reachable mid-way through operation 'a+1'
		fmt.Fprintln(out, a+1)
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
		// O(1) logic doesn't strictly need massive buffers, but keeping it standard for the repo
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