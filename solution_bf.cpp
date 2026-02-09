#include <iostream>
#include <vector>
#include <cstdint>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;

    vector<int> scroll;
    scroll.reserve(q);

    for (int k = 0; k < q; k++) {
        int type;
        cin >> type;

        if (type == 1) {
            int x;
            cin >> x;
            scroll.push_back(x);
        } else if (type == 2) {
            int x, y;
            cin >> x >> y;
            // Naively scan entire scroll and replace x with y.
            for (size_t i = 0; i < scroll.size(); i++) {
                if (scroll[i] == x) {
                    scroll[i] = y;
                }
            }
        } else if (type == 3) {
            int x, y;
            cin >> x >> y;
            // Must be simultaneous: swap x and y wherever they occur.
            for (size_t i = 0; i < scroll.size(); i++) {
                if (scroll[i] == x) {
                    scroll[i] = y;
                } else if (scroll[i] == y) {
                    scroll[i] = x;
                }
            }
        }
    }

    // Output final scroll
    for (size_t i = 0; i < scroll.size(); i++) {
        if (i) cout << ' ';
        cout << scroll[i];
    }
    cout << "\n";

    // Naive inversion count: O(n^2)
    int64_t inversionCount = 0;
    for (size_t i = 0; i < scroll.size(); i++) {
        for (size_t j = i + 1; j < scroll.size(); j++) {
            if (scroll[i] > scroll[j]) {
                inversionCount++;
            }
        }
    }

    cout << inversionCount << "\n";
    return 0;
}