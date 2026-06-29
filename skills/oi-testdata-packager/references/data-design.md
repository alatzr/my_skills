# OI Data Design Reference

## When Official Subtasks Exist

Copy the official table into a planning table and generate tests by group.

Example official table:

| Score | Range |
|---:|---|
| 10% | `n=1`, `sum k_i <= 10`, `x,t <= 10` |
| 20% | `n <= 10`, `sum k_i <= 100`, `x <= 100`, `t <= 32767` |
| 40% | `n <= 100`, `sum k_i <= 100`, `x <= 100`, `t <= 86400` |
| 70% | `n <= 1000`, `sum k_i <= 3000`, `x <= 1000`, `t <= 1e9` |
| 100% | `n <= 1e5`, `sum k_i <= 3e5`, `x <= 1e5`, `t <= 1e9` |

Design response:

| Group | Tests | Must Satisfy | Purpose |
|---|---:|---|---|
| G1 | 2-4 | 10% range | hand tiny, brute force check, all corner behavior |
| G2 | 3-5 | 20% range | small exhaustive/random, overflow near `32767` |
| G3 | 3-5 | 40% range | medium, time/day boundary near `86400` |
| G4 | 4-6 | 70% range | transition to intended complexity |
| G5 | 6-10 | 100% range | max size, worst pattern, adversarial random |

Rules:

- A G1 test must satisfy G1 limits exactly; do not accidentally use a larger value.
- Include at least one boundary value for every displayed upper bound.
- If constraints include `sum k_i`, test both many small groups and one group near the sum maximum.
- If the problem has `t_i` or weights up to `1e9`, include values that break `int` sum/multiplication.
- Keep a short note explaining which wrong solution each group attacks.

## When No Subtasks Exist

Create fair partial-score coverage:

| Group | Typical Size | Purpose |
|---|---|---|
| Tiny | `n <= 8-12` | brute force, exhaustive or dense random |
| Small | `n <= 50-200` | simple `O(n^2)`/`O(n^3)` solutions may pass |
| Medium | `n <= 2000-5000` | separates quadratic from intended |
| Special | full `n`, restricted shape | sorted input, tree, DAG, all equal, one dimension small |
| Full | max constraints | intended solution only |
| Anti-hack | max constraints | patterns targeting common wrong assumptions |

Choose ranges based on the likely complexities:

- If intended is `O(n log n)`, include a medium group that allows `O(n^2)` only on small values.
- If intended is DP `O(nm)`, include groups with one dimension tiny and another full.
- If intended is graph shortest path, include trees, sparse graphs, dense graphs if legal, and unreachable nodes.
- If intended uses modulo/math, include boundary residues and values near modulus.

## Test Types To Mix

Use all relevant types:

- Samples or sample-like tests.
- Minimum legal values.
- Single object / no operation / all operations.
- Maximum legal values.
- All equal values.
- Strictly increasing/decreasing values.
- Alternating patterns.
- Random uniform.
- Random clustered.
- Adversarial hand cases.
- Overflow-boundary cases.
- Duplicates and ties.
- Invalid-looking but legal edge cases.

## Generator Notes

For each generated pack, keep generator choices reproducible:

- Use a fixed random seed.
- Store generation code in `additional_file/mkin.h` or another file if useful.
- Name cases sequentially as `1.in`, `2.in`, ...
- Ensure line endings and trailing spaces are harmless.
- Sort input files numerically before packaging.

## Answer Generation And Cross-Check

Preferred reliability path:

1. Generate `.in`.
2. Run `std.cpp` to produce `.ans`.
3. For tiny cases, run `bf.cpp` and compare with `std.cpp`.
4. If outputs differ, stop and inspect before packaging.
5. Run the standard solution on maximum cases under intended time limits when feasible.

Never hand-write large `.ans` files.

## Reporting Template

After packaging, report:

```text
Output: /path/name.zip
Tests: 25
Groups:
- G1 official 10%: tests 1-4, tiny brute-force range
- G2 official 20%: tests 5-8, small random and boundary
- G3 official 40%: tests 9-12, medium constraints
- G4 official 70%: tests 13-18, transition/worst shapes
- G5 official 100%: tests 19-25, max and adversarial
Checks:
- std.cpp compiled
- answers generated
- brute force compared on tests 1-8
```
