package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n int
	fmt.Fscan(in, &n)
	var s string
	fmt.Fscan(in, &s)

	// Count number of 1s (elements Souvlakity owns)
	c := strings.Count(s, "1")

	if c == 1 {
		fmt.Fprintln(out, 0)
	} else if c == 2 {
		fmt.Fprintln(out, 1)
	} else {
		// If c >= 3, he never gives away the extremes. 
		// Score is exactly the initial range.
		first := strings.Index(s, "1")
		last := strings.LastIndex(s, "1")
		fmt.Fprintln(out, last-first)
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