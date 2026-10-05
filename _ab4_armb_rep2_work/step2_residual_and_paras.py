#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""step2：①阴性-only 残留扫描（spec 附录 A-3 同法：新建子树→只跑 8 条阴性→计数残留）
②对照组 A/B docx 逐段对照（量化合法路径上的既知差异）。"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

SCRATCH = Path(r"D:\workspace\zcode研究\_ab4_armb_rep2_work")
ASSET = Path(r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates")
ARM = {"A": ASSET / "package" / "scripts" / "gen_doc.py",
       "B": ASSET / "oracle" / "oracle.py"}
CTRL_DATA = ASSET / "oracle" / "inputs" / "周报" / "case1.json"
PY = sys.executable
NEG_ONLY = SCRATCH / "neg_only"

for s in (sys.stdout, sys.stderr):
    if hasattr(s, "reconfigure"):
        s.reconfigure(encoding="utf-8", errors="replace")

# ---------- ① 阴性-only：全新子树，只跑 8 条阴性命令 ----------
if NEG_ONLY.exists():
    shutil.rmtree(NEG_ONLY)
(NEG_ONLY / "inputs").mkdir(parents=True)
p3 = NEG_ONLY / "inputs" / "notjson.json"
p3.write_text("不是JSON", encoding="utf-8")
p4 = NEG_ONLY / "inputs" / "toplist.json"
p4.write_text('["数组","非对象"]', encoding="utf-8")
p2 = NEG_ONLY / "inputs" / "no_such_file.json"
assert not p2.exists()

neg_cases = [
    ("n1", "证书", str(CTRL_DATA)),
    ("n2", "周报", str(p2)),
    ("n3", "周报", str(p3)),
    ("n4", "周报", str(p4)),
]
exits = {}
for arm in ("A", "B"):
    for case, tpl, data in neg_cases:
        outdir = NEG_ONLY / "out" / arm / case
        cmd = [PY, str(ARM[arm]), "--template", tpl, "--data", data, "--outdir", str(outdir)]
        proc = subprocess.run(cmd, cwd=str(NEG_ONLY), capture_output=True)
        exits[f"{arm}/{case}"] = proc.returncode
        assert not outdir.exists(), f"残留：{outdir} 被创建"

residual = [str(p.relative_to(NEG_ONLY)) for p in NEG_ONLY.rglob("*")
            if p.is_file() and p.name in ("文书.docx", "fields.json")]
step1 = {
    "method": "spec 附录 A-3 同法：全新子树 neg_only/，只跑 8 条阴性命令（2 实现 × 4 非法输入）",
    "exit_codes": exits,
    "negative_exit_all_2": all(v == 2 for v in exits.values()),
    "residual_count_文书_docx_plus_fields_json": len(residual),
    "residual_paths": residual,
    "neg_only_tree_file_inventory": sorted(
        str(p.relative_to(NEG_ONLY)) for p in NEG_ONLY.rglob("*") if p.is_file()),
}

# ---------- ② 对照组 docx 逐段对照 ----------
import docx


def paras(p: Path) -> list[str]:
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            if name.endswith((".xml", ".rels")):
                head = z.read(name)[:4096]
                assert b"<!DOCTYPE" not in head and b"<!ENTITY" not in head, name
    return [q.text for q in docx.Document(str(p)).paragraphs]


pa = paras(SCRATCH / "out" / "A" / "C" / "文书.docx")
pb = paras(SCRATCH / "out" / "B" / "C" / "文书.docx")
diffs = [{"idx": i, "A": a, "B": b} for i, (a, b) in enumerate(zip(pa, pb)) if a != b]
step2 = {
    "paragraph_count": {"A": len(pa), "B": len(pb)},
    "diff_paragraphs": diffs,
    "A_paragraphs": pa,
    "B_paragraphs": pb,
}
out = {"step1_negative_only_sweep": step1, "step2_control_paragraphs": step2}
(SCRATCH / "step2_report.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
