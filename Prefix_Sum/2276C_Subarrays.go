/*
{
    "problem_name": "Subarrays",
    "category": "Prefix Sum / Math",
    "time_complexity": "O(N) -> Single pass with delayed mapping.",
    "space_complexity": "O(N) -> Array allocations for prefixes and tracking counts.",
    "formula_used": "prefix_sum[r] % k == prefix_sum[l-1] % k with a sliding delayed map (delay = k)"
}
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n, k int
	fmt.Fscan(in, &n, &k)

	// Array to store the prefix sums modulo k
	// prefix[0] is explicitly set to 0 to handle subarrays starting at index 1
	prefix := make([]int, n+1)
	prefix[0] = 0

	for i := 1; i <= n; i++ {
		var a int
		fmt.Fscan(in, &a)
		// Calculate continuous running prefix sum mod k
		prefix[i] = (prefix[i-1] + (a % k)) % k
	}

	// This map tracks the frequencies of the remainders we have seen so far
	// We use an array instead of a Go map since the values are just remainders mod k
	countMap := make([]int, k)
	
	var totalValidSubarrays int64 = 0

	// We iterate through the array. 
	// At index r, we can only form valid subarrays with previous indices <= r - k - 1
	// So, we add the prefix remainder at (r - k - 1) to our countMap just before checking
	for r := k + 1; r <= n; r++ {
		// Add the remainder that just entered our valid delayed window
		validLeftIndex := r - k - 1
		countMap[prefix[validLeftIndex]]++

		// Any matching remainder in the map represents a valid subarray ending at r
		totalValidSubarrays += int64(countMap[prefix[r]])
	}

	fmt.Fprintln(out, totalValidSubarrays)
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