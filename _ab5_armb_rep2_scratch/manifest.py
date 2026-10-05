import hashlib
import os
import sys

root = sys.argv[1]
rows = []
for dp, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(dp, f)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rel = os.path.relpath(p, root).replace(os.sep, '/')
        rows.append((rel, h, os.path.getsize(p)))
rows.sort()
for rel, h, sz in rows:
    print(f"{h}  {sz:>8}  {rel}")
print(f"FILE_COUNT={len(rows)}")
