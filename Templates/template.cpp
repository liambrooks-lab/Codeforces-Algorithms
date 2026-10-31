/*
{
    "problem_name": "...",
    "category": "...",
    "time_complexity": "...",
    "space_complexity": "...",
    "formula_used": "..."
}
*/
#include <bits/stdc++.h>
using namespace std;

void solve() {
    // Solution logic here
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Local environment check: redirect standard streams if input.txt is present
    ifstream fin("input.txt");
    if (fin.good()) {
        fin.close();
        freopen("input.txt", "r", stdin);
        freopen("output.txt", "w", stdout);
    }

    int t = 1;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}
