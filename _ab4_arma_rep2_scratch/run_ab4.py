# -*- coding: utf-8 -*-
"""ab4/arm-a/rep2 runner: A/B test -- invalid-input rejection.

Black-box A/B: runs the skill under test (package/scripts/gen_doc.py, arm A)
and the reference implementation (oracle/oracle.py) with the same CLI
(--template X --data F --outdir D), cwd = skill ROOT, on four invalid inputs
plus one legal control. Records exit code, stdout, stderr, and produced
artifacts. This runner NEVER reads the content of any file under
skillfactory/ -- it only executes the two CLIs and lists directories.
"""
import json, os, shutil, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
SCR  = r"D:\workspace\zcode研究\_ab4_arma_rep2_scratch"
FIX  = os.path.join(SCR, "fixtures")
ORACLE_DATA = os.path.join(BASE, "oracle", "inputs", "周报", "case1.json")

IMPLS = [
    ("package", os.path.join(BASE, "package", "scripts", "gen_doc.py")),  # arm A: skill under test
    ("oracle",  os.path.join(BASE, "oracle", "oracle.py")),               # reference implementation
]

# ---------- fixtures (outside skillfactory) ----------
os.makedirs(FIX, exist_ok=True)
notjson = os.path.join(FIX, "notjson.json")
with open(notjson, "w", encoding="utf-8", newline="") as f:
    f.write("这不是JSON")                       # case T3: not JSON at all
arr = os.path.join(FIX, "array.json")
with open(arr, "w", encoding="utf-8", newline="") as f:
    f.write('["数组","非对象"]')                 # case T4: top-level JSON array, not object
missing = os.path.join(FIX, "no-such-file.json")  # case T2: never created
if os.path.exists(missing):
    os.remove(missing)

assert os.path.isfile(ORACLE_DATA), "oracle case1.json missing"
assert not os.path.exists(missing), "T2 fixture must not exist"

# ---------- residue marker (mtime baseline) ----------
marker = os.path.join(SCR, "marker.txt")
with open(marker, "w", encoding="utf-8") as f:
    f.write(time.strftime("%Y-%m-%d %H:%M:%S"))

# ---------- cases ----------
CASES = [
    ("T1-invalid-template", "证书", ORACLE_DATA),   # illegal template name
    ("T2-data-missing",     "周报", missing),        # --data points to nonexistent file
    ("T3-data-not-json",    "周报", notjson),        # --data content is not JSON
    ("T4-data-top-array",   "周报", arr),            # --data is top-level JSON array
    ("C0-legal-control",    "周报", ORACLE_DATA),    # legal control
]

def list_files(root):
    if not os.path.isdir(root):
        return None
    out = []
    for dp, dns, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            out.append([os.path.relpath(p, root).replace("\\", "/"), os.path.getsize(p)])
    return sorted(out)

def dec(b):
    return b.decode("utf-8", errors="replace").strip()

def show_path(p):
    return os.path.relpath(p, SCR).replace("\\", "/") if p.startswith(SCR) \
        else os.path.relpath(p, BASE).replace("\\", "/")

results = []
for pas in (1, 2):
    for case_id, tpl, data in CASES:
        for impl, script in IMPLS:
            outdir = os.path.join(SCR, "out", f"pass{pas}", impl, case_id)
            if os.path.isdir(outdir):
                shutil.rmtree(outdir)
            cmd = [sys.executable, script, "--template", tpl, "--data", data, "--outdir", outdir]
            t0 = time.time()
            try:
                p = subprocess.run(cmd, capture_output=True, cwd=BASE, timeout=180)
                exit_code, so, se = p.returncode, dec(p.stdout), dec(p.stderr)
            except subprocess.TimeoutExpired:
                exit_code, so, se = "TIMEOUT", "", "killed after 180s"
            entry = {
                "pass": pas, "case": case_id, "impl": impl,
                "template": tpl, "data": show_path(data),
                "cmd": f"python {show_path(script)} --template {tpl} --data {show_path(data)} --outdir {show_path(outdir)}",
                "exit": exit_code,
                "stdout": so,
                "stderr": se,
                "outdir_created": os.path.isdir(outdir),
                "outdir_files": list_files(outdir),
                "seconds": round(time.time() - t0, 2),
            }
            results.append(entry)
            print(f"pass{pas} {case_id:22s} [{impl:7s}] exit={entry['exit']} "
                  f"outdir_created={entry['outdir_created']} files={entry['outdir_files']}")
            if se:
                print(f"    stderr: {se[:500]}")
            if so:
                print(f"    stdout: {so[:250]}")

with open(os.path.join(SCR, "ab4_runs.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("saved ab4_runs.json ; RUNNER DONE")
