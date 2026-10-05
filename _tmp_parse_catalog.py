# -*- coding: utf-8 -*-
import re, io, json

p = r'D:/workspace/zcode研究/skillfactory/v2/CATALOG.md'
text = io.open(p, encoding='utf-8').read()
lines = text.split('\n')

rows = [(i, l) for i, l in enumerate(lines, 1) if l.startswith('| [')]
print('rows starting "| [":', len(rows))
print('total chars in rows:', sum(len(l) for _, l in rows))

pat = re.compile(r'(?<!\\)\|')
bad = []
for i, l in rows:
    cells = pat.split(l)
    n = len(cells) - 2  # leading empty + trailing empty
    if n != 7:
        bad.append((i, n))
print('rows with != 7 cols:', bad, 'count:', len(bad))

rt = [i for i, l in rows if '【红队】' in l]
print('rows containing redteam marker:', len(rt))

sec = None
cnt = {}
order = []
for l in lines:
    m3 = re.match(r'^### ([AB]\d+\.\d+)', l)
    m2 = re.match(r'^## ([AB]\d+)', l)
    if m3:
        sec = m3.group(1)
    elif m2:
        sec = m2.group(1)
    elif l.startswith('| [') and sec:
        if sec not in cnt:
            order.append(sec)
        cnt[sec] = cnt.get(sec, 0) + 1
for s in order:
    print(s, cnt[s])

# extract first URL per row, check none missing
nourl = []
for i, l in rows:
    if not re.search(r'\((https?://[^)]+)\)', l):
        nourl.append(i)
print('rows without URL:', nourl)

# empty-cell check
empty_cells = []
for i, l in rows:
    cells = [c.strip() for c in pat.split(l)][1:-1]
    for idx, c in enumerate(cells):
        if c == '':
            empty_cells.append((i, idx))
print('empty cells (row, colidx):', empty_cells)
