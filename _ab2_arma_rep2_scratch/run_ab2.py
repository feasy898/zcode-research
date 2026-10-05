# -*- coding: utf-8 -*-
"""ab2 arm-a rep2 runner: backup pre-existing case2 outputs, then run
oracle (reference) and package/gen_doc.py (skill under test) on
请示函/case2.json and 会议通知/case2.json into scratch outdirs.
Only prints derived status (exit codes, produced files). Never prints source.
"""
import os, shutil, subprocess, sys

BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
SCR  = r"D:\workspace\zcode研究\_ab2_arma_rep2_scratch"
CASES = [("请示函", "case2"), ("会议通知", "case2")]

# 1) backup whatever already exists in the standard out dirs
for side, sub in (("oracle", r"oracle\out"), ("package", r"package\out")):
    for t, c in CASES:
        src = os.path.join(BASE, sub, t, c)
        dst = os.path.join(SCR, "backup", side, t, c)
        if os.path.isdir(src):
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"backup {side}/{t}/{c}: {sorted(os.listdir(dst))}")
        else:
            print(f"backup {side}/{t}/{c}: MISSING pre-existing dir")

# 2) run both implementations into scratch outdirs
for t, c in CASES:
    data = os.path.join(BASE, "oracle", "inputs", t, f"{c}.json")
    for side, cmd in (
        ("oracle", [sys.executable, os.path.join(BASE, "oracle", "oracle.py"),
                    "--template", t, "--data", data,
                    "--outdir", os.path.join(SCR, "out", "oracle", t, c)]),
        ("package", [sys.executable, os.path.join(BASE, "package", "scripts", "gen_doc.py"),
                     "--template", t, "--data", data,
                     "--outdir", os.path.join(SCR, "out", "package", t, c)]),
    ):
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        outd = os.path.join(SCR, "out", side, t, c)
        produced = sorted(os.listdir(outd)) if os.path.isdir(outd) else "NOT CREATED"
        print(f"run {side} {t}/{c}: exit={r.returncode} produced={produced}")
        if r.stdout.strip():
            print(f"  stdout: {r.stdout.strip()[:600]}")
        if r.stderr.strip():
            print(f"  stderr: {r.stderr.strip()[:600]}")
print("RUNNER DONE")
