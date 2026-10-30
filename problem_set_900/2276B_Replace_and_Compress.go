/*
{
    "problem_name": "Replace and Compress",
    "category": "Strings / Observations",
    "time_complexity": "O(N) -> Single pass string scan. Zero actual compression simulations.",
    "space_complexity": "O(N) -> To store the string in memory, optimal for 3*10^5 constraints."
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var s string
	fmt.Fscan(in, &s)
	n := len(s)

	canIncrease := 0
	canDecrease := 0

	// Loop from 1 to n-2 because we cannot change the first and last characters
	for i := 1; i < n-1; i++ {
		// Check for 3 consecutive identical characters (Length + 2)
		if s[i-1] == s[i] && s[i] == s[i+1] {
			canIncrease = 1
		}
		// Check for an isolated character surrounded by opposite characters (Length - 2)
		if s[i-1] != s[i] && s[i] != s[i+1] {
			canDecrease = 1
		}
		
		// Early exit if both possibilities are already found
		if canIncrease == 1 && canDecrease == 1 {
			break
		}
	}

	// Total unique strings = base string (1) + can increase (0 or 1) + can decrease (0 or 1)
	fmt.Fprintln(out, 1 + canIncrease + canDecrease)
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
		// Use a large buffer for fast I/O throughput
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