#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_rep2.py — 复用资产评测器 eval/runner.py 的检查函数，对 ab-002/arm-b/rep2 产物执行检查 1-4。
样例输入 = 本任务输入（platform=xhs, topic=租房避坑指南, 5 条卖点）。
检查 5（与 oracle 参照逐项比对）不适用：oracle 仅覆盖资产自带 8 个 golden case。
"""
import json
import os
import sys

ASSET = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "skillfactory", "v4", "assets", "hot-templates"))
sys.path.insert(0, os.path.join(ASSET, "eval"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
import runner  # eval/runner.py

CAND = os.path.normpath(os.path.join(ASSET, "tests", "ab", "ab-002", "arm-b", "rep2"))
PLATFORM, TOPIC = "xhs", "租房避坑指南"
PTS = ["签约前查房东房产证与身份证一致性",
       "押金条款写明退还条件与时限",
       "入住当天拍照录像留档",
       "水电燃气表底数写进合同附件",
       "转租条款提前约定违约金"]

checks, ctx = runner.check_artifacts("ab-002/arm-b/rep2", CAND)
if ctx is None:
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    sys.exit(1)
checks.append(runner.check_self_consistent("ab-002/arm-b/rep2", ctx["sj"], PTS, PLATFORM))
checks.append(runner.check_platform_template("ab-002/arm-b/rep2", ctx["sj"], ctx["md_raw"], PTS, PLATFORM))
checks.append(runner.check_sample_data("ab-002/arm-b/rep2", ctx, TOPIC, PTS))
failed = [c for c in checks if not c["pass"]]
print(json.dumps({"ok": not failed, "checks": checks}, ensure_ascii=False, indent=2))
sys.exit(0 if not failed else 1)
