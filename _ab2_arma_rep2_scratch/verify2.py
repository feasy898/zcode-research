# -*- coding: utf-8 -*-
"""ab2 follow-up checks: (1) content-level determinism (backup vs fresh,
ignoring $.outputs paths and docx zip timestamps); (2) fabrication needles;
(3) rendered_as self-consistency per side."""
import json, os, re, zipfile
import xml.etree.ElementTree as ET

SCR  = r"D:\workspace\zcode研究\_ab2_arma_rep2_scratch"
BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
CASES = [("请示函", "case2"), ("会议通知", "case2")]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def strip_outputs(d):
    return {k: v for k, v in d.items() if k != "outputs"}

def docx_text(p):
    z = zipfile.ZipFile(p)
    root = ET.fromstring(z.read("word/document.xml"))
    return "\n".join("".join(t.text or "" for t in par.iter(W + "t")) for par in root.iter(W + "p"))

print("##### 1. content-level determinism: pre-existing backup vs fresh scratch run #####")
for t, c in CASES:
    for side in ("oracle", "package"):
        lb = json.load(open(os.path.join(SCR, "backup", side, t, c, "fields.json"), encoding="utf-8"))
        lf = json.load(open(os.path.join(SCR, "out", side, t, c, "fields.json"), encoding="utf-8"))
        same_ledger = strip_outputs(lb) == strip_outputs(lf)
        tb = docx_text(os.path.join(SCR, "backup", side, t, c, "文书.docx"))
        tf = docx_text(os.path.join(SCR, "out", side, t, c, "文书.docx"))
        same_text = tb == tf
        print(f"  {t}/{side}: ledger_identical_modulo_outputs={same_ledger}  docx_text_identical={same_text}")
        if not same_ledger:
            print(f"    backup ledger keys={sorted(lb)}")
            print(f"    backup summary={json.dumps(lb.get('summary'), ensure_ascii=False)}")
        if not same_text:
            print(f"    backup text: {tb!r}"[:400])
            print(f"    fresh  text: {tf!r}"[:400])

print()
print("##### 2. fabrication needles on fresh docx text #####")
PHONE = re.compile(r"(?:\d{3,4}-\d{7,8})|(?:1\d{10})")
DATE  = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")
for t, c in CASES:
    for side in ("oracle", "package"):
        txt = docx_text(os.path.join(SCR, "out", side, t, c, "文书.docx"))
        phones, dates = PHONE.findall(txt), DATE.findall(txt)
        leak = "此键不在模板字段内" in txt
        print(f"  {t}/{side}: phone_like={phones} date_like={dates} 备注_value_leaked={leak} "
              f"____count={txt.count('____')}")

print()
print("##### 3. rendered_as self-consistency (ledger claim vs actual docx) #####")
EXPECT = {
    ("请示函", "主送机关"): ("____：", "以____占位"),
    ("请示函", "请示事项"): ("____", "以____占位"),
    ("请示函", "联系电话"): ("联系电话：", "留空（渲染为空字符串）"),
    ("会议通知", "会议名称"): ("____", "以____占位"),
    ("会议通知", "会议地点"): ("会议地点：____", "以____占位"),
    ("会议通知", "会议议题"): ("会议议题：", "留空（渲染为空字符串）"),
    ("会议通知", "联系人"):   ("联系人：", "留空（渲染为空字符串）"),
}
for (t, fname), (needle, claim) in EXPECT.items():
    row = [f"  {t}/{fname} claim={claim!r}"]
    for side in ("oracle", "package"):
        txt = docx_text(os.path.join(SCR, "out", side, t, c := "case2", "文书.docx"))
        row.append(f"{side}→{needle!r} in_text={needle in txt}")
    print("; ".join(row))
# list-kind omission check
for side in ("oracle", "package"):
    txt = docx_text(os.path.join(SCR, "out", side, "会议通知", "case2", "文书.docx"))
    print(f"  会议通知/{side}: 会议要求 label present={'会议要求' in txt} (claim: 省略该条目/小节)")
print("VERIFY2 DONE")
