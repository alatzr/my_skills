---
name: gdy-cpp-style
description: "gdy 的个人 OJ 代码与题解风格。用于编写竞赛题代码、OJ 提交、中文题解、算法讲解时贴近 gdy 历史提交习惯：以 C++14/C++11(O2) 为主，偏短变量名、全局数组、直接实现、少封装、中文短注释和训练题风格说明。"
---

# gdy C++ 代码风格

## 核心目标

按 gdy 平时在 OJ 上提交代码和写题解的习惯输出：简洁、偏竞赛实战、可直接粘贴到 Hydro/AtCoder/USACO 类评测系统，说明文字用中文，代码少包装、重实现。

除非用户明确要求其他语言或其他风格，否则写 OJ 代码和题解时优先使用本风格。

## 代码默认习惯

- 默认使用 C++14 兼容写法。
- 以如下模板开头：

```cpp
#include<bits/stdc++.h>
using namespace std;
```

- 需要 long long 时，简单题优先写 `#define ll long long`。
- 数据范围已知时优先写全局常量：`const int N = ... + 10;`。常见形式有 `1e5 + 10`、`2e5 + 10`、`1e6 + 10`、`1010`、`510`。
- 竞赛数据结构优先全局声明：
  `a[N]`、`b[N]`、`c[N]`、`dp[N]`、`f[N]`、`g[N]`、`st[N]`、`vis[N]`、`dist[N]`、`ans[N]`、`vector<int> adj[N]`。
- 普通单测题优先写 `int main()`：

```cpp
int main(){
	...
	return 0;
}
```
- 新写代码优先用 TAB 缩进；如果是在已有 4 空格代码里修改，则保持原文件缩进。
- 不要过度使用类、命名空间、lambda、泛型模板。只有标准算法拆出来更清楚时，才写辅助函数。

## 输入输出

- 默认使用 `cin` / `cout`。
- 小中等数据量不要主动加快速 IO；输入量大时再加：

```cpp
ios::sync_with_stdio(false);
cin.tie(0);
```

- `scanf` / `printf` 只在已有代码就是这种风格，或格式/性能确实更方便时使用。
- 输出换行可以用 `endl`。
- 文件输入输出题在 `main` 开头显式写：

```cpp
freopen("xxx.in", "r", stdin);
freopen("xxx.out", "w", stdout);
```

## 命名习惯

- 循环和公式里使用短变量名：`i`、`j`、`k`、`n`、`m`、`x`、`y`、`l`、`r`、`mid`、`sum`、`ans`、`cnt`、`res`。
- 算法函数用常见名字：`dfs`、`bfs`、`dijkstra`、`find`、`add`、`cmp`、`solve`。
- 小结构体优先命名为 `Node`，字段常用 `x`、`y`、`z`、`val`、`d`、`id`。
- pair 相关可用 `PII` 或 `pair<int,int>`；排序或图论代码中可接受 `#define x first`、`#define y second`。
- 数组默认 1 下标；当题目天然 0 下标或 0 下标更优或使用 STL vector 更自然时再用 0 下标。

## 算法实现偏好

- 标准算法直接写出来，不要藏在复杂封装里。
- 已知范围时优先数组，不优先 vector。
- 图论用 `vector<int> adj[N]` 或链式前向星/边数组。
- 网格 BFS 使用 `dx/dy` 数组，队列可用 `queue<Node>`，也可以用手写数组队列。
- DFS 默认递归实现；递归深度风险明显时再改迭代或说明风险。
- DP 常用 `dp`、`f`、`g`。初始化 INF 用 `memset(dp, 0x3f, sizeof dp)`，清零用 `memset(..., 0, ...)`。
- INF 常写 `const int INF = 0x3f3f3f3f;` 或 `const int INF = 1e9;`。
- 全局数组排序写 `sort(p+1, p+1+n, cmp)`；vector 排序写 `sort(v.begin(), v.end())`。
- 代码整体保持紧凑，不为“看起来高级”额外加包装。

## 注释风格

- 只在关键代码或复杂逻辑处添加中文短注释。
- 推荐注释形态：

```cpp
int s[N]; // 前缀和
// 状态计算
// 枚举领头人的位置
```

- 不要逐行解释语法。
- 代码内注释通常是一句话或一个短语，不写长篇教程。

## 题解写法

写中文题解时保持训练题风格，结构简洁直接，容易理解：
1. 题目大意
2. 思路
3. 算法
4. 时间复杂度
5. 参考代码

说明尽量贴近代码，使用直接表达：
- `先排序，然后从左到右贪心。`
- `dp[i] 表示前 i 个物品能得到的最大值。`
- `用队列做 BFS，第一次到达就是最短路。`

## 常用代码模板

普通单测题：

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

多测题：

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
- 坐标稀疏、数据范围动态、需要离散化时，可以用 vector/map。
- 输入非常大时加快速 IO。
- 不要默认 `#define int long long`，只有整题都容易溢出且这样更简洁时再用。
- 修改用户已有代码时，优先保持原文件风格，而不是强行套模板。
