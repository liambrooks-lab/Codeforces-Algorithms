# Algorithmic Repository Index

Automated problem index categorized by algorithmic taxonomy.

## Game Theory

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Hey It's Me Souvlakity](../Game_Theory/2261A_Souvlakity.go) | Game Theory | O(N) | O(1) | Binary string ownership range evaluation; score = lastIndex('1') - firstIndex('1') for count >= 3, with base states for count <= 2 |
| [I Know About a Million Things](../Game_Theory/2261C_i_know_about_a_million_things.go) | Game Theory | O(N) -> Pure byte-level custom parser. Zero reflection overhead. | O(1) -> Absolute bare-metal. Slices bypassed entirely. | Parity state-space reduction; terminal losing states: (evens == 0 && odds == 3) \|\| (evens == 1 && odds == 1) |

## Math

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Monocarp and Projects](../Math/2260B_monocarp_and_projects.go) | Math | O(min(k, y - x)) | O(1) | (y + i) % (x + i) == (y - x) % (x + i); early termination with remaining * (y - x) when x + i > y - x |
| [KiaKio](../Math/2269B_KiaKio.go) | Math | O(N) | O(N) | Sum of digit squares cycle convergence followed by combinatorics sum(c * (c - 1) / 2) over equivalence classes |
| [In Search of Convenience](../Math/2275A_in_search_of_convenience.go) | Math | O(1) | O(1) | (x - x0)^2 + (y - y0)^2 = R^2; setting y = y0 simplifies to (x0 + R, y0) |
| [Perfect Sandwiches](../Math/2276A_Perfect_Sandwiches.go) | Math | O(1) -> Pure mathematical derivation, zero loops. | O(1) -> Only primitive variables used. | min(b, a - b) if a > b else -1 |

## Matrices

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Min Matrices](../Matrices/2263B_Min_Matrices.go) | Matrices | O(N^2) | O(1) | Constructive matrix filling: diagonal mins i+1 for i < x where x = 2n - k, row/col mins for >= x, and sequential filler |

## Sorting

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Unrequited Love](../Sorting/2275C_Unrequited_Love.go) | Sorting | O(N log N) -> Standard sorting for frequency counting. Simple, clean, and cache-friendly. | O(N) -> Single slice allocation, no map overhead. | Triad mapping v[i] = a[i] + a[i+2] - a[i+4], sorted frequency count sum(c * (c - 1) / 2) minus overlapping distance-2 and distance-4 pairs |

## Stacks

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Did Not Go to Print](../Stacks/2275B_did_not_go_to_print.go) | Stacks | O(N) | O(N) | Monotonic stack simulation for document cancellation ('1' push, '2' pop/print, '3' print) |

## Strings

| Problem | Category | Time | Space | Formula/Notes |
|---|---|---|---|---|
| [Replace and Compress](../Strings/2276B_Replace_and_Compress.go) | Strings | O(N) -> Single pass string scan. Zero actual compression simulations. | O(N) -> To store the string in memory, optimal for 3*10^5 constraints. | String invariance scan: total unique lengths = 1 + canIncrease (if s[i-1]==s[i]==s[i+1]) + canDecrease (if s[i-1]!=s[i]!=s[i+1]) |

