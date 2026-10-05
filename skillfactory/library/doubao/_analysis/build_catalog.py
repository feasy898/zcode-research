import os, re, json, io

ROOT = r"D:/workspace/zcode研究/skillfactory/library/doubao"
data = json.load(io.open(os.path.join(ROOT, "_analysis", "fm.json"), encoding="utf-8"))

def unq(s):
    if not isinstance(s, str):
        return s
    return s.strip().strip("'\"")

# category rules by name keyword
def cat(name):
    n = name
    if n.startswith("lark"): return "飞书协同"
    if n in ("word","ppt","sheet","html","doubao-pdf","artifact-preview"): return "文档办公"
    if "academic" in n or "journal" in n or "paper" in n or "research-proposal" in n or "reference-audit" in n or "critical-reading" in n: return "学术科研"
    if "medical" in n or "clinical" in n: return "医疗健康"
    if any(k in n for k in ("stock","earnings","finance","industry-analysis","private-company","public-company","wealth","daily-stock")) or n=="multi-stock-comparison": return "金融投研"
    if any(k in n for k in ("contract","dpa","patent","compliance","personal-info","marketing-material-review")): return "法律合规"
    if any(k in n for k in ("book","novel","newmedia","multiplatform","creative","headlines","cross-border-growth")): return "内容创作"
    if any(k in n for k in ("ecommerce","listing","product-","product-selection","customer-service","product-content","sentiment")): return "电商跨境"
    if n.startswith("byted-mediakit") or n.startswith("seed") or "video-extract" in n: return "媒体生成"
    if any(k in n for k in ("browser","computer-use")): return "浏览器/系统操作"
    if any(k in n for k in ("app-builder","cron","enterprise-search","identity","record","skill-creator","verifier","pc-optimizer")): return "平台工具"
    if any(k in n for k in ("market-hotspot","marketing-plan","oceanengine","announcement")): return "营销增长"
    return "其他"

def struct_feat(entries, file_count):
    e = set(entries)
    parts = []
    if "references" in e: parts.append("references/")
    if "reference" in e: parts.append("reference/")
    if "scripts" in e: parts.append("scripts/")
    if "agents" in e: parts.append("agents/")
    if "assets" in e: parts.append("assets/")
    if "sub-skills" in e: parts.append("sub-skills/")
    if "schemas" in e: parts.append("schemas/")
    if "evals" in e: parts.append("evals/")
    if "tests" in e: parts.append("tests/")
    if "config" in e: parts.append("config/")
    if "templates" in e: parts.append("templates/")
    if "scenes" in e: parts.append("scenes/")
    if "playbooks" in e: parts.append("playbooks/")
    if "branches" in e: parts.append("branches/")
    if file_count == 1: parts.append("单文件(仅SKILL.md)")
    elif not parts: parts.append("仅SKILL.md+散文件")
    return "+".join(parts) if parts else "?"

def fm_feats(fm):
    f = []
    if isinstance(fm.get("metadata"), dict):
        m = fm["metadata"]
        if "requires" in m: f.append("requires.bins 依赖声明")
        if "cliHelp" in m: f.append("cliHelp 探测命令")
        if "version" in m: f.append("metadata.version")
        if "hub" in m: f.append("hub 路由")
        if "product" in m: f.append("product/domain 归属")
        if "short-description" in m: f.append("short-description 短描述")
    if fm.get("license"): f.append("license 字段")
    if fm.get("permissions"): f.append("permissions 声明(" + ",".join(map(str, fm["permissions"])) + ")")
    if fm.get("compatibility"): f.append("compatibility 环境声明")
    if fm.get("version"): f.append("version 字段")
    return "；".join(f) + "（front-matter 完整度中上）" if f else "极简 front-matter，触发全靠 description"

rows = []
for r in sorted(data, key=lambda x: unq(x["fm"].get("name","zzz"))):
    fm = r["fm"]
    name = unq(fm.get("name",""))
    desc = unq(fm.get("description","")) or ""
    if not isinstance(desc, str): desc = json.dumps(desc, ensure_ascii=False)
    # first sentence
    first = re.split(r"(?:。|！|\n)", desc)[0][:120]
    ver = unq(fm.get("version","")) or unq(fm.get("metadata",{}).get("version","") if isinstance(fm.get("metadata"),dict) else "") or "—"
    lic = unq(fm.get("license","")) or "—"
    rows.append({
        "name": name, "ver": ver, "lic": lic, "cat": cat(name),
        "desc": first, "struct": struct_feat(r["entries"], r["file_count"]),
        "files": r["file_count"], "body_chars": r["body_chars"],
        "feat": fm_feats(fm), "dir": r["dir"],
        "desc_full": desc,
    })

json.dump(rows, io.open(os.path.join(ROOT, "_analysis", "catalog_rows.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows:", len(rows))
cats = {}
for x in rows: cats[x["cat"]] = cats.get(x["cat"], 0) + 1
for k, v in sorted(cats.items(), key=lambda kv: -kv[1]): print(k, v)
