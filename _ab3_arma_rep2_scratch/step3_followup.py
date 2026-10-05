# -*- coding: utf-8 -*-
"""ab3/arm-a/rep2 step3: explain residual determinism diffs + ____ positions + package/out determinism."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
SCR = r"D:\workspace\zcode研究\_ab3_arma_rep2_scratch"
TPLS = ["周报", "工作总结"]

def deep_diff(a, b, path="$"):
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: diffs.append(f"{path}.{k}: only-pre={b[k]!r}")
            elif k not in b: diffs.append(f"{path}.{k}: only-new={a[k]!r}")
            else: diffs += deep_diff(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): diffs.append(f"{path}: len {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)): diffs += deep_diff(x, y, f"{path}[{i}]")
    elif a != b:
        diffs.append(f"{path}: pre={a!r} vs new={b!r}")
    return diffs

def docx_texts(p):
    from docx import Document
    return [para.text for para in Document(p).paragraphs]

for tpl in TPLS:
    print("=" * 90)
    print(f"### {tpl}")
    # 1) explain the 2 residual ledger diffs vs pre-existing oracle/out
    pre = json.load(open(rf"{ROOT}\oracle\out\{tpl}\case2\fields.json", encoding="utf-8"))
    new = json.load(open(rf"{SCR}\out\oracle\{tpl}\case2\fields.json", encoding="utf-8"))
    print("[oracle 确定性] 残余 diff 明细:")
    for d in deep_diff(pre, new): print("   ", d)
    # 2) package determinism vs pre-existing package/out (if present)
    pre_p = rf"{ROOT}\package\out\{tpl}\case2"
    if os.path.isdir(pre_p):
        pre2 = json.load(open(os.path.join(pre_p, "fields.json"), encoding="utf-8"))
        new2 = json.load(open(rf"{SCR}\out\package\{tpl}\case2\fields.json", encoding="utf-8"))
        dd = deep_diff(pre2, new2)
        print(f"[package 确定性] vs 仓内既有 package/out/{tpl}/case2：diff 数={len(dd)}")
        for d in dd: print("   ", d)
        same = docx_texts(os.path.join(pre_p, "文书.docx")) == docx_texts(rf"{SCR}\out\package\{tpl}\case2\文书.docx")
        print(f"[package 确定性] docx 段落文本一致={same}")
    else:
        print(f"[package 确定性] 仓内无 package/out/{tpl}/case2，跳过")
    # 3) ____ positions on both sides
    for side in ("oracle", "package"):
        txts = docx_texts(rf"{SCR}\out\{side}\{tpl}\case2\文书.docx")
        hits = [(i, t) for i, t in enumerate(txts) if "____" in t]
        print(f"[{side} ____ 位置] " + "; ".join(f"p{i}={t!r}" for i, t in hits))
    # 4) section headers both sides
    for side in ("oracle", "package"):
        txts = docx_texts(rf"{SCR}\out\{side}\{tpl}\case2\文书.docx")
        heads = [(i, t) for i, t in enumerate(txts) if t[:2] in ("一、", "二、", "三、", "四、")]
        print(f"[{side} 节头] " + "; ".join(f"p{i}={t!r}" for i, t in heads))

# raw p01 of both 周报 sides, repr-escaped
print("=" * 90)
for side in ("oracle", "package"):
    t = docx_texts(rf"{SCR}\out\{side}\周报\case2\文书.docx")[1]
    print(f"周报 p01 [{side}] codepoints={[hex(ord(c)) for c in t[:14]]} text={t!r}")
