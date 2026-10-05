# -*- coding: utf-8 -*-
"""ab3 arm-b/rep1 — artifact analysis. Inspects ONLY scratch copies produced by run_ab3.py.

Focus: list-field boundary behavior (占位条目 / 省略 / 字符串单项化) per side:
  A = 被测技能 gen_doc.py   B = 参照实现 oracle.py
"""
import difflib, hashlib, json, os, re, zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WORK = r"D:\workspace\zcode研究\_ab3_armb_rep1_work"
TEMPLATES = ["周报", "工作总结"]
SCHEMA = {
    "周报": [("部门", 1, "text"), ("填报人", 1, "text"), ("周期", 1, "text"),
           ("本周工作内容", 1, "list"), ("下周工作计划", 1, "list"),
           ("问题与需协调事项", 0, "list"), ("报送日期", 0, "text")],
    "工作总结": [("总结主体", 1, "text"), ("总结时段", 1, "text"), ("工作回顾", 1, "list"),
             ("主要成绩", 1, "list"), ("存在问题", 0, "list"),
             ("下一步工作打算", 1, "list"), ("成文日期", 0, "text")],
}
FOCUS = {  # input shape per ask
    "周报": {"周期": "required text = empty string", "本周工作内容": "required list = empty array",
           "问题与需协调事项": "optional list ABSENT", "部门": "required text ABSENT (not in ask, found in input)"},
    "工作总结": {"总结主体": "required text ABSENT", "工作回顾": "required list given as STRING",
             "主要成绩": "required list = empty array", "存在问题": "optional list ABSENT",
             "成文日期": "optional text ABSENT"},
}
HEAD = re.compile(r"^[一二三四五六七八九十]+、")

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

def sections(paras):
    """map section header -> list of following item paragraphs (until next header / 报送|成文 line)."""
    secs, cur = {}, None
    for p in paras:
        if HEAD.match(p):
            cur = p
            secs[cur] = []
        elif cur is not None:
            if re.match(r"^(报送日期|成文日期)[:：]", p):
                cur = None
            else:
                secs[cur].append(p)
    return secs

for t in TEMPLATES:
    print("#" * 34, t, "case2", "#" * 34)
    led = {}
    for tag in ("A", "B"):
        d = os.path.join(WORK, tag, t, "case2")
        led[tag] = json.load(open(os.path.join(d, "fields.json"), encoding="utf-8"))
        print(f"[{tag}] docx sha256={sha(os.path.join(d, '文书.docx'))[:16]}  fields.json sha256={sha(os.path.join(d, 'fields.json'))[:16]}")
    print(f"-- docx byte-identical A==B: {sha(os.path.join(WORK,'A',t,'case2','文书.docx')) == sha(os.path.join(WORK,'B',t,'case2','文书.docx'))}")
    print(f"-- fields.json byte-identical A==B: {sha(os.path.join(WORK,'A',t,'case2','fields.json')) == sha(os.path.join(WORK,'B',t,'case2','fields.json'))}")

    dd = deep_diff(led["A"], led["B"])
    dd2 = [x for x in dd if not x[0].startswith("$.outputs")]
    print(f"-- ledger deep-diff A vs B modulo $.outputs: {'IDENTICAL' if not dd2 else str(len(dd2)) + ' diff(s)'}")
    for p_, kind, va, vb in dd2:
        s = json.dumps(va, ensure_ascii=False) if isinstance(va, (dict, list)) else repr(va)
        z = json.dumps(vb, ensure_ascii=False) if isinstance(vb, (dict, list)) else repr(vb)
        print(f"     {kind} @ {p_}: A={s} | B={z}")

    # ledger dump (focus fields) + consistency, per side
    for tag in ("A", "B"):
        j = led[tag]
        det = j["fields"]
        names = [d["name"] for d in det]
        req_map = {n: r for n, r, _ in SCHEMA[t]}
        kinds = {n: k for n, _, k in SCHEMA[t]}
        filled = [d["name"] for d in det if d["status"] == "filled"]
        missing = [d["name"] for d in det if d["status"] == "missing"]
        s = j["summary"]
        ok1 = filled == j["filled_fields"] and missing == j["missing_fields"]
        mrn = [d["name"] for d in det if d["status"] == "missing" and d["required"]]
        ok2 = s.get("missing_required_names") == mrn and s.get("missing_required") == len(mrn)
        ok3 = (s.get("total") == len(det) == len(req_map) and s.get("filled") == len(filled)
               and s.get("missing") == len(missing) and s.get("filled", 0) + s.get("missing", 0) == s.get("total"))
        ok4 = all(d["required"] == bool(req_map[d["name"]]) for d in det)
        ok5 = all(d.get("kind") == kinds[d["name"]] for d in det)
        print(f"-- [{tag}] consistency: names_in_spec_order={names == list(req_map)} filled/missing_lists_match={ok1} "
              f"missing_required_ok={ok2} counts_ok={ok3} required_flags_ok={ok4} kinds_ok={ok5}")
        print(f"     [{tag}] title={j.get('title')!r} summary.unknown_keys={s.get('unknown_keys')}")
        print(f"     [{tag}] FOCUS ledger entries (input shape -> how the side recorded it):")
        for d in det:
            if d["name"] in FOCUS[t]:
                v = d.get("value", "<none>")
                vs = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else repr(v)
                extra = "".join(f" {k}={d[k]!r}" for k in sorted(d) if k not in ("name", "status", "required", "kind", "value"))
                print(f"        {d['name']:<10} [{FOCUS[t][d['name']]}] -> status={d['status']} value={vs}{extra}")

    # docx text: full dump + section-aware classification
    texts = {tag: docx_paras(os.path.join(WORK, tag, t, "case2", "文书.docx")) for tag in ("A", "B")}
    for tag in ("A", "B"):
        print(f"-- [{tag}] docx full text (non-empty paras):")
        for i, p in enumerate(texts[tag]):
            if p.strip():
                print(f"     {tag}{i:02d}| {p}")
    for tag in ("A", "B"):
        print(f"-- [{tag}] section map (header -> items):")
        for h, items in sections(texts[tag]).items():
            print(f"     {h!r} -> {len(items)} item(s): {items!r}")
    ta_ne = [x for x in texts["A"] if x.strip()]
    tb_ne = [x for x in texts["B"] if x.strip()]
    print(f"-- non-empty para sequences equal: {ta_ne == tb_ne}")
    dl = list(difflib.unified_diff(tb_ne, ta_ne, "B/oracle", "A/skill", lineterm="", n=0))
    print("-- [A vs B docx text unified diff]" + ("  IDENTICAL text content" if not dl else f"  {len(dl)} lines:"))
    for l in dl[:60]:
        print("     " + l)
    print()
print("ANALYSIS DONE")
