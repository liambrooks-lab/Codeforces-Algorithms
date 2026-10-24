package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	var n int
	fmt.Fscan(in, &n)
	var s string
	fmt.Fscan(in, &s)

	// Pre-allocate slice capacities to prevent dynamic memory re-allocations
	stack := make([]int, 0, n)
	printed := make([]bool, n+1)

	// 1-based indexing sequence run
	for i := 1; i <= n; i++ {
		ch := s[i-1]
		if ch == '1' {
			stack = append(stack, i)
		} else if ch == '2' {
			if len(stack) > 0 {
				top := stack[len(stack)-1]
				stack = stack[:len(stack)-1] // Pop
				printed[top] = true
			} else {
				printed[i] = true
			}
		} else if ch == '3' {
			printed[i] = true
		}
	}

	// Count unprinted documents first to avoid allocating extra memory
	count := 0
	for i := 1; i <= n; i++ {
		if !printed[i] {
			count++
		}
	}

	// Fast printing without creating intermediate string slices/arrays
	fmt.Fprintln(out, count)
	if count > 0 {
		first := true
		for i := 1; i <= n; i++ {
			if !printed[i] {
				if !first {
					out.WriteByte(' ')
				}
				out.WriteString(strconv.Itoa(i))
				first = false
			}
		}
	}
	out.WriteByte('\n')
}

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	var t int
	fmt.Fscan(in, &t)
	for tc := 0; tc < t; tc++ {
		solve(in, out)
	}
}