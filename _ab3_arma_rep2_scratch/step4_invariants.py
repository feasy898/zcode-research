# -*- coding: utf-8 -*-
"""ab3/arm-a/rep2 step4: ledger invariants (SKILL.md §5) on both sides + oracle verify.py."""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
SCR = r"D:\workspace\zcode研究\_ab3_arma_rep2_scratch"
TPLS = ["周报", "工作总结"]
TITLE_FORMULA = {"周报": ("部门", "工作周报"), "工作总结": ("总结主体", "总结时段", "工作总结")}

def check_ledger(tag, d, docx_first_nonempty):
    errs = []
    if set(d) != {"template", "title", "filled_fields", "missing_fields", "fields", "summary", "outputs"}:
        errs.append(f"顶层键≠7: {sorted(d)}")
    for f in d["fields"]:
        req_keys = {"name", "required", "kind", "status", "value"}
        if not req_keys <= set(f): errs.append(f"{f.get('name')} 缺键 {req_keys - set(f)}")
        if f["status"] == "filled":
            if f["value"] is None: errs.append(f"{f['name']} filled 但 value=null")
            if "rendered_as" in f: errs.append(f"{f['name']} filled 却带 rendered_as")
        elif f["status"] == "missing":
            if f["value"] is not None: errs.append(f"{f['name']} missing 但 value 非空")
            if f.get("rendered_as") is None: errs.append(f"{f['name']} missing 无 rendered_as")
        else:
            errs.append(f"{f['name']} 非法 status={f['status']}")
        if f["kind"] == "list" and f["status"] == "filled" and not isinstance(f["value"], list):
            errs.append(f"{f['name']} list filled 但 value 非数组: {f['value']!r}")
    s = d["summary"]
    if set(s) != {"total", "filled", "missing", "missing_required", "missing_required_names", "unknown_keys"}:
        errs.append(f"summary 键≠6: {sorted(s)}")
    nf = sum(1 for f in d["fields"] if f["status"] == "filled")
    nm = sum(1 for f in d["fields"] if f["status"] == "missing")
    if not (s["filled"] == nf and s["missing"] == nm and nf + nm == s["total"] == len(d["fields"])):
        errs.append(f"计数不自洽: summary={s} vs 实数 filled={nf} missing={nm}")
    mr = [f["name"] for f in d["fields"] if f["status"] == "missing" and f["required"]]
    if s["missing_required_names"] != mr or s["missing_required"] != len(mr):
        errs.append(f"missing_required_names 不自洽: {s['missing_required_names']} vs {mr}")
    if d["filled_fields"] != [f["name"] for f in d["fields"] if f["status"] == "filled"]:
        errs.append("filled_fields 序列不自洽")
    if d["missing_fields"] != [f["name"] for f in d["fields"] if f["status"] == "missing"]:
        errs.append("missing_fields 序列不自洽")
    if d["title"] != docx_first_nonempty:
        errs.append(f"title≠文书标题段: ledger={d['title']!r} docx={docx_first_nonempty!r}")
    # title formula (V2, ____ substitution for missing)
    head = d["title"]
    for name in TITLE_FORMULA:
        pass
    print(f"  [{tag}] 错误数={len(errs)}")
    for e in errs: print("     ✗", e)
    return errs

def docx_first_nonempty(p):
    from docx import Document
    for para in Document(p).paragraphs:
        if para.text.strip(): return para.text
    return None

total_errs = 0
for tpl in TPLS:
    print(f"### {tpl} 台账不变量（SKILL.md §5）")
    for side, root in (("oracle", rf"{SCR}\out\oracle"), ("package", rf"{SCR}\out\package")):
        d = json.load(open(rf"{root}\{tpl}\case2\fields.json", encoding="utf-8"))
        first = docx_first_nonempty(rf"{root}\{tpl}\case2\文书.docx")
        total_errs += len(check_ledger(f"{side}/{tpl}", d, first))
    # title formula expectation
    for side, root in (("oracle", rf"{SCR}\out\oracle"), ("package", rf"{SCR}\out\package")):
        d = json.load(open(rf"{root}\{tpl}\case2\fields.json", encoding="utf-8"))
        vals = {f["name"]: f["value"] for f in d["fields"]}
        if tpl == "周报":
            exp = f"{vals.get('部门') or '____'}工作周报"
        else:
            exp = f"{vals.get('总结主体') or '____'}{vals.get('总结时段')}工作总结"
        print(f"  [{side}/{tpl}] 标题公式预期={exp!r} 实际={d['title']!r} 一致={exp == d['title']}")

print("\n### oracle 自带 verify.py（仓内 oracle/out 8 样例校验）")
p = subprocess.run([sys.executable, "verify.py"], capture_output=True, cwd=rf"{ROOT}\oracle")
print("exit =", p.returncode)
print(p.stdout.decode("utf-8", errors="replace").strip())
if p.stderr.decode("utf-8", errors="replace").strip():
    print("stderr:", p.stderr.decode("utf-8", errors="replace").strip()[:500])
print(f"\nTOTAL ledger invariant errors (4 ledgers) = {total_errs}")
