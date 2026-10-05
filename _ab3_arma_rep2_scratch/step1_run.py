# -*- coding: utf-8 -*-
"""ab3/arm-a/rep2 step1: run both implementations on the two case2 inputs."""
import subprocess, sys, json, os

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
SCR = r"D:\workspace\zcode研究\_ab3_arma_rep2_scratch"

RUNS = [
    # (impl, script, template, input relative to ROOT, outdir)
    ("oracle",  r"oracle\oracle.py",                 "周报",   r"oracle\inputs\周报\case2.json",     rf"{SCR}\out\oracle\周报\case2"),
    ("package", r"package\scripts\gen_doc.py",       "周报",   r"oracle\inputs\周报\case2.json",     rf"{SCR}\out\package\周报\case2"),
    ("oracle",  r"oracle\oracle.py",                 "工作总结", r"oracle\inputs\工作总结\case2.json", rf"{SCR}\out\oracle\工作总结\case2"),
    ("package", r"package\scripts\gen_doc.py",       "工作总结", r"oracle\inputs\工作总结\case2.json", rf"{SCR}\out\package\工作总结\case2"),
]

results = []
for impl, script, tpl, data_rel, outdir in RUNS:
    data_abs = os.path.join(ROOT, data_rel)
    cmd = [sys.executable, os.path.join(ROOT, script.replace("\\", os.sep)) if False else os.path.normpath(os.path.join(ROOT, script)),
           "--template", tpl, "--data", data_abs, "--outdir", outdir]
    p = subprocess.run(cmd, capture_output=True, cwd=ROOT)
    entry = {
        "impl": impl, "template": tpl,
        "cmd": " ".join([cmd[0]] + [c if i != 1 else os.path.relpath(c, ROOT) for i, c in enumerate(cmd[1:])]),
        "exit": p.returncode,
        "stdout": p.stdout.decode("utf-8", errors="replace").strip(),
        "stderr": p.stderr.decode("utf-8", errors="replace").strip(),
        "files": sorted(os.listdir(outdir)) if os.path.isdir(outdir) else None,
    }
    results.append(entry)
    print(f"[{impl}/{tpl}] exit={entry['exit']} files={entry['files']}")
    print(f"  stdout: {entry['stdout']}")
    if entry["stderr"]:
        print(f"  stderr: {entry['stderr']}")

with open(os.path.join(SCR, "step1_runs.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("saved step1_runs.json")
