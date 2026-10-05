# -*- coding: utf-8 -*-
"""ab4-invalid-input-rejection / arm-a / rep1 — runner.

Constraint protocol (禁止读取 skillfactory/ 任何文件), same as ab2/ab3 runners:
this script never opens/prints the CONTENT of any skillfactory file. It only
  (a) EXECUTES the two entry points the ask requires to run
      (A=被测技能 package/scripts/gen_doc.py, B=参照实现 oracle/oracle.py), and
  (b) records STRUCTURAL metadata (file names/sizes/existence) of product roots
      under skillfactory to detect artifact residue — no contents.
All invalid inputs are constructed in this scratch dir (outside skillfactory);
all artifacts are produced into this scratch dir and inspected here.
Per group we record: exit code, stdout, stderr (verbatim into logs/), and
artifact residue via before/after tree diff.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
WORK = r"D:\workspace\zcode研究\_ab4_arma_rep1_work"
LOGS = os.path.join(WORK, "logs")
PY = sys.executable

IMPLS = {
    "A": os.path.join(ROOT, "package", "scripts", "gen_doc.py"),   # 被测技能
    "B": os.path.join(ROOT, "oracle", "oracle.py"),                # 参照实现
}
LEGAL = os.path.join(ROOT, "oracle", "inputs", "周报", "case1.json")

# ---------- skillfactory structural snapshot (names/sizes ONLY, for residue) ----------
SF_WATCH = [
    ROOT,                                  # top level only
    os.path.join(ROOT, "package", "out"),  # known product root of A (may not exist)
    os.path.join(ROOT, "oracle", "out"),   # known product root of B (may not exist)
]

def sf_snapshot():
    snap = {}
    for base in SF_WATCH:
        if not os.path.isdir(base):
            snap[base] = "(ABSENT)"
            continue
        if base == ROOT:  # top level only
            snap[base] = sorted((n, os.path.getsize(os.path.join(base, n)) if os.path.isfile(os.path.join(base, n)) else -1)
                                for n in os.listdir(base))
        else:
            entries = []
            for dp, dns, fns in os.walk(base):
                for f in fns:
                    p = os.path.join(dp, f)
                    entries.append((os.path.relpath(p, base), os.path.getsize(p)))
            snap[base] = sorted(entries)
    return snap

# ---------- local WORK snapshot (full tree, skip logs/) ----------
def work_snapshot():
    snap = {}
    for dp, dns, fns in os.walk(WORK):
        dns[:] = [d for d in dns if not (dp == WORK and d == "logs")]
        for f in fns:
            p = os.path.join(dp, f)
            snap[os.path.relpath(p, WORK)] = os.path.getsize(p)
    return snap

def diff_snap(before, after):
    out = []
    for k in sorted(set(before) | set(after)):
        b, a = before.get(k), after.get(k)
        if b is None:
            out.append(f"NEW     {k}  size={a}")
        elif a is None:
            out.append(f"GONE    {k}  (was size={b})")
        elif a != b:
            out.append(f"CHANGED {k}  size {b} -> {a}")
    return out

# ---------- prepare invalid inputs in scratch ----------
os.makedirs(LOGS, exist_ok=True)
inputs_dir = os.path.join(WORK, "inputs")
os.makedirs(inputs_dir, exist_ok=True)

notjson_path = os.path.join(inputs_dir, "not_json.txt")
with open(notjson_path, "w", encoding="utf-8") as f:
    f.write("这不是JSON：键＝值；第二项 ＝ 值2。{未闭合的伪JSON")

toparray_path = os.path.join(inputs_dir, "top_level_array.json")
with open(toparray_path, "w", encoding="utf-8") as f:
    f.write('["数组", "非对象"]')

missing_path = os.path.join(inputs_dir, "nonexistent_不存在.json")  # deliberately never created
assert not os.path.exists(missing_path)

GROUPS = [
    ("g1_template_证书", "证书", LEGAL),        # ① 非法模板名（数据用合法 case1）
    ("g2_data_文件不存在", "周报", missing_path),  # ② --data 指向不存在文件
    ("g3_data_非JSON", "周报", notjson_path),   # ③ 内容不是 JSON
    ("g4_data_顶层非对象", "周报", toparray_path),  # ④ 顶层是数组
    ("g0_合法对照", "周报", LEGAL),              # 合法对照组
]

print("#### ENTRY POINTS (existence by name only) ####")
for arm, script in IMPLS.items():
    print(f"[{arm}] exe={PY} script={script} exists={os.path.isfile(script)}")
print(f"[legal input] {LEGAL} exists={os.path.isfile(LEGAL)} size={os.path.getsize(LEGAL)}B")
print()
print("#### LOCAL INVALID INPUTS (constructed in scratch, contents shown verbatim) ####")
for p in (notjson_path, toparray_path):
    raw = open(p, "rb").read()
    print(f"{os.path.basename(p)}: {len(raw)}B sha256={hashlib.sha256(raw).hexdigest()[:16]} content={raw.decode('utf-8')!r}")
print(f"nonexistent path (never created): {missing_path}")
print()

sf_before = sf_snapshot()

print("#### RUNS (cwd=scratch; --outdir fresh per run) ####")
results = {}
for arm, script in IMPLS.items():
    for gname, tpl, data in GROUPS:
        outdir = os.path.join(WORK, arm, gname, "out")
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        os.makedirs(os.path.dirname(outdir), exist_ok=True)
        cmd = [PY, script, "--template", tpl, "--data", data, "--outdir", outdir]
        w_before = work_snapshot()
        try:
            cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=180, cwd=WORK)
            rc, so, se = cp.returncode, cp.stdout, cp.stderr
        except subprocess.TimeoutExpired as e:
            rc, so, se = "TIMEOUT", (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), \
                          (e.stderr or b"").decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        w_after = work_snapshot()
        residue = diff_snap(w_before, w_after)
        sf_after_all = None  # filled at the very end; per-run we only flag outdir state
        outdir_state = ("MISSING" if not os.path.isdir(outdir) else
                        str({f: os.path.getsize(os.path.join(outdir, f)) for f in sorted(os.listdir(outdir))}))
        log = (f"arm={arm} group={gname}\n--- argv ---\n{cmd}\n"
               f"--- exit ---\n{rc}\n--- stdout ---\n{so}\n--- stderr ---\n{se}\n"
               f"--- outdir state after run ---\n{outdir_state}\n"
               f"--- residue (WORK tree diff) ---\n" + ("\n".join(residue) if residue else "(none)") + "\n")
        with open(os.path.join(LOGS, f"{arm}_{gname}.log"), "w", encoding="utf-8") as f:
            f.write(log)
        results[(arm, gname)] = dict(rc=rc, so=so, se=se, residue=residue, outdir=outdir_state)
        print(f"[{arm}] {gname}: exit={rc} outdir={outdir_state}")
        print(f"    stdout: {so.strip()[:400]!r}")
        print(f"    stderr: {se.strip()[:400]!r}")
        print(f"    residue: {'; '.join(residue) if residue else '(none)'}")

print()
print("#### SKILLFACTORY RESIDUE CHECK (names/sizes only — no contents) ####")
sf_after = sf_snapshot()
sf_residue = []
for base in SF_WATCH:
    b, a = sf_before[base], sf_after[base]
    if b != a:
        sf_residue.append(f"{base}: {b!r} -> {a!r}")
print("\n".join(sf_residue) if sf_residue else "(no structural change under watched skillfactory roots)")

print()
print("#### CONTROL PRODUCTS VALIDITY (g0) ####")
for arm in IMPLS:
    outdir = os.path.join(WORK, arm, "g0_合法对照", "out")
    docx = os.path.join(outdir, "文书.docx")
    if os.path.isfile(docx):
        try:
            with zipfile.ZipFile(docx) as z:
                names = z.namelist()
                bad = z.testzip()
            print(f"[{arm}] 文书.docx valid zip={bad is None} entries={len(names)} has_word/document.xml={'word/document.xml' in names}")
        except Exception as e:
            print(f"[{arm}] 文书.docx NOT a valid zip: {type(e).__name__}: {e}")
    else:
        print(f"[{arm}] 文书.docx ABSENT")

print("DONE")
