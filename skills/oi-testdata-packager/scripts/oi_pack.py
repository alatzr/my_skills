#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, text=True, **kwargs)


def numeric_key(path: Path):
    stem = path.stem
    return (0, int(stem)) if stem.isdigit() else (1, stem)


def copy_if_exists(src, dst):
    if src:
        p = Path(src)
        if p.exists():
            shutil.copy2(p, dst)


def write_problem_yaml(path: Path, pid: str, title: str, tags, owner: str):
    lines = [
        f"pid: {pid}",
        f"owner: {owner}",
        f"title: {title}",
        "tag:",
    ]
    for tag in tags:
        lines.append(f"  - {tag}")
    lines += ["nSubmit: 1", "nAccept: 1"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_config(path: Path, time_limit: str, memory_limit: str):
    path.write_text(
        f"type: default\ntime: {time_limit}\nmemory: {memory_limit}\n",
        encoding="utf-8",
    )


def compile_cpp(src: Path, exe: Path):
    cmd = ["g++", "-std=c++17", "-O2", "-pipe", str(src), "-o", str(exe)]
    run(cmd)


def generate_answers(inputs, exe: Path, testdata_dir: Path, timeout: float):
    for idx, inp in enumerate(inputs, start=1):
        out = testdata_dir / f"{idx}.ans"
        dst_in = testdata_dir / f"{idx}.in"
        shutil.copy2(inp, dst_in)
        data = inp.read_bytes()
        proc = subprocess.run(
            [str(exe)],
            input=data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr.decode("utf-8", errors="replace"))
            raise RuntimeError(f"std failed on {inp.name} with code {proc.returncode}")
        out.write_bytes(proc.stdout)


def compare_with_bf(inputs, std_exe: Path, bf_exe: Path, limit: int, timeout: float):
    checked = 0
    for inp in inputs[:limit]:
        data = inp.read_bytes()
        a = subprocess.run([str(std_exe)], input=data, stdout=subprocess.PIPE, timeout=timeout, check=True)
        b = subprocess.run([str(bf_exe)], input=data, stdout=subprocess.PIPE, timeout=timeout, check=True)
        if a.stdout != b.stdout:
            raise RuntimeError(f"bf mismatch on {inp.name}")
        checked += 1
    return checked


def make_zip(root_dir: Path, zip_path: Path):
    if zip_path.exists():
        zip_path.unlink()
    zip_abs = zip_path.resolve()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root_dir.rglob("*")):
            if path.is_file() and path.resolve() != zip_abs:
                zf.write(path, path.relative_to(root_dir))


def main():
    ap = argparse.ArgumentParser(description="Build an OI-style judgedata package zip.")
    ap.add_argument("--input-dir", required=True, help="Directory containing .in files.")
    ap.add_argument("--std", required=True, help="Standard solution C++ file.")
    ap.add_argument("--out-dir", required=True, help="Output working directory.")
    ap.add_argument("--zip-name", default="name.zip", help="Output zip file name.")
    ap.add_argument("--pid", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--tags", nargs="*", default=[])
    ap.add_argument("--owner", default="3")
    ap.add_argument("--time", default="2s")
    ap.add_argument("--memory", default="256m")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--problem-zh")
    ap.add_argument("--problem-en")
    ap.add_argument("--solution-zh")
    ap.add_argument("--mkin")
    ap.add_argument("--bf", help="Optional brute-force C++ file.")
    ap.add_argument("--bf-count", type=int, default=0, help="Number of first tests to compare with bf.")
    args = ap.parse_args()

    input_dir = Path(args.input_dir)
    inputs = sorted(input_dir.glob("*.in"), key=numeric_key)
    if not inputs:
        raise SystemExit("no .in files found")

    out_dir = Path(args.out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    problem_dir = out_dir / "1"
    testdata_dir = problem_dir / "testdata"
    add_dir = problem_dir / "additional_file"
    testdata_dir.mkdir(parents=True)
    add_dir.mkdir(parents=True)

    std_src = Path(args.std)
    shutil.copy2(std_src, add_dir / "std.cpp")
    copy_if_exists(args.problem_zh, problem_dir / "problem_zh.md")
    copy_if_exists(args.problem_en, problem_dir / "problem_en.md")
    copy_if_exists(args.solution_zh, add_dir / "solution_zh.md")
    copy_if_exists(args.mkin, add_dir / "mkin.h")

    write_problem_yaml(problem_dir / "problem.yaml", args.pid, args.title, args.tags, args.owner)
    write_config(testdata_dir / "config.yaml", args.time, args.memory)

    with tempfile.TemporaryDirectory() as td:
        std_exe = Path(td) / "std"
        compile_cpp(std_src, std_exe)
        if args.bf and args.bf_count > 0:
            bf_exe = Path(td) / "bf"
            compile_cpp(Path(args.bf), bf_exe)
            checked = compare_with_bf(inputs, std_exe, bf_exe, args.bf_count, args.timeout)
        else:
            checked = 0
        generate_answers(inputs, std_exe, testdata_dir, args.timeout)

    zip_path = out_dir / args.zip_name
    make_zip(out_dir, zip_path)

    print(f"zip: {zip_path}")
    print(f"tests: {len(inputs)}")
    print(f"bf_checked: {checked}")


if __name__ == "__main__":
    main()
