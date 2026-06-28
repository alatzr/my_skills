---
name: gdy-cpp-style
description: "Personal OJ solution style for user gdy. Use when Codex writes competitive-programming code, OJ submissions, Chinese problem solutions, or algorithm explanations that should match gdy's historical submissions: mainly C++14/C++11(O2), concise Chinese writeups, short variable names, global arrays, simple functions, and pragmatic contest templates."
---

# Gdy C++ Style

## Core Goal

Write OJ code and题解 like gdy: concise, contest-oriented C++, easy to paste into Hydro/AtCoder/USACO-style judges, with short Chinese explanations and minimal abstraction.

Use this style unless the user explicitly asks for another language/style or the problem requires a library/API style solution.

## Code Defaults

- Prefer C++14-compatible code.
- Start most submissions with:

```cpp
#include<bits/stdc++.h>
using namespace std;
```

- Use `#include <bits/stdc++.h>` with a space only when the surrounding code already uses that spacing.
- Prefer `#define ll long long` for simple long-long needs. `using ll = long long;` is acceptable in more modern-looking AtCoder-style snippets.
- Use `const int N = ... + 10;` for limits, usually global. Common forms: `1e5 + 10`, `2e5 + 10`, `1e6 + 10`, `1010`, `510`.
- Use global arrays and containers for contest data:
  `a[N]`, `b[N]`, `c[N]`, `dp[N]`, `f[N]`, `g[N]`, `st[N]`, `vis[N]`, `dist[N]`, `ans[N]`, `vector<int> adj[N]`.
- Prefer simple `int main()` with braces on the next line:

```cpp
int main()
{
	...
	return 0;
}
```

- Use TAB indentation when writing fresh code. If editing a file that already uses 4 spaces, keep that file's indentation.
- Do not overuse classes, namespaces, lambdas, or generic templates. Add helper functions only when they clarify a standard algorithm.

## Input And Output

- Default to `cin` / `cout`.
- Do not add fast I/O by default for small/medium problems. Add it only when input is large:

```cpp
ios::sync_with_stdio(false);
cin.tie(0);
```

- Use `scanf` / `printf` only when matching an existing scanf-style solution or when performance/formatting is simpler.
- Print `endl` when the style benefits from clarity. For tight loops, prefer `'\n'`.
- For file I/O problems, write explicit `freopen` near the start of `main`:

```cpp
freopen("xxx.in", "r", stdin);
freopen("xxx.out", "w", stdout);
```

- If many file-I/O solutions are expected, this macro is in-style:

```cpp
#define io(x); freopen(x".in", "r", stdin), freopen(x".out", "w", stdout);
```

## Naming

- Use short variable names in loops and formulas: `i`, `j`, `k`, `n`, `m`, `x`, `y`, `l`, `r`, `mid`, `sum`, `ans`, `cnt`, `res`.
- Use conventional algorithm names: `dfs`, `bfs`, `dijkstra`, `find`, `add`, `cmp`, `solve`.
- Use `Node` for small structs and fields like `x`, `y`, `z`, `val`, `d`, `id`.
- Use `PII` or `pair<int,int>` for pair-heavy code. Macros `#define x first` and `#define y second` are acceptable for pair sorting/code brevity.
- Prefer 1-indexing for arrays unless the problem is naturally 0-indexed or uses C++ STL vectors.

## Algorithms And Data Structures

- Implement standard algorithms directly and visibly.
- Prefer arrays over vectors when constraints are known.
- Use `vector<int> adj[N]` or edge arrays for graphs.
- For BFS on grids, use `dx/dy` arrays and either `queue<Node>` or a manual queue array.
- For DFS, use a simple recursive function unless recursion depth is risky.
- For DP, use `dp`, `f`, `g`; initialize with `memset(dp, 0x3f, sizeof dp)` for INF or `memset(..., 0, ...)` for zero.
- Use `const int INF = 0x3f3f3f3f;` or `const int INF = 1e9;`.
- Use `sort(p+1, p+1+n, cmp)` for global arrays and `sort(v.begin(), v.end())` for vectors.
- Keep implementation compact; avoid explanatory helper wrappers that are not needed for the solution.

## Comments

- Use short Chinese comments for non-obvious state meanings or algorithm steps.
- Good comment style:

```cpp
int pre[N]; // 前缀和
// 状态计算
// 枚举领头人的位置
```

- Avoid verbose line-by-line comments. Do not explain syntax.
- In code, comments should usually be one short phrase, not full tutorial paragraphs.

## Problem Solution Writeups

When writing题解, use concise Chinese and a practical structure:

1. `思路`
2. `状态表示` / `状态转移` when DP is involved
3. `实现细节`
4. `复杂度`
5. `代码`

Keep prose close to the code. Prefer direct statements such as:

- `先排序，然后从左到右贪心。`
- `dp[i] 表示前 i 个物品能得到的最大值。`
- `用队列做 BFS，第一次到达就是最短路。`

Do not write a polished editorial unless asked. Keep the explanation suitable for students reading a training OJ solution.

## Fresh Code Template

For ordinary single-test problems:

```cpp
#include<bits/stdc++.h>
using namespace std;

const int N = 1e5 + 10;

int n;
int a[N];

int main()
{
	cin >> n;
	for (int i = 1; i <= n; i++)
		cin >> a[i];

	int ans = 0;
	
	cout << ans;
	return 0;
}
```

For multi-test problems, use `solve()`:

```cpp
#include<bits/stdc++.h>
using namespace std;

#define ll long long

void solve()
{
	
}

int main()
{
	int T;
	cin >> T;
	while (T--)
		solve();
	return 0;
}
```

## When To Deviate

- Use C++17 only if the judge/problem requires it or the user asks.
- Use vectors/maps when limits are dynamic or coordinate values are sparse.
- Add fast I/O for large input.
- Avoid `#define int long long` unless overflow is pervasive and the solution is simpler that way.
- Preserve existing file style when editing user-provided code, even if it differs from these defaults.
