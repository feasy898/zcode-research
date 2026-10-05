# -*- coding: utf-8 -*-
"""Diagnostic: does A render boilerplate when data is COMPLETE (case1)? Also A/B on case1,
plus explicit leftover-token scan ({...} / {{...}} / 【】) on case2 outputs."""
import json, os, subprocess, sys, zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
WORK = r"D:\workspace\zcode研究\_ab2_arm_a_rep1_work"
IMPLS = {"A": os.path.join(ROOT, "package", "scripts", "gen_doc.py"),
         "B": os.path.join(ROOT, "oracle", "oracle.py")}
PINS = {"请示函": ["现就有关事项请示如下：", "妥否，请批示。"],
        "会议通知": ["经研究，决定召开", "现将有关事项通知如下", "特此通知。", "一、", "二、", "三、"]}

def docx_paras(p):
    z = zipfile.ZipFile(p)
    root = ET.fromstring(z.read("word/document.xml"))
    return ["".join(t.text or "" for t in el.iter(W + "t")) for el in root.iter(W + "p")]

for t in ("请示函", "会议通知"):
    for arm, script in IMPLS.items():
        outdir = os.path.join(WORK, "diag_case1", arm, t)
        cp = subprocess.run([sys.executable, script, "--template", t,
                             "--data", os.path.join(ROOT, "oracle", "inputs", t, "case1.json"),
                             "--outdir", outdir], capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert cp.returncode == 0, (arm, t, cp.stderr[:300])
        txt = "\n".join(x for x in docx_paras(os.path.join(outdir, "文书.docx")) if x.strip())
        pins = {pin: (pin in txt) for pin in PINS[t]}
        print(f"[case1/{t}] {arm}: pins={pins}")
    # leftover-token scan on case2 outputs (both arms)
    for arm in IMPLS:
        paras = docx_paras(os.path.join(WORK, arm, t, "case2", "文书.docx"))
        bad = [p for p in paras if ("{" in p or "}" in p or "【" in p or "】" in p or "TODO" in p or "待填" in p)]
        print(f"[case2/{t}] {arm}: leftover-token paras = {bad if bad else 'NONE'}")
print("DIAG DONE")
