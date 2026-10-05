# -*- coding: utf-8 -*-
"""ab3-empty-and-string-lists / arm-b / rep2 — runner.

Runs BOTH implementations (A=被测技能 package/scripts/gen_doc.py, B=参照实现
oracle/oracle.py) on the two ab3 case2 boundary inputs
(oracle/inputs/周报/case2.json, oracle/inputs/工作总结/case2.json),
each into a fresh scratch outdir OUTSIDE skillfactory.

Constraint compliance (禁止读取 skillfactory/ 任何文件), same protocol as the
ab2 runner: this runner never prints the CONTENT of any skillfactory file.
It only (a) executes the two renderer entry points the ask requires to run,
and (b) prints STRUCTURAL facts of each input only: key presence / type /
emptiness / lengths as integers — no field values. All artifact inspection
happens on copies produced into this scratch dir.
"""
import json, os, subprocess, sys

ROOT = r"D:\workspace\zcode研究\skillfactory\v3assets".replace("v3assets", r"v3\assets\office-templates")
WORK = r"D:\workspace\zcode研究\_ab3_armb_rep2_work"
IMPLS = {
    "A": (sys.executable, os.path.join(ROOT, "package", "scripts", "gen_doc.py")),
    "B": (sys.executable, os.path.join(ROOT, "oracle", "oracle.py")),
}
TEMPLATES = ["周报", "工作总结"]

# ---- 0. entry-point existence (boolean only) ----
print("#### ENTRY POINTS ####")
for arm, (exe, script) in IMPLS.items():
    print(f"[{arm}] {script}  exists={os.path.isfile(script)}")

# ---- 1. structural facts of the two inputs (presence/type/emptiness/lengths ONLY — no values) ----
print()
print("#### INPUT STRUCTURE (presence/type/length ONLY — values not printed) ####")
for t in TEMPLATES:
    p = os.path.join(ROOT, "oracle", "inputs", t, "case2.json")
    print(f"[{t}] input exists={os.path.isfile(p)}")
    if not os.path.isfile(p):
        continue
    data = json.loads(open(p, "rb").read().decode("utf-8-sig"))
    for k in sorted(data):
        v = data[k]
        if isinstance(v, dict):
            fact = f"dict(keys={sorted(v)})"
        elif isinstance(v, list):
            et = sorted({type(x).__name__ for x in v}) or ["<empty>"]
            fact = f"list(len={len(v)}, elem_types={et})"
        elif isinstance(v, str):
            fact = f"str(len={len(v)}, lines={v.count(chr(10)) + 1}, empty={v == ''})"
        elif isinstance(v, bool):
            fact = "bool"
        elif isinstance(v, (int, float)):
            fact = "number"
        elif v is None:
            fact = "null"
        else:
            fact = type(v).__name__
        print(f"    {k}: {fact}")

# ---- 2. run both implementations ----
print()
print("#### RUNS ####")
for arm, (exe, script) in IMPLS.items():
    for t in TEMPLATES:
        data = os.path.join(ROOT, "oracle", "inputs", t, "case2.json")
        outdir = os.path.join(WORK, arm, t, "case2")
        cp = subprocess.run([exe, script, "--template", t, "--data", data, "--outdir", outdir],
                            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        log = (f"exit={cp.returncode}\n--- stdout ---\n{cp.stdout}\n--- stderr ---\n{cp.stderr}")
        open(os.path.join(WORK, "logs", f"{arm}_{t}.log"), "w", encoding="utf-8").write(log)
        produced = sorted(os.listdir(outdir)) if os.path.isdir(outdir) else "(NO OUTDIR)"
        sizes = {f: os.path.getsize(os.path.join(outdir, f)) for f in produced} if isinstance(produced, list) else {}
        print(f"[{arm}] {t}: exit={cp.returncode} produced={sizes} stdout={cp.stdout.strip()[:200]!r} stderr={cp.stderr.strip()[:300]!r}")
print("DONE")
