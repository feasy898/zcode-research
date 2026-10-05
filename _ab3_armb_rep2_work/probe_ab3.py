# -*- coding: utf-8 -*-
"""ab3 arm-b rep2 — SYNTHETIC-input ablation probes (values entirely ours, no fixture values).

P1 工作总结 complete: 存在问题 present + 成文日期 present, proper lists
   -> question: does the omitted-section renumbering (case2 B=三 / A=四) come from
      dynamic renumbering, and does the trailing ____ turn into the date?
P2 工作总结, 工作回顾 as ONE string containing a newline
   -> question: does either side split the string into multiple items (anti-单项化)?
P3 周报 complete: all fields incl. 部门 present
   -> question: does A render 部门 at all (case2 A dropped the label) — i.e. is the
      case2 drop missing-triggered?
Runs A (gen_doc.py) and B (oracle.py) on each probe into scratch probe dirs.
"""
import json, os, subprocess, sys, zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
WORK = r"D:\workspace\zcode研究\_ab3_armb_rep2_work"
IMPLS = {
    "A": (sys.executable, os.path.join(ROOT, "package", "scripts", "gen_doc.py")),
    "B": (sys.executable, os.path.join(ROOT, "oracle", "oracle.py")),
}

PROBES = {
    ("工作总结", "P1_complete"): {
        "总结时段": "2026年9月", "工作回顾": ["合成回顾一", "合成回顾二"],
        "主要成绩": ["合成成绩一"], "存在问题": ["合成问题一"],
        "下一步工作打算": ["合成打算一"], "成文日期": "2026年9月30日",
    },
    ("工作总结", "P2_newline_string"): {
        "总结时段": "2026年9月", "工作回顾": "合成回顾一\n合成回顾二",
        "主要成绩": ["合成成绩一"], "存在问题": ["合成问题一"],
        "下一步工作打算": ["合成打算一"], "成文日期": "2026年9月30日",
    },
    ("周报", "P3_complete"): {
        "周期": "2026-09-21 至 2026-09-27", "部门": "合成部门", "填报人": "合成填报人",
        "本周工作内容": ["合成本周一"], "下周工作计划": ["合成下周一"],
        "问题与需协调事项": ["合成协调一"], "报送日期": "2026-09-28",
    },
}

def blocks_of(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    out = []
    for el in root.find(W + "body"):
        tag = el.tag.split("}")[1]
        if tag == "p":
            out.append("".join(t.text or "" for t in el.iter(W + "t")))
        elif tag == "tbl":
            for tr in el.findall(W + "tr"):
                out.append(" | ".join("/".join("".join(t.text or "" for t in p.iter(W + "t"))
                                               for p in tc.findall(W + "p")) for tc in tr.findall(W + "tc")))
    return out

pdir = os.path.join(WORK, "probes")
os.makedirs(pdir, exist_ok=True)
for (t, pname), fields in PROBES.items():
    src = os.path.join(pdir, f"{pname}.json")
    json.dump(fields, open(src, "w", encoding="utf-8"), ensure_ascii=False)
    print("=" * 90)
    print(f"##### {t} / {pname} #####")
    for arm, (exe, script) in IMPLS.items():
        outdir = os.path.join(pdir, pname, arm)
        cp = subprocess.run([exe, script, "--template", t, "--data", src, "--outdir", outdir],
                            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        docx = os.path.join(outdir, "文书.docx")
        ok = os.path.isfile(docx)
        print(f"--- {arm}: exit={cp.returncode} docx={ok} stdout={cp.stdout.strip()[:220]!r}")
        if cp.stderr.strip():
            print(f"    stderr={cp.stderr.strip()[:220]!r}")
        if ok:
            for i, b in enumerate(blocks_of(docx)):
                print(f"    {i:02d} {b!r}")
print("DONE")
