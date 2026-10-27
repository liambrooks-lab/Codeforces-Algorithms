/*
{
    "problem_name": "KiaKio",
    "category": "problem_set_800",
    "time_complexity": "O(n)",
    "space_complexity": "O(n)"
}
*/

package main

import (
	"bufio"
	"fmt"
	"os"
)

// Helper function: Number ke digits ke squares ka sum nikalne ke liye
func getNext(x int) int {
	sum := 0
	for x > 0 {
		d := x % 10
		sum += d * d
		x /= 10
	}
	return sum
}

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n int
	if _, err := fmt.Fscan(in, &n); err != nil {
		return
	}

	freq := make(map[int]int64)

	for i := 0; i < n; i++ {
		var current int
		fmt.Fscan(in, &current)

		// Har number ko 100 times simulate kar rahe hain
		// 100 steps ke baad 100% guarantee hai ki number apni permanent cycle mein set ho jayega
		for step := 0; step < 100; step++ {
			current = getNext(current)
		}

		// Permanent state ki frequency store kar lo
		freq[current]++
	}

	var ans int64
	// Combinatorics: Har frequency group mein se pairs nikalna (n * (n-1) / 2)
	for _, count := range freq {
		ans += (count * (count - 1)) / 2
	}

	fmt.Fprintln(out, ans)
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
