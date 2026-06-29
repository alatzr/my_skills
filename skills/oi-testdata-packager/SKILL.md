---
name: oi-testdata-packager
description: Create OI/ICPC-style judgedata packages from known problem statements, standard solutions, brute force solutions, generators, and data range tables. Use when Codex must design subtasks, generate tests with partial-score brute-force points, include special cases, produce .in/.ans files, or package a zip like problem.yaml + testdata + additional_file for OI training problems.
---

# OI Testdata Packager

## Core Goal

Produce a judgedata zip package for an already-understood problem. The package must respect official constraints when given, and must deliberately include brute-force subtasks, special cases, boundary cases, randomized cases, and full-score cases.

Default output structure should match:

```text
name.zip
└── 1/
    ├── problem.yaml
    ├── problem_zh.md
    ├── problem_en.md
    ├── testdata/
    │   ├── 1.in
    │   ├── 1.ans
    │   ├── ...
    │   └── config.yaml
    └── additional_file/
        ├── std.cpp
        ├── solution_zh.md
        └── mkin.h
```

If the user gives a different platform format, adapt the packager, but preserve the principle: every `.in` has a matching `.ans`, metadata is present, and the zip opens directly into the expected root directory.

## Workflow

1. Read the full problem statement, input/output format, samples, constraints, and any scoring table.
2. Extract all variables and constraints into a short data-design table.
3. If the statement has a subtask/scoring table, follow it strictly. Each official range must have tests inside that range, and full-score tests must hit the maximum ranges.
4. If the statement has no scoring table, design partial-score groups yourself:
   - tiny brute-force group,
   - small/medium algorithm-transition group,
   - special-structure group,
   - adversarial/boundary group,
   - full random and full worst-case group.
5. Write or collect:
   - `std.cpp`: accepted intended solution,
   - optional `bf.cpp`: brute-force oracle for tiny cases,
   - generator script or generator notes.
6. Generate tests by group. Include samples only if requested; otherwise keep samples separate from official tests.
7. Produce answers with `std.cpp`. Cross-check tiny cases with `bf.cpp` when available.
8. Run sanity checks: constraints, parser coverage, duplicate detection when useful, and no empty output files.
9. Package as zip and report group coverage.

Read `references/data-design.md` whenever designing data groups or when the user provides a table like “10%, 20%, 40%, 70%, 100%”.

Use `scripts/oi_pack.py` when you already have a directory of `.in` files and a standard solution and need deterministic `.ans`, metadata, config, and zip packaging.

## Data Design Rules

- Treat the official data range table as a contract, not a suggestion.
- Do not put a test exceeding a lower subtask range inside that subtask’s group.
- Include at least one maximum-boundary test for each meaningful official range.
- Include cases that target common wrong solutions, not only random data.
- For multi-test input, vary both the number of test cases and the total size.
- Prefer deterministic generators with a fixed seed and record the seed in notes or comments.
- Avoid all-random packs. Use a mix of hand cases, structured generators, and random stress cases.
- For graph problems, cover disconnected/connected, tree/dense, self-loop/multi-edge if allowed, and indexing boundaries.
- For DP problems, cover impossible states, many optimal choices, zero/one boundaries, and maximum dimensions.
- For string problems, cover empty/minimal strings when legal, all same characters, alternating patterns, periodic strings, and long random strings.
- For math problems, cover primes/composites, powers, gcd/lcm extremes, overflow boundaries, and modulo edge cases.

## Package Metadata Defaults

Use this `problem.yaml` shape unless the user gives a platform-specific schema:

```yaml
pid: <problem-id>
owner: 3
title: <title>
tag:
  - <tag1>
  - <tag2>
nSubmit: 1
nAccept: 1
```

Use this `testdata/config.yaml` unless the user specifies time/memory:

```yaml
type: default
time: 2s
memory: 256m
```

## Script Quick Start

Prepare:

```text
work/
├── inputs/
│   ├── 1.in
│   ├── 2.in
│   └── ...
├── std.cpp
├── problem_zh.md
├── problem_en.md
└── solution_zh.md
```

Run:

```bash
python3 scripts/oi_pack.py \
  --input-dir work/inputs \
  --std work/std.cpp \
  --out-dir work/out \
  --zip-name name.zip \
  --pid CF6A \
  --title Triangle \
  --tags GESP一级 CodeForces CF-900 枚举 几何知识 \
  --problem-zh work/problem_zh.md \
  --problem-en work/problem_en.md \
  --solution-zh work/solution_zh.md
```

The script compiles `std.cpp`, runs it on every `.in`, writes `.ans`, creates the reference directory layout, and writes the zip.

## Validation Checklist

Before finishing, verify:

- The zip contains `1/testdata/N.in` and `1/testdata/N.ans` for every case.
- The number of tests and subtask intent are reported to the user.
- The official constraints are satisfied by every case.
- Tiny tests were cross-checked with brute force if a brute-force program exists.
- Full-score cases include maximum sizes, worst shapes, and random cases.
- `problem.yaml`, `config.yaml`, `std.cpp`, and solution notes are included.
- No generated `.ans` file is empty unless the correct output can be empty and the checker allows it.

## User-Facing Summary

When done, report:

- zip path,
- number of tests,
- groups/subtasks covered,
- whether `std.cpp` compiled and generated all answers,
- whether brute-force cross-check was run,
- any uncertainty about statement interpretation.
