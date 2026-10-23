package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	// Solution logic here
}

func main() {
	// Local environment check: redirect I/O if input.txt exists
	if _, err := os.Stat("input.txt"); err == nil {
		inFile, err := os.Open("input.txt")
		if err == nil {
			os.Stdin = inFile
			defer inFile.Close()
		}

		outFile, err := os.Create("output.txt")
		if err == nil {
			os.Stdout = outFile
			defer outFile.Close()
		}
	}

	// Fast I/O
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	var t int
	if _, err := fmt.Fscan(in, &t); err != nil {
		return
	}

	for i := 0; i < t; i++ {
		solve(in, out)
	}
}
