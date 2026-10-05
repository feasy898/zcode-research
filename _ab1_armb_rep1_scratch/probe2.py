# -*- coding: utf-8 -*-
"""Targeted probes: styles.xml diff, sectPr diff, boilerplate presence, ledger dump."""
import sys, json, zipfile, hashlib, difflib
import xml.etree.ElementTree as ET
sys.path.insert(0, r"D:\workspace\zcode研究\_ab1_armb_rep1_scratch")
from abcompare import canon_xml, docx_structure, deep_diff, fmt

TEMPLATES = ["周报", "请示函", "会议通知", "工作总结"]
BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"

print("########## 1. styles.xml canonical diff (A=package, B=oracle) ##########")
for T in TEMPLATES:
    za = zipfile.ZipFile(BASE + rf"\package\out\{T}\case1\文书.docx")
    zb = zipfile.ZipFile(BASE + rf"\oracle\out\{T}\case1\文书.docx")
    sa, sb = canon_xml(za.read("word/styles.xml")), canon_xml(zb.read("word/styles.xml"))
    same_styles = sa == sb
    print(f"\n--- {T}: styles.xml canonical identical = {same_styles}")
    if not same_styles:
        da = sa.replace("><", ">\n<").splitlines()
        db = sb.replace("><", ">\n<").splitlines()
        for line in difflib.unified_diff(da, db, "A/package", "B/oracle", lineterm="", n=0):
            print("   " + line[:220])

print()
print("########## 2. sectPr (page setup) comparison ##########")
for T in TEMPLATES:
    A = docx_structure(BASE + rf"\package\out\{T}\case1\文书.docx")
    B = docx_structure(BASE + rf"\oracle\out\{T}\case1\文书.docx")
    sa = [b["xml"] for b in A["blocks"] if b["type"] == "sectPr"]
    sb = [b["xml"] for b in B["blocks"] if b["type"] == "sectPr"]
    print(f"--- {T}: sectPr count A={len(sa)} B={len(sb)}; canonical-identical={sa == sb}")
    if sa and sb and sa[0] != sb[0]:
        for line in difflib.unified_diff(sa[0].replace("><", ">\n<").splitlines(),
                                         sb[0].replace("><", ">\n<").splitlines(),
                                         "A/package", "B/oracle", lineterm="", n=0):
            print("   " + line[:220])

print()
print("########## 3. boilerplate / field-string presence in docx full text ##########")
NEEDLES = {
    "周报": ["部门：研发部", "填报人：王小明", "周期：2026-09-21 至 2026-09-27"],
    "请示函": ["现就有关事项请示如下：", "妥否，请批示。", "申请采购 V100S", "联系人：李工", "公司总经理办公会："],
    "会议通知": ["经研究，决定召开", "特此通知。", "一、会议时间", "五、会议要求", "会议议题：三季度"],
    "工作总结": ["一、工作回顾", "四、下一步工作打算"],
}
def fulltext(p):
    z = zipfile.ZipFile(p)
    root = ET.fromstring(z.read("word/document.xml"))
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    return "\n".join("".join(t.text or "" for t in p_.iter(W + "t")) for p_ in root.iter(W + "p"))
for T in TEMPLATES:
    ta = fulltext(BASE + rf"\package\out\{T}\case1\文书.docx")
    tb = fulltext(BASE + rf"\oracle\out\{T}\case1\文书.docx")
    print(f"--- {T}")
    for n in NEEDLES[T]:
        print(f"    {n!r:40} in-A={n in ta}  in-B={n in tb}")

print()
print("########## 4. fields.json ledger (B=oracle side; A verified identical except $.outputs paths) ##########")
for T in TEMPLATES:
    fa = json.load(open(BASE + rf"\package\out\{T}\case1\fields.json", encoding="utf-8"))
    fb = json.load(open(BASE + rf"\oracle\out\{T}\case1\fields.json", encoding="utf-8"))
    d = [x for x in deep_diff(fa, fb) if not x[0].startswith("$.outputs")]
    print(f"--- {T}: non-path diffs vs oracle = {len(d)}")
    print("    ledger B/oracle:")
    print("    " + json.dumps(fb, ensure_ascii=False, indent=2).replace("\n", "\n    ")[:1600])

print()
print("########## 5. package/out regeneration determinism (fresh vs pre-run backup) ##########")
for T in TEMPLATES:
    for f in ("文书.docx", "fields.json"):
        p_new = BASE + rf"\package\out\{T}\case1\{f}"
        p_old = r"D:\workspace\zcode研究\_ab1_armb_rep1_scratch\backup_package_out" + rf"\{T}\case1\{f}"
        import os
        if not os.path.exists(p_old):
            print(f"    {T}/{f}: no pre-existing copy (backup lacked it)")
            continue
        h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
        print(f"    {T}/{f}: fresh={h(p_new)} old={h(p_old)} identical={h(p_new)==h(p_old)}")
