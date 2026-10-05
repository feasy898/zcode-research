import os, re, json, io

ROOT = r"D:/workspace/zcode研究/skillfactory/library/doubao"
data = json.load(io.open(os.path.join(ROOT, "_analysis", "fm.json"), encoding="utf-8"))

for r in data:
    sm = os.path.join(ROOT, r["dir"], "SKILL.md")
    text = io.open(sm, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = m.group(1) if m else ""
    dm = re.search(r"^description:\s*(>?-?|\|)[ \t]*\n((?:[ \t]+.*\n?)*)", fm, re.M)
    if dm and dm.group(1).strip() in (">", ">-", "|", "|-"):
        block = dm.group(2)
        joined = re.sub(r"\s*\n\s*", " ", block).strip()
        r["fm"]["description"] = joined
        r["desc_block_scalar"] = True
    else:
        r["desc_block_scalar"] = False

json.dump(data, io.open(os.path.join(ROOT, "_analysis", "fm.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

import statistics
lens = [len(r["fm"]["description"]) for r in data if isinstance(r["fm"].get("description"), str)]
print("description 长度: n=%d min=%d median=%d max=%d" % (len(lens), min(lens), int(statistics.median(lens)), max(lens)))
print(">500字:", sum(1 for x in lens if x > 500), " 200-500字:", sum(1 for x in lens if 200 < x <= 500), " <200字:", sum(1 for x in lens if x <= 200))
