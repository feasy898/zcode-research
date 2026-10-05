# -*- coding: utf-8 -*-
"""ab2 arm-a rep2 comparator: oracle vs package on 请示函/case2 + 会议通知/case2.
Prints derived findings only: input fixture structure, full ledgers, deep diffs,
docx paragraph text, placeholder/fabrication needle checks, determinism vs backup.
"""
import hashlib, json, os, zipfile
import xml.etree.ElementTree as ET

SCR  = r"D:\workspace\zcode研究\_ab2_arma_rep2_scratch"
BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
CASES = [("请示函", "case2"), ("会议通知", "case2")]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

def deep_diff(a, b, path="$"):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append(f"{path}.{k}: ONLY_IN_package = {b[k]!r}")
            elif k not in b:
                out.append(f"{path}.{k}: ONLY_IN_oracle = {a[k]!r}")
            else:
                out += deep_diff(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path}: LEN oracle={len(a)} package={len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            out += deep_diff(x, y, f"{path}[{i}]")
    else:
        if a != b:
            out.append(f"{path}: oracle={a!r} vs package={b!r}")
    return out

def docx_paras(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    return ["".join(t.text or "" for t in p.iter(W + "t")) for p in root.iter(W + "p")]

def value_profile(v):
    if v is None: return "null"
    if isinstance(v, str):
        if v == "": return "EMPTY_STRING"
        return f"str({v!r})"
    return f"{type(v).__name__}({v!r})"

for t, c in CASES:
    print("=" * 100)
    print(f"### {t} / {c}")
    inp = os.path.join(BASE, "oracle", "inputs", t, f"{c}.json")
    ind = json.load(open(inp, encoding="utf-8"))
    print(f"-- input fixture keys/profile (via harness):")
    for k in ind:
        print(f"     {k}: {value_profile(ind[k])}")

    led = {}
    for side in ("oracle", "package"):
        p = os.path.join(SCR, "out", side, t, c, "fields.json")
        led[side] = json.load(open(p, encoding="utf-8"))
        d = os.path.join(SCR, "out", side, t, c, "文书.docx")
        led[side]["__docx_paras__"] = docx_paras(d)

    print(f"-- ledger ORACLE (full, outputs paths elided):")
    oj = {k: v for k, v in led["oracle"].items() if k != "outputs"}
    print("   " + json.dumps(oj, ensure_ascii=False, indent=1).replace("\n", "\n   "))
    print(f"-- ledger PACKAGE (full, outputs paths elided):")
    pj = {k: v for k, v in led["package"].items() if k != "outputs"}
    print("   " + json.dumps(pj, ensure_ascii=False, indent=1).replace("\n", "\n   "))

    dj = [x for x in deep_diff(led["oracle"], led["package"]) if not x.startswith("$.outputs")]
    print(f"-- ledger deep-diff oracle vs package (excl $.outputs): {len(dj)} diff(s)")
    for line in dj:
        print("     " + line)

    print(f"-- docx ORACLE paragraphs:")
    for i, s in enumerate(led["oracle"]["__docx_paras__"]):
        print(f"     ORC P{i:02d}: {s!r}")
    print(f"-- docx PACKAGE paragraphs:")
    for i, s in enumerate(led["package"]["__docx_paras__"]):
        print(f"     PKG P{i:02d}: {s!r}")

    # fabrication needle checks: values that are PRESENT in input must appear;
    # for missing/empty fields, no plausible-looking invented content markers
    print("-- needle checks:")
    filled = led["package"].get("filled_fields", [])
    missing = led["package"].get("missing_fields", [])
    alltext_pkg = "\n".join(led["package"]["__docx_paras__"])
    alltext_orc = "\n".join(led["oracle"]["__docx_paras__"])
    ph_marks = ["____", "__", "【", "（待", "(待", "待补", "待填", "××", "XX", "TBD", "N/A", "—"]
    print(f"     package filled_fields={filled}")
    print(f"     package missing_fields={missing}")
    print(f"     oracle filled_fields={led['oracle'].get('filled_fields')}")
    print(f"     oracle missing_fields={led['oracle'].get('missing_fields')}")
    for m in ph_marks:
        cp, co = alltext_pkg.count(m), alltext_orc.count(m)
        if cp or co:
            print(f"     placeholder marker {m!r}: package={cp} oracle={co}")

    # determinism vs pre-run backups
    print("-- determinism (fresh scratch run vs pre-existing skillfactory out backup):")
    for side in ("oracle", "package"):
        for f in ("文书.docx", "fields.json"):
            fresh = os.path.join(SCR, "out", side, t, c, f)
            old = os.path.join(SCR, "backup", side, t, c, f)
            if os.path.exists(old):
                print(f"     {side}/{f}: fresh={sha(fresh)} backup={sha(old)} equal={sha(fresh)==sha(old)}")
            else:
                print(f"     {side}/{f}: no backup")
print("=" * 100)
print("COMPARE DONE")
