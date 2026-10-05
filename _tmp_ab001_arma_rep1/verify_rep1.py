# -*- coding: utf-8 -*-
"""verify_rep1.py — 复用 eval/runner.py 的检查函数，对自定义输入产物跑检查 1-4（不含检查5）。

用法：python verify_rep1.py <被测case目录>
样例输入取自本目录 sample_input.json（与任务给定的 platform/topic/points 一致）。
检查 5（与 oracle 参照一致率）不适用：oracle/out 仅覆盖资产自带 8 case 的输入，
与本任务自定义 topic/points 不同，逐项比对 points_used/topic 必然失配，非产物缺陷。
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "..", "skillfactory", "v4", "assets", "hot-templates")
RUNNER = os.path.join(ASSET, "eval", "runner.py")

spec = importlib.util.spec_from_file_location("runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

case_dir = os.path.abspath(sys.argv[1])
case_name = "dy/rep1"

with open(os.path.join(HERE, "sample_input.json"), "r", encoding="utf-8-sig") as f:
    sample = json.load(f)
platform = sample["platform"]
topic = str(sample["topic"]).strip()
pts, err = runner.norm_points(sample["points"])
assert err is None, err

checks, ctx = runner.check_artifacts(case_name, case_dir)
if ctx is None:
    for c in checks:
        print(json.dumps(c, ensure_ascii=False))
    sys.exit(1)

checks.append(runner.check_self_consistent(case_name, ctx["sj"], pts, platform))
checks.append(runner.check_platform_template(case_name, ctx["sj"], ctx["md_raw"], pts, platform))
checks.append(runner.check_sample_data(case_name, ctx, topic, pts))

failed = [c for c in checks if not c["pass"]]
for c in checks:
    print(json.dumps(c, ensure_ascii=False))
print("SUMMARY passed=%d failed=%d ok=%s" % (len(checks) - len(failed), len(failed), not failed))
sys.exit(0 if not failed else 1)
