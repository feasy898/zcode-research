import os, re, json, io

ROOT = r"D:/workspace/zcode研究/skillfactory/library/doubao"
out = []
for d in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, d)
    if not os.path.isdir(p) or not d.startswith("skill-"):
        continue
    sm = os.path.join(p, "SKILL.md")
    if not os.path.exists(sm):
        continue
    text = io.open(sm, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = m.group(1) if m else ""
    body = text[m.end():] if m else text
    rec = {"dir": d, "fm_raw_lines": fm.count("\n")+1 if fm else 0,
           "body_lines": body.count("\n")+1, "body_chars": len(body),
           "total_chars": len(text)}
    keys = {}
    cur_top = None
    for line in fm.splitlines():
        if not line.strip():
            continue
        top = re.match(r"^([A-Za-z_][\w-]*):(.*)$", line)
        subitem = re.match(r"^\s+([A-Za-z_][\w-]*):(.*)$", line)
        listitem = re.match(r"^\s*-\s*(.*)$", line)
        if top:
            cur_top = top.group(1)
            val = top.group(2).strip()
            keys[cur_top] = val if val else {}
        elif subitem and cur_top:
            if not isinstance(keys.get(cur_top), dict):
                keys[cur_top] = {}
            keys[cur_top][subitem.group(1)] = subitem.group(2).strip()
        elif listitem and cur_top:
            cur = keys.get(cur_top)
            if isinstance(cur, list):
                cur.append(listitem.group(1).strip())
            elif isinstance(cur, dict) and not cur:
                keys[cur_top] = [listitem.group(1).strip()]
            elif isinstance(cur, dict):
                cur.setdefault("_list", []).append(listitem.group(1).strip())
    rec["fm"] = keys
    rec["entries"] = sorted(os.listdir(p))
    n = 0
    for r, _, files in os.walk(p):
        n += len(files)
    rec["file_count"] = n
    out.append(rec)

json.dump(out, io.open(os.path.join(ROOT, "_analysis", "fm.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("parsed", len(out))
