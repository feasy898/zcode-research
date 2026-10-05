#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""并行黑盒探测台（临时工具）：并发跑多份 eval/runner.py，读 per-file matched 计数。
可选 c7=true 时同时跑 oracle validate.py 记录其 C7 字节差异文件清单（黑盒输出）。
不读 oracle/ 任何文件内容；只消费两个工具的输出。"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = r"D:\workspace\zcode研究"
ASSET = os.path.join(ROOT, "skillfactory", "v5", "assets", "deploy-pack")
EVAL = os.path.join(ASSET, "eval", "runner.py")
OVAL = os.path.join(ASSET, "oracle", "validate.py")
OREF = os.path.join(ASSET, "oracle", "out")
BASE = os.path.join(tempfile.gettempdir(), "dp-probe2")
FILES = ("docker-compose.yml", ".env.example", "DEPLOY.md")
MAXPAR = 10


def launch(idx, r):
    pack = os.path.join(BASE, "p%04d" % idx)
    os.makedirs(pack, exist_ok=True)
    for fn in FILES:
        lines = r.get(fn, [])
        with open(os.path.join(pack, fn), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))
    procs = [(subprocess.Popen([sys.executable, EVAL, pack, OREF], stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL), "eval")]
    if r.get("c7"):
        procs.append((subprocess.Popen([sys.executable, OVAL, "--pack", pack, "--out",
                                        os.path.join(pack, "_rep.json")],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), "val"))
    return pack, procs, r


def collect(pack, procs, r):
    m = {}
    for p, kind in procs:
        p.wait()
        if kind != "eval":
            continue
        out = p.stdout.read().decode("utf-8", "replace")
        try:
            j = json.loads(out)
            c4 = next(c for c in j["checks"] if c["name"] == "reference_text_agreement_90pct")
            m = {c["file"]: c["matched"] for c in c4["per_file"]}
            rate = j["summary"]["text_agreement_rate"]
        except Exception:
            m, rate = {"ERR": out[:200]}, None
    c7 = None
    rp = os.path.join(pack, "_rep.json")
    if r.get("c7") and os.path.isfile(rp):
        try:
            with open(rp, "rb") as f:
                rep = json.loads(f.read().decode("utf-8-sig"))
            c7 = {"verdict": rep.get("verdict"),
                  "C7diff": next((c.get("detail") for c in rep.get("checks", [])
                                  if c.get("name", "").startswith("C7")), None)}
        except Exception as e:
            c7 = {"err": str(e)}
    rec = {"label": r.get("label", ""),
           "compose": m.get("docker-compose.yml"), "env": m.get(".env.example"),
           "deploy": m.get("DEPLOY.md"), "rate": rate}
    if c7:
        rec["c7"] = c7
    return rec


def run_plan(plan):
    pending, results, idx = [], [], 0
    for r in plan:
        pending.append(launch(idx, r))
        idx += 1
        if len(pending) >= MAXPAR:
            for pack, procs, r0 in pending:
                results.append(collect(pack, procs, r0))
            pending = []
    for pack, procs, r0 in pending:
        results.append(collect(pack, procs, r0))
    for rec in results:
        print(json.dumps(rec, ensure_ascii=False))


if __name__ == "__main__":
    run_plan(json.load(sys.stdin))
