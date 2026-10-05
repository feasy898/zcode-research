# -*- coding: utf-8 -*-
"""ab3-empty-and-string-lists / arm-b / rep2 — artifact comparator.

Reads ONLY the four output dirs produced into this scratch dir
(A=<被测技能 gen_doc.py>, B=<参照实现 oracle.py>).
Dumps, per template: ordered docx blocks (paragraph texts / table cell texts)
for A and B verbatim, a block-level A-vs-B diff, and a fields.json deep diff.
"""
import json, os, zipfile, difflib
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WORK = r"D:\workspace\zcode研究\_ab3_armb_rep2_work"
TEMPLATES = ["周报", "工作总结"]


def blocks_of(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    out = []
    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            txt = "".join(t.text or "" for t in el.iter(W + "t"))
            num = el.find(W + "pPr/" + W + "numPr")
            out.append(("p", ("• " if num is not None else "") + txt))
        elif tag == "tbl":
            for ri, tr in enumerate(el.findall(W + "tr")):
                cells = [" / ".join("".join(t.text or "" for t in p.iter(W + "t"))
                                    for p in tc.findall(W + "p")) for tc in tr.findall(W + "tc")]
                out.append(("tbl", f"row{ri}: " + " | ".join(cells)))
    return out


def jdiff(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append(f"{path}/{k}: ONLY_IN_B = {b[k]!r}")
            elif k not in b:
                out.append(f"{path}/{k}: ONLY_IN_A = {a[k]!r}")
            else:
                out += jdiff(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path}: LIST_LEN A={len(a)} B={len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            out += jdiff(x, y, f"{path}[{i}]")
    elif type(a) is not type(b):
        out.append(f"{path}: TYPE A={type(a).__name__}:{a!r} B={type(b).__name__}:{b!r}")
    elif a != b:
        out.append(f"{path}: A={a!r} B={b!r}")
    return out


for t in TEMPLATES:
    da = os.path.join(WORK, "A", t, "case2", "文书.docx")
    db = os.path.join(WORK, "B", t, "case2", "文书.docx")
    fa = os.path.join(WORK, "A", t, "case2", "fields.json")
    fb = os.path.join(WORK, "B", t, "case2", "fields.json")
    BA, BB = blocks_of(da), blocks_of(db)
    print("=" * 100)
    print(f"##### {t} / case2 — docx blocks (verbatim, scratch copies) #####")
    for side, B in (("A", BA), ("B", BB)):
        print(f"--- {side} ({len(B)} blocks) ---")
        for i, (kind, txt) in enumerate(B):
            print(f"  {i:02d} [{kind}] {txt!r}")
    print(f"--- A-vs-B block diff ---")
    la = [f"{k}:{x}" for k, x in BA]
    lb = [f"{k}:{x}" for k, x in BB]
    dl = list(difflib.unified_diff(la, lb, "A", "B", lineterm="", n=0))
    print("\n".join(dl[2:]) if len(dl) > 2 else "  (no textual block differences)")
    ja, jb = json.load(open(fa, encoding="utf-8")), json.load(open(fb, encoding="utf-8"))
    print(f"--- fields.json A-vs-B deep diff ({len(jdiff(ja, jb))} diffs) ---")
    for line in jdiff(ja, jb):
        print(f"  · {line}")
    print()
print("DONE")
