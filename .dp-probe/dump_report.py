#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临时工具：把 oracle validate.py 的完整 JSON 报告落盘并打印全部字段（黑盒输出检查）。"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = r"D:\workspace\zcode研究"
ASSET = os.path.join(ROOT, "skillfactory", "v5", "assets", "deploy-pack")
PACK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ASSET, "package", "out", "pack-canonical")

tmp = tempfile.mkdtemp(prefix="dp-dump-")
rep = os.path.join(tmp, "r.json")
p = subprocess.run([sys.executable, os.path.join(ASSET, "oracle", "validate.py"),
                    "--pack", PACK, "--out", rep],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("exit:", p.returncode)
print("--- stdout ---")
print(p.stdout)
print("--- report full JSON ---")
if os.path.isfile(rep):
    with open(rep, "rb") as f:
        data = f.read().decode("utf-8-sig")
    print(data)
else:
    print("(no report file)")
