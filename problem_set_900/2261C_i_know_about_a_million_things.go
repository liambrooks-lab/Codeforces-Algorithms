/*
{
    "problem_name": "I Know About a Million Things",
    "category": "Game Theory / Math",
    "time_complexity": "O(N) -> Pure byte-level custom parser. Zero reflection overhead.",
    "space_complexity": "O(1) -> Absolute bare-metal. Slices bypassed entirely."
}
*/
package main

import (
	"bufio"
	"os"
)

// Ultra-fast byte-level integer parser to obliterate the 406ms latency
func readInt(in *bufio.Reader) int {
	var res int
	var c byte
	var err error
	
	// Skip whitespaces
	for {
		c, err = in.ReadByte()
		if err != nil || c > 32 {
			break
		}
	}
	if err != nil {
		return 0
	}
	
	// Parse integer digits directly
	for {
		res = res*10 + int(c-'0')
		c, err = in.ReadByte()
		if err != nil || c <= 32 {
			break
		}
	}
	return res
}

func solve(in *bufio.Reader, out *bufio.Writer) {
	n := readInt(in)

	odds := 0
	evens := 0

	// Read 10^6 elements directly from buffer, bypassing any array allocations
	for i := 0; i < n; i++ {
		x := readInt(in)
		if x%2 != 0 {
			odds++
		} else {
			evens++
		}
	}

	// FLAWLESS GAME THEORY: 
	// The ONLY two losing states in the entire game logic
	if (evens == 0 && odds == 3) || (evens == 1 && odds == 1) {
		out.WriteString("Larpity\n")
	} else {
		out.WriteString("Moggity\n")
	}
}

func main() {
	var inFile *os.File
	if _, err := os.Stat("input.txt"); err == nil {
		inFile, _ = os.Open("input.txt")
		defer inFile.Close()
	} else {
		inFile = os.Stdin
	}

	// Using a massive 64KB read buffer for maximum I/O pipeline throughput
	in := bufio.NewReaderSize(inFile, 65536)
	
	var out *bufio.Writer
	if _, err := os.Stat("input.txt"); err == nil {
		outFile, _ := os.Create("output.txt")
		defer outFile.Close()
		out = bufio.NewWriter(outFile)
	} else {
		out = bufio.NewWriter(os.Stdout)
	}
	defer out.Flush()

	t := readInt(in)
	for i := 0; i < t; i++ {
		solve(in, out)
	}
}