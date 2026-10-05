#include <bits/stdc++.h>
using namespace std;

// Helper function: Number ke digits ke squares ka sum nikalne ke liye
int getNext(int x) {
    int sum = 0;
    while (x > 0) {
        int d = x % 10;
        sum += d * d;
        x /= 10;
    }
    return sum;
}

void solve() {
    int n;
    cin >> n;
    
    map<int, long long> freq;
    
    for (int i = 0; i < n; i++) {
        int current;
        cin >> current;
        
        // Har number ko 100 times simulate kar rahe hain
        // 100 steps ke baad 100% guarantee hai ki number apni permanent cycle mein set ho jayega
        for (int step = 0; step < 100; step++) {
            current = getNext(current);
        }
        
        // Permanent state ki frequency store kar lo
        freq[current]++;
    }
    
    long long ans = 0;
    // Combinatorics: Har frequency group mein se pairs nikalna (n * (n-1) / 2)
// Combinatorics: Har frequency group mein se pairs nikalna (n * (n-1) / 2)
for (auto const& p : freq) {
    long long count = p.second;
    ans += (count * (count - 1)) / 2;
}
    
    cout << ans << "\n";
}

int main() {
    // Tera C++ Fast I/O magic
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int t;
    cin >> t; 
    while (t--) {
        solve();
    }
    return 0;
}