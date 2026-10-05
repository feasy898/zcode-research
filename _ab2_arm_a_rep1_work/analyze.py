# -*- coding: utf-8 -*-
"""ab2 arm-a/rep1 — artifact analysis. Inspects ONLY scratch copies produced by run_arms.py."""
import json, os, hashlib, zipfile, difflib
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WORK = r"D:\workspace\zcode研究\_ab2_arm_a_rep1_work"
TEMPLATES = ["请示函", "会议通知"]
REQUIRED = {
    "请示函": {"请示事由": 1, "主送机关": 1, "请示缘由": 1, "请示事项": 1, "请示单位": 1, "联系人": 0, "联系电话": 0, "成文日期": 0},
    "会议通知": {"会议名称": 1, "召开单位": 1, "主送对象": 1, "会议时间": 1, "会议地点": 1, "参会人员": 1,
             "会议议题": 0, "会议要求": 0, "联系人": 0, "联系电话": 0, "发文日期": 0},
}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def docx_paras(p):
    z = zipfile.ZipFile(p)
    root = ET.fromstring(z.read("word/document.xml"))
    return ["".join(t.text or "" for t in el.iter(W + "t")) for el in root.iter(W + "p")]

def deep_diff(a, b, path="$"):
    out = []
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        out.append((path, f"type {type(a).__name__}/{type(b).__name__}", a, b))
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: out.append((path + "." + k, "only-in-B", None, b[k]))
            elif k not in b: out.append((path + "." + k, "only-in-A", a[k], None))
            else: out += deep_diff(a[k], b[k], path + "." + k)
    elif isinstance(a, list):
        if len(a) != len(b): out.append((path, f"len {len(a)}/{len(b)}", a, b))
        for i, (x, y) in enumerate(zip(a, b)): out += deep_diff(x, y, f"{path}[{i}]")
    elif a != b:
        out.append((path, "value", a, b))
    return out

def fmt(v, limit=200):
    s = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    return s if len(s) <= limit else s[:limit] + f"...(+{len(s)-limit})"

for t in TEMPLATES:
    print("#" * 30, t, "case2", "#"*30)
    fa = json.load(open(rf"{WORK}\A\{t}\case2\fields.json", encoding="utf-8"))
    fb = json.load(open(rf"{WORK}\B\{t}\case2\fields.json", encoding="utf-8"))

    print(f"-- fields.json sha256 A={sha(rf'{WORK}\\A\\{t}\\case2\\fields.json')[:16]} B={sha(rf'{WORK}\\B\\{t}\\case2\\fields.json')[:16]} BYTE_IDENTICAL={sha(rf'{WORK}\\A\\{t}\\case2\\fields.json')==sha(rf'{WORK}\\B\\{t}\\case2\\fields.json')}")
    print("-- [B/oracle ledger full dump]")
    print(json.dumps(fb, ensure_ascii=False, indent=1))
    dd = deep_diff(fa, fb)
    print(f"-- [A vs B ledger deep-diff] {len(dd)} diff(s)")
    for p, kind, va, vb in dd: print(f"     {kind} @ {p}: A={fmt(va)} | B={fmt(vb)}")
    # modulo outputs
    dd2 = [d for d in dd if not d[0].startswith("$.outputs")]
    print(f"-- [A vs B ledger deep-diff modulo $.outputs] {'IDENTICAL' if not dd2 else str(len(dd2)) + ' diff(s): ' + '; '.join(d[0] for d in dd2)}")

    # internal consistency of each side's ledger
    for tag, j in (("A", fa), ("B", fb)):
        det = j["fields"]; names = [d["name"] for d in det]
        req_map = REQUIRED[t]
        filled = [d["name"] for d in det if d["status"] == "filled"]
        missing = [d["name"] for d in det if d["status"] == "missing"]
        s = j["summary"]
        ok1 = filled == j["filled_fields"] and missing == j["missing_fields"]
        mrn = [d["name"] for d in det if d["status"] == "missing" and d["required"]]
        ok2 = s["missing_required_names"] == mrn and s["missing_required"] == len(mrn)
        ok3 = s["total"] == len(det) == len(req_map) and s["filled"] == len(filled) and s["missing"] == len(missing) and s["filled"] + s["missing"] == s["total"]
        ok4 = all(d["required"] == bool(req_map[d["name"]]) for d in det)
        print(f"-- [{tag}] consistency: names_in_spec_order={names == list(req_map)} filled/missing_lists_match_status={ok1} missing_required_ok={ok2} counts_ok={ok3} required_flags_ok={ok4}")
        print(f"     [{tag}] status/value per field: " + " | ".join(f"{d['name']}:{d['status']}" + (f"={d['value']!r}" if d['status'] == 'filled' and isinstance(d.get('value'), str) and len(d.get('value') or '') <= 24 else (f"(len={len(d['value'])})" if d['status'] == 'filled' else "")) for d in det))
        print(f"     [{tag}] rendered_as of missing fields: " + " | ".join(f"{d['name']}->{d.get('rendered_as')!r}" for d in det if d["status"] == "missing"))
        print(f"     [{tag}] summary.unknown_keys={s.get('unknown_keys')} title={j.get('title')!r}")
        # empty-string fields must NOT be counted filled
        for fname in ("请示事项", "会议地点"):
            if fname in req_map:
                d = next(d for d in det if d["name"] == fname)
                if d["status"] == "filled": print(f"     [{tag}] !! EMPTY-STRING FIELD {fname} counted as FILLED (value={d.get('value')!r})")

    # docx text comparison
    ta = docx_paras(rf"{WORK}\A\{t}\case2\文书.docx")
    tb = docx_paras(rf"{WORK}\B\{t}\case2\文书.docx")
    print(f"-- docx paragraphs: A={len(ta)} B={len(tb)}  (A empty paras: {[i for i,x in enumerate(ta) if not x.strip()]}  B empty paras: {[i for i,x in enumerate(tb) if not x.strip()]})")
    print("-- [A/技能 docx full text] (empty paras skipped)")
    for i, p in enumerate(ta):
        if p.strip(): print(f"     A{i:02d}| {p}")
    print("-- [B/oracle docx full text] (empty paras skipped)")
    for i, p in enumerate(tb):
        if p.strip(): print(f"     B{i:02d}| {p}")
    ta_ne = [x for x in ta if x.strip()]; tb_ne = [x for x in tb if x.strip()]
    print(f"-- non-empty para sequences equal: {ta_ne == tb_ne}")
    print("-- [A vs B docx text diff] (unified, only non-empty lines)")
    dl = list(difflib.unified_diff(tb_ne, ta_ne, "B/oracle", "A/技能", lineterm="", n=0))
    if not dl: print("     IDENTICAL text content")
    for l in dl[:40]: print("     " + l)
    # fabrication scan: placeholders look like ____ / （  ） / blanks; flag digits/phones/dates near missing-field lines
    print("-- fabrication heuristic scan (lines containing ____ or 【 or placeholder marks, plus any digit-runs):")
    for tag, tx in (("A", ta), ("B", tb)):
        hits = []
        for p in tx:
            if any(m in p for m in ("____", "＿＿", "【", "XXX", "xx", "（此处", "(此处")) or any(c.isdigit() for c in p):
                hits.append(p)
        for h in hits: print(f"     [{tag}] {h}")
    print()
print("ANALYSIS DONE")
