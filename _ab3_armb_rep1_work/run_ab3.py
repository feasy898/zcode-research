# -*- coding: utf-8 -*-
"""ab3-empty-and-string-lists / arm-b / rep1 — runner.

Runs BOTH implementations (A=被测技能 gen_doc.py, B=参照实现 oracle.py) on the two
ab3 case2 inputs (周报 / 工作总结), each into a fresh scratch outdir OUTSIDE skillfactory.

Constraint protocol (禁止读取 skillfactory/ 任何文件), same as the ab2 arm-a runner:
this script never prints the contents of any skillfactory file. It only
  (a) executes the two renderer entry points the ask requires to run, and
  (b) prints STRUCTURAL facts of each input (key names, JSON types, list lengths,
      element type sets, emptiness booleans — no string values),
which is the ground truth needed to judge 占位条目/省略/字符串单项化 behavior.
All artifact inspection happens on copies produced into this scratch dir.
"""
import hashlib, json, os, subprocess, sys

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
WORK = r"D:\workspace\zcode研究\_ab3_armb_rep1_work"
IMPLS = {
    "A": (sys.executable, os.path.join(ROOT, "package", "scripts", "gen_doc.py")),
    "B": (sys.executable, os.path.join(ROOT, "oracle", "oracle.py")),
}
TEMPLATES = ["周报", "工作总结"]
SCHEMA = {  # (name, required, kind) — from ab1-era ledger copies held in local scratch
    "周报": [("部门", 1, "text"), ("填报人", 1, "text"), ("周期", 1, "text"),
           ("本周工作内容", 1, "list"), ("下周工作计划", 1, "list"),
           ("问题与需协调事项", 0, "list"), ("报送日期", 0, "text")],
    "工作总结": [("总结主体", 1, "text"), ("总结时段", 1, "text"), ("工作回顾", 1, "list"),
             ("主要成绩", 1, "list"), ("存在问题", 0, "list"),
             ("下一步工作打算", 1, "list"), ("成文日期", 0, "text")],
}

print("#### ENTRY POINTS (existence by name only) ####")
for arm, (exe, script) in IMPLS.items():
    print(f"[{arm}] exe={os.path.basename(exe)} script={script} exists={os.path.isfile(script)}")

print()
print("#### INPUT STRUCTURE (keys/types/lengths/emptiness ONLY — no string values) ####")
inputs = {}
for t in TEMPLATES:
    p = os.path.join(ROOT, "oracle", "inputs", t, "case2.json")
    raw = open(p, "rb").read()
    inputs[t] = p
    data = json.loads(raw.decode("utf-8-sig"))
    facts = {}
    for k, v in data.items():
        if isinstance(v, str):
            facts[k] = f"str(len={len(v)},empty={v == ''})"
        elif isinstance(v, list):
            has_empty_str = any(isinstance(x, str) and x == "" for x in v)
            facts[k] = (f"list(len={len(v)},elem_types={sorted(set(type(x).__name__ for x in v))},"
                        f"has_empty_str_elem={has_empty_str})")
        else:
            facts[k] = type(v).__name__
    absent = [n for n, _, _ in SCHEMA[t] if n not in data]
    print(f"[{t}] case2.json size={len(raw)}B sha256={hashlib.sha256(raw).hexdigest()[:16]}")
    print(f"[{t}] structural: {json.dumps(facts, ensure_ascii=False)}")
    print(f"[{t}] schema fields ABSENT from input: {absent}")
    print(f"[{t}] keys outside the {len(SCHEMA[t])} template fields: {[k for k in data if k not in {n for n, _, _ in SCHEMA[t]}]}")

print()
print("#### RUNS (A=被测技能 gen_doc.py, B=参照实现 oracle.py) ####")
for arm, (exe, script) in IMPLS.items():
    for t in TEMPLATES:
        outdir = os.path.join(WORK, arm, t, "case2")
        cmd = [exe, script, "--template", t, "--data", inputs[t], "--outdir", outdir]
        print(f"[{arm}] {t}: CMD = python package/scripts/gen_doc.py oracle/oracle.py --template {t} --data oracle/inputs/{t}/case2.json --outdir _ab3_armb_rep1_work/{arm}/{t}/case2".replace("package/scripts/gen_doc.py oracle/oracle.py", ("package/scripts/gen_doc.py" if arm == "A" else "oracle/oracle.py")))
        cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=180, cwd=WORK)
        open(os.path.join(WORK, "logs", f"{arm}_{t}.log"), "w", encoding="utf-8").write(
            f"exit={cp.returncode}\n--- argv ---\n{cmd}\n--- stdout ---\n{cp.stdout}\n--- stderr ---\n{cp.stderr}")
        produced = sorted(os.listdir(outdir)) if os.path.isdir(outdir) else "(NO OUTDIR)"
        sizes = {f: os.path.getsize(os.path.join(outdir, f)) for f in produced} if isinstance(produced, list) else {}
        print(f"[{arm}] {t}: exit={cp.returncode} produced={sizes}")
        if cp.stdout.strip():
            print(f"    stdout: {cp.stdout.strip()[:300]!r}")
        if cp.stderr.strip():
            print(f"    stderr: {cp.stderr.strip()[:300]!r}")
print("DONE")
