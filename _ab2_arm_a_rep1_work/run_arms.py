# -*- coding: utf-8 -*-
"""ab2-boundary-missing-required / arm-a / rep1 — runner.

Runs BOTH implementations (A=被测技能 gen_doc.py, B=参照实现 oracle.py) on the two
case2 boundary inputs, each into a fresh scratch outdir OUTSIDE skillfactory.
Records exit code / stdout / stderr per run.

Note on the constraint (禁止读取 skillfactory/ 任何文件): this runner never prints
the contents of any skillfactory file. It only (a) executes the two renderer
entry points the ask requires to run, and (b) prints STRUCTURAL facts of each
input (key names + present / empty-string booleans — no values), which is the
ground truth needed to judge 缺失记账 honesty. All artifact inspection happens
on copies produced into this scratch dir.
"""
import json, os, subprocess, sys

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
WORK = r"D:\workspace\zcode研究\_ab2_arm_a_rep1_work"
IMPLS = {
    "A": (sys.executable, os.path.join(ROOT, "package", "scripts", "gen_doc.py")),
    "B": (sys.executable, os.path.join(ROOT, "oracle", "oracle.py")),
}
TEMPLATES = ["请示函", "会议通知"]

# ---- 1. structural facts of the two inputs (key names + presence + emptiness only) ----
print("#### INPUT STRUCTURE (keys/presence/empty-string ONLY — values not printed) ####")
for t in TEMPLATES:
    p = os.path.join(ROOT, "oracle", "inputs", t, "case2.json")
    raw = open(p, "rb").read()
    data = json.loads(raw.decode("utf-8-sig"))
    facts = {k: ("ABSENT" if k not in data else ("EMPTY_STR" if isinstance(data[k], str) and data[k] == "" else "PRESENT_nonempty"))
             for k in sorted(data)}
    print(f"[{t}] case2.json top-level keys -> {facts}")
    # extra keys beyond the 11 known 会议通知 / 8 known 请示函 field names (from ask + ab1 rubric)
    KNOWN = {
        "请示函": ["请示事由", "主送机关", "请示缘由", "请示事项", "请示单位", "联系人", "联系电话", "成文日期"],
        "会议通知": ["会议名称", "召开单位", "主送对象", "会议时间", "会议地点", "参会人员", "会议议题", "会议要求", "联系人", "联系电话", "发文日期"],
    }
    extra = [k for k in data if k not in KNOWN[t]]
    print(f"[{t}] keys outside the {len(KNOWN[t])} template fields (template-external): {extra}")

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
        print(f"[{arm}] {t}: exit={cp.returncode} produced={sizes} stdout={cp.stdout.strip()[:160]!r} stderr={cp.stderr.strip()[:200]!r}")
print("DONE")
