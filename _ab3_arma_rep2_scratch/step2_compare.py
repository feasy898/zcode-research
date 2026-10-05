# -*- coding: utf-8 -*-
"""ab3/arm-a/rep2 step2: deep-compare ledgers + docx paragraphs, list-behavior probes."""
import json, os, re, sys, itertools

sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
SCR = r"D:\workspace\zcode研究\_ab3_arma_rep2_scratch"
TPLS = ["周报", "工作总结"]

def strip_paths(o, key_sub=("docx", "fields", "path", "outdir")):
    """Recursive: blank out any string containing an absolute path marker."""
    if isinstance(o, dict):
        return {k: ("<PATH>" if isinstance(v, str) and ("zcode研究" in v or ":\\workspace" in v) else strip_paths(v, key_sub)) for k, v in o.items()}
    if isinstance(o, list):
        return [("<PATH>" if isinstance(v, str) and ("zcode研究" in v or ":\\workspace" in v) else strip_paths(v, key_sub)) for v in o]
    return o

def deep_diff(a, b, path="$"):
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: diffs.append(f"{path}.{k}: 只在 package 侧存在 = {b[k]!r}")
            elif k not in b: diffs.append(f"{path}.{k}: 只在 oracle 侧存在 = {a[k]!r}")
            else: diffs += deep_diff(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append(f"{path}: 长度 {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            diffs += deep_diff(x, y, f"{path}[{i}]")
    else:
        if a != b:
            diffs.append(f"{path}: oracle={a!r} vs package={b!r}")
    return diffs

def docx_paras(p):
    from docx import Document
    d = Document(p)
    out = []
    for para in d.paragraphs:
        pf = para.paragraph_format
        ind = pf.first_line_indent
        out.append({
            "text": para.text,
            "align": str(pf.alignment),
            "firstLineIndent": (str(ind) if ind is not None else None),
            "style": para.style.name if para.style is not None else None,
        })
    return out

report = []
for tpl in TPLS:
    print("=" * 100)
    print(f"### 模板 {tpl} / case2")
    a = json.load(open(rf"{SCR}\out\oracle\{tpl}\case2\fields.json", encoding="utf-8"))
    b = json.load(open(rf"{SCR}\out\package\{tpl}\case2\fields.json", encoding="utf-8"))
    a2, b2 = strip_paths(a), strip_paths(b)
    diffs = deep_diff(a2, b2)
    print(f"[ledger 深度 diff，抹去绝对路径后] 差异数 = {len(diffs)}")
    for d in diffs:
        print("  DIFF:", d)

    # ledger per-field summary table
    print("\n[逐字段记账]")
    for fa, fb in itertools.zip_longest(a["fields"], b["fields"]):
        assert fa["name"] == fb["name"], (fa, fb)
        mark = "  " if (fa["status"], fa.get("value"), fa.get("rendered_as")) == (fb["status"], fb.get("value"), fb.get("rendered_as")) else "≠≠"
        print(f" {mark} {fa['name']}(req={fa['required']},kind={fa['kind']}): oracle status={fa['status']} value={json.dumps(fa.get('value'), ensure_ascii=False)} rendered_as={fa.get('rendered_as')!r}")
        if mark == "≠≠":
            print(f"      package                            status={fb['status']} value={json.dumps(fb.get('value'), ensure_ascii=False)} rendered_as={fb.get('rendered_as')!r}")
    print(f" summary oracle = {json.dumps(a['summary'], ensure_ascii=False)}")
    print(f" summary packge = {json.dumps(b['summary'], ensure_ascii=False)}")

    # docx paragraphs
    pa = docx_paras(rf"{SCR}\out\oracle\{tpl}\case2\文书.docx")
    pb = docx_paras(rf"{SCR}\out\package\{tpl}\case2\文书.docx")
    print(f"\n[docx 段落] oracle {len(pa)} 段 / package {len(pb)} 段")
    for i in range(max(len(pa), len(pb))):
        xa = pa[i] if i < len(pa) else None
        xb = pb[i] if i < len(pb) else None
        same = xa and xb and xa["text"] == xb["text"]
        print(f"  p{i:02d} {'=' if same else '≠'} O: {xa['text'] if xa else '<无>'!r}")
        if not same and xb is not None:
            print(f"        P: {xb['text']!r}")

    # fabricated-content probes
    both_text = "\n".join([p["text"] for p in pa] + [p["text"] for p in pb])
    print("\n[编造针检]")
    if tpl == "工作总结":
        dates = re.findall(r"\d{4}[年\-/.]\d{1,2}", both_text)
        print(f"  日期型字符串命中（输入成文日期缺失）: {dates}")
        print(f"  '存在问题'节头出现次数（选填缺失应=0）: {both_text.count('存在问题')} / '三、' 出现: {both_text.count('三、')}")
    if tpl == "周报":
        print(f"  报送日期 '2026-09-28'（输入已填）出现次数: {both_text.count('2026-09-28')}")
        print(f"  '三、问题与需协调事项'节头出现次数（选填缺失应=0）: {both_text.count('三、问题与需协调事项')}")
    print(f"  '____' 计数: oracle={chr(10).join(p['text'] for p in pa).count('____')} package={chr(10).join(p['text'] for p in pb).count('____')}")

    # determinism vs pre-existing in-repo oracle products
    pre = rf"{ROOT}\oracle\out\{tpl}\case2"
    if os.path.isdir(pre):
        pa_old = docx_paras(os.path.join(pre, "文书.docx"))
        fa_old = json.load(open(os.path.join(pre, "fields.json"), encoding="utf-8"))
        ld = deep_diff(strip_paths(fa_old), a2)
        same_paras = [p["text"] for p in pa_old] == [p["text"] for p in pa]
        print(f"\n[确定性] 与仓内既有 oracle/out/{tpl}/case2 相比：ledger 差异={len(ld)}（抹路径），docx 段落文本一致={same_paras}")

json.dump({"done": True}, open(rf"{SCR}\step2_done.json", "w"))
print("\nDONE")
