# -*- coding: utf-8 -*-
"""A/B artifact comparator for ab1-standard-four-templates (arm-b/rep1).

Compares two case output dirs (each holding 文书.docx + fields.json):
  1. sha256 byte-level
  2. zip entry inventory
  3. per-XML-part canonical comparison (parse + re-serialize, order-preserving)
  4. semantic document.xml diff (blocks: paragraph/table, with formatting)
  5. fields.json deep diff (only differing paths printed)

Prints a bounded report. Never dumps whole files.
"""
import sys, json, hashlib, zipfile, io
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def canon_xml(data: bytes) -> str:
    def sort_attr(el):
        el.attrib = dict(sorted(el.attrib.items()))
        for c in el:
            sort_attr(c)
    root = ET.fromstring(data)
    sort_attr(root)
    # strip volatile metadata in core.xml
    if root.tag.endswith("}coreProperties"):
        for t in list(root):
            if t.tag.split("}")[1] in ("created", "modified", "lastModifiedBy", "revision"):
                root.remove(t)
    return ET.tostring(root, encoding="unicode")

def run_props(r):
    rPr = r.find(W + "rPr")
    props = {}
    if rPr is None:
        return props
    for ch in rPr:
        tag = ch.tag.split("}")[1]
        if tag == "rFonts":
            props["font"] = {k.split("}")[1]: v for k, v in ch.attrib.items()}
        elif tag in ("sz", "szCs"):
            props[tag] = ch.attrib.get(W + "val")
        elif tag == "b":
            props["bold"] = ch.attrib.get(W + "val", "1")
        elif tag in ("color",):
            props[tag] = ch.attrib.get(W + "val")
        else:
            props[tag] = dict(ch.attrib)
    return props

def para_props(p):
    pPr = p.find(W + "pPr")
    props = {}
    if pPr is None:
        return props
    for ch in pPr:
        tag = ch.tag.split("}")[1]
        if tag == "pStyle":
            props["style"] = ch.attrib.get(W + "val")
        elif tag == "jc":
            props["align"] = ch.attrib.get(W + "val")
        elif tag in ("spacing", "ind", "numPr"):
            def flat(e):
                d = {}
                for c in e:
                    d[c.tag.split("}")[1]] = {k.split("}")[1]: v for k, v in c.attrib.items()} or c.attrib.get(W+"val")
                return d or dict((k.split("}")[1], v) for k, v in e.attrib.items())
            props[tag] = flat(ch)
        else:
            props[tag] = dict((k.split("}")[1], v) for k, v in ch.attrib.items())
    return props

def docx_structure(path):
    z = zipfile.ZipFile(path)
    names = sorted(z.namelist())
    doc = z.read("word/document.xml")
    root = ET.fromstring(doc)
    body = root.find(W + "body")
    blocks = []
    def runs_of(p):
        rs = []
        for r in p.findall(W + "r"):
            t = "".join(t.text or "" for t in r.findall(W + "t"))
            rs.append({"text": t, "props": run_props(r)})
        return rs
    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            txt = "".join(t.text or "" for t in el.iter(W + "t"))
            blocks.append({"type": "p", "text": txt, "pPr": para_props(el), "runs": runs_of(el)})
        elif tag == "tbl":
            rows = []
            for tr in el.findall(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    ctxt = "\n".join("".join(t.text or "" for t in p.iter(W + "t")) for p in tc.findall(W + "p"))
                    tcPr = tc.find(W + "tcPr")
                    cprops = {}
                    if tcPr is not None:
                        for ch in tcPr:
                            cprops[ch.tag.split("}")[1]] = dict((k.split("}")[1], v) for k, v in ch.attrib.items())
                    cells.append({"text": ctxt, "tcPr": cprops})
                rows.append(cells)
            grid = [g.attrib.get(W + "w") for g in el.findall(W + "tblGrid/" + W + "gridCol")]
            tblPr = el.find(W + "tblPr")
            tprops = {}
            if tblPr is not None:
                for ch in tblPr:
                    tprops[ch.tag.split("}")[1]] = dict((k.split("}")[1], v) for k, v in ch.attrib.items())
            blocks.append({"type": "tbl", "grid": grid, "tblPr": tprops, "rows": rows})
        elif tag == "sectPr":
            blocks.append({"type": "sectPr", "xml": canon_xml(ET.tostring(el, encoding="utf-8"))})
    part_canon = {}
    for n in names:
        if n.endswith(".xml") or n.endswith(".rels"):
            try:
                part_canon[n] = canon_xml(z.read(n))
            except ET.ParseError:
                part_canon[n] = "<unparseable>"
    return {"zip_names": names, "sha_docx": sha256(path), "blocks": blocks, "part_canon": part_canon}

def deep_diff(a, b, path="$", out=None):
    if out is None:
        out = []
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        out.append((path, f"type {type(a).__name__} vs {type(b).__name__}", a, b))
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((path + "." + k, "only-in-B", None, b[k]))
            elif k not in b:
                out.append((path + "." + k, "only-in-A", a[k], None))
            else:
                deep_diff(a[k], b[k], path + "." + k, out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, f"len {len(a)} vs {len(b)}", f"list(len={len(a)})", f"list(len={len(b)})"))
        for i, (x, y) in enumerate(zip(a, b)):
            deep_diff(x, y, f"{path}[{i}]", out)
    else:
        if a != b:
            out.append((path, "value", a, b))
    return out

def fmt(v, limit=120):
    s = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    return s if len(s) <= limit else s[:limit] + f"...(+{len(s)-limit} chars)"

def compare_pair(label, dir_a, dir_b, name_a="A", name_b="B"):
    print("=" * 100)
    print(f"[{label}]  A={name_a}: {dir_a}")
    print(f"{' '*len(label)}  B={name_b}: {dir_b}")
    da, db = dir_a + "/文书.docx", dir_b + "/文书.docx"
    fa, fb = dir_a + "/fields.json", dir_b + "/fields.json"
    A, B = docx_structure(da), docx_structure(db)
    print(f"-- docx sha256: A={A['sha_docx'][:16]}… B={B['sha_docx'][:16]}…  byte-identical={A['sha_docx']==B['sha_docx']}")
    if set(A["zip_names"]) != set(B["zip_names"]):
        print(f"-- zip entries differ: only-A={sorted(set(A['zip_names'])-set(B['zip_names']))} only-B={sorted(set(B['zip_names'])-set(A['zip_names']))}")
    else:
        print(f"-- zip entries: {len(A['zip_names'])} parts, name sets identical")
    noncanon = [n for n in A["part_canon"] if n in B["part_canon"] and A["part_canon"][n] != B["part_canon"][n]]
    only_a = [n for n in A["part_canon"] if n not in B["part_canon"]]
    print(f"-- canonical-XML identical parts: {len([n for n in A['part_canon'] if n in B['part_canon'] and A['part_canon'][n]==B['part_canon'][n]])}/{len(A['part_canon'])}; differing: {noncanon if noncanon else 'NONE'}; only-in-A: {only_a or 'none'}")
    # semantic block diff
    ba, bb = A["blocks"], B["blocks"]
    print(f"-- document body blocks: A={len(ba)} B={len(bb)}", "(equal count)" if len(ba) == len(bb) else "<< COUNT MISMATCH")
    ndiff = 0
    for i in range(max(len(ba), len(bb))):
        x = ba[i] if i < len(ba) else None
        y = bb[i] if i < len(bb) else None
        if x is None or y is None:
            print(f"   block#{i}: MISSING in {'A' if x is None else 'B'}; other side: {fmt(x or y)}")
            ndiff += 1
            continue
        d = deep_diff(x, y)
        if d:
            ndiff += 1
            print(f"   block#{i} ({x['type']}): {len(d)} prop diffs — text A={fmt(x.get('text',''))!r} B={fmt(y.get('text',''))!r}")
            for p, kind, va, vb in d[:8]:
                print(f"      · {kind} @ {p}: A={fmt(va)} | B={fmt(vb)}")
            if len(d) > 8:
                print(f"      · … {len(d)-8} more diffs in this block")
    if ndiff == 0:
        print("   semantic document structure: IDENTICAL (all blocks, texts, alignment, fonts, sizes, tables, sectPr)")
    # fields.json
    ja, jb = json.load(open(fa, encoding="utf-8")), json.load(open(fb, encoding="utf-8"))
    fd = deep_diff(ja, jb)
    if not fd:
        print(f"-- fields.json: IDENTICAL (top-level keys: {sorted(ja) if isinstance(ja, dict) else type(ja).__name__})")
    else:
        print(f"-- fields.json: {len(fd)} DIFFS")
        for p, kind, va, vb in fd:
            print(f"   · {kind} @ {p}: A={fmt(va)} | B={fmt(vb)}")
    print()
    return {"byte_identical_docx": A["sha_docx"] == B["sha_docx"], "fields_diffs": len(fd), "block_diffs": ndiff}

if __name__ == "__main__":
    compare_pair(sys.argv[1], sys.argv[2], sys.argv[3])
