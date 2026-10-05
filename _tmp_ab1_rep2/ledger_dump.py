# -*- coding: utf-8 -*-
"""Dump field ledgers (derived facts only) and characterize fresh-vs-backup nondeterminism."""
import json, difflib, zipfile, hashlib
BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
BAK  = r"D:\workspace\zcode研究\_tmp_ab1_rep2\backup2"
TMPLS = ["周报", "请示函", "会议通知", "工作总结"]

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

for T in TMPLS:
    j = load(rf"{BASE}\package\out\{T}\case1\fields.json")
    print(f"== {T} package fields.json ledger ==")
    print("  template:", j.get("template"), "| title:", j.get("title"))
    print("  filled:", j.get("filled_fields"), "| missing:", j.get("missing_fields"))
    print("  summary:", j.get("summary"))
    f = j.get("fields")
    if isinstance(f, dict):
        for k, v in f.items():
            print(f"    {k} = {v!r}")
    else:
        for item in (f or []):
            print(f"    {item!r}")
print()
print("#### oracle fresh-vs-backup fields.json diff (what is nondeterministic) ####")
for T in TMPLS:
    a = load(rf"{BAK}\oracle_out\{T}\case1\fields.json")
    b = load(rf"{BASE}\oracle\out\{T}\case1\fields.json")
    sa = json.dumps(a, ensure_ascii=False, indent=1, sort_keys=True).splitlines()
    sb = json.dumps(b, ensure_ascii=False, indent=1, sort_keys=True).splitlines()
    dl = [l for l in difflib.unified_diff(sa, sb, lineterm="")
          if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    print(f"-- {T}: {len(dl)} changed line(s)")
    for l in dl[:12]:
        print("   ", l)
print()
print("#### package fresh-vs-backup docx: is diff only zip metadata? ####")
for T in TMPLS:
    za = zipfile.ZipFile(rf"{BAK}\package_out\{T}\case1\文书.docx")
    zb = zipfile.ZipFile(rf"{BASE}\package\out\{T}\case1\文书.docx")
    na = {i.filename: i.date_time for i in za.infolist()}
    nb = {i.filename: i.date_time for i in zb.infolist()}
    same_names = set(na) == set(nb)
    content_diff = [n for n in sorted(set(na) & set(nb))
                    if hashlib.sha256(za.read(n)).hexdigest() != hashlib.sha256(zb.read(n)).hexdigest()]
    time_only = [n for n in sorted(set(na) & set(nb)) if na[n] != nb[n]]
    print(f"-- {T}: entry_names_equal={same_names} content-diff entries={content_diff} time-only-diff entries={len(time_only)}")
