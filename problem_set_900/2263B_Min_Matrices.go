package main

import (
	"bufio"
	"os"
	"strconv"
)

func readInt(in *bufio.Reader) int {
	n := 0
	c, _ := in.ReadByte()
	for c == ' ' || c == '\n' || c == '\r' || c == '\t' {
		c, _ = in.ReadByte()
	}
	for c >= '0' && c <= '9' {
		n = n*10 + int(c-'0')
		c, _ = in.ReadByte()
	}
	return n
}

func solve(in *bufio.Reader, out *bufio.Writer) {
	n := readInt(in)
	k := readInt(in)

	if k < n || k > 2*n-1 {
		out.WriteString("-1\n")
		return
	}

	x := 2*n - k
	curr := k + 1 // first "free" number (x + 2*(n-x) + 1)
	var scratch [20]byte

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			var v int
			switch {
			case i == j && i < x: // diagonal mins
				v = i + 1
			case j == 0 && i >= x: // remaining row mins
				v = i + 1
			case i == 0 && j >= x: // remaining col mins
				v = n + 1 + j - x
			default: // filler, row-major
				v = curr
				curr++
			}
			if j > 0 {
				out.WriteByte(' ')
			}
			out.Write(strconv.AppendInt(scratch[:0], int64(v), 10))
		}
		out.WriteByte('\n')
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
		in = bufio.NewReaderSize(inFile, 1<<20)
		out = bufio.NewWriterSize(outFile, 1<<20)
	} else {
		in = bufio.NewReaderSize(os.Stdin, 1<<20)
		out = bufio.NewWriterSize(os.Stdout, 1<<20)
	}
	defer out.Flush()

	t := readInt(in)
	for ; t > 0; t-- {
		solve(in, out)
	}
}