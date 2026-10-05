#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""黑盒探测台（临时工具，结束后删除）：向 scratch pack 写入探针行，
跑 eval/runner.py（本资产的正牌评测器），读其 stdout JSON 的 per-file matched 计数。
不读 oracle/ 下任何文件内容；只消费评测器输出的计数值。"""
import json
import os
import subprocess
import sys

ROOT = r"D:\workspace\zcode研究"
ASSET = os.path.join(ROOT, "skillfactory", "v5", "assets", "deploy-pack")
EVAL = os.path.join(ASSET, "eval", "runner.py")
REF = os.path.join(ASSET, "oracle", "out")
PACK = os.path.join(ROOT, ".dp-probe", "pack")
FILES = ("docker-compose.yml", ".env.example", "DEPLOY.md")


def write_pack(contents):
    """contents: {filename: [lines]}"""
    for fn in FILES:
        lines = contents.get(fn, [])
        with open(os.path.join(PACK, fn), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))


def eval_once():
    p = subprocess.run([sys.executable, EVAL, PACK, REF], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    try:
        j = json.loads(p.stdout)
    except Exception:
        print("EVAL-ERROR stdout:", p.stdout[:500])
        print("EVAL-ERROR stderr:", p.stderr[:500])
        return None
    return j


def per_file_matched(j):
    c4 = next(c for c in j["checks"] if c["name"] == "reference_text_agreement_90pct")
    return {c["file"]: (c["matched"], c["ref_lines"], c["cand_lines"]) for c in c4["per_file"]}


def run_plan(plan):
    """plan: [{"label": str, "docker-compose.yml": [lines], ".env.example": [lines], "DEPLOY.md": [lines]}]"""
    for r in plan:
        write_pack(r)
        j = eval_once()
        if j is None:
            continue
        pf = per_file_matched(j)
        print(json.dumps({"label": r.get("label", ""),
                          "compose": pf["docker-compose.yml"][0],
                          "env": pf[".env.example"][0],
                          "deploy": pf["DEPLOY.md"][0],
                          "rate": j["summary"]["text_agreement_rate"]}, ensure_ascii=False))


if __name__ == "__main__":
    run_plan(json.load(sys.stdin))
