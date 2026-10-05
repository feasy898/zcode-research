# -*- coding: utf-8 -*-
"""Parse skillfactory/v2/CATALOG.md asset rows into InventoryItem JSON array.
Mechanical only: verbatim cells, de-link names, cap long text fields with marker.
"""
import re, io, json, sys

CAP_WHAT = int(sys.argv[1]) if len(sys.argv) > 1 else 60
CAP_VALUE = int(sys.argv[2]) if len(sys.argv) > 2 else 45
CAP_MAT = int(sys.argv[3]) if len(sys.argv) > 3 else 40
OUT = r'D:/workspace/zcode研究/_tmp_inventory.json'

p = r'D:/workspace/zcode研究/skillfactory/v2/CATALOG.md'
lines = io.open(p, encoding='utf-8').read().split('\n')

pat = re.compile(r'(?<!\\)\|')
link = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
urlre = re.compile(r'\((https?://[^)]+)\)')

def unesc(s):
    return s.replace('\\|', '|')

def clean_name(cell):
    s = unesc(cell.strip())
    s = link.sub(lambda m: m.group(1), s)      # [text](url) -> text
    s = s.replace('【红队】', '').strip()       # redteam marker -> foundBy
    return s

def first_url(cell):
    m = urlre.search(unesc(cell))
    return m.group(1) if m else ''

def cap(s, n):
    s = s.strip()
    return s if len(s) <= n else s[:n] + '……'

sec = None
items = []
rt_count = 0
for l in lines:
    m3 = re.match(r'^### (.+?)（\d+）\s*$', l)
    if m3:
        sec = m3.group(1).strip()
        continue
    if not l.startswith('| ['):
        continue
    cells = [unesc(c.strip()) for c in pat.split(l)][1:-1]
    assert len(cells) == 7, cells
    c_asset, c_platform, c_type, c_what, c_value, c_mat, c_src = cells
    if '【红队】' in c_src:
        found = c_src
        rt_count += 1
    else:
        found = '目录'
    items.append({
        'name': clean_name(c_asset),
        'url': first_url(c_asset),
        'platform': c_platform,
        'assetType': c_type,
        'domain': sec,
        'what': cap(c_what, CAP_WHAT),
        'valueForUs': cap(c_value, CAP_VALUE),
        'maturity': cap(c_mat, CAP_MAT),
        'foundBy': found,
    })

print('items:', len(items))
print('redteam foundBy:', rt_count)
js = ',\n'.join(json.dumps(it, ensure_ascii=False, separators=(chr(44), chr(58))) for it in items)
arr = '[\n' + js + '\n]'
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(arr)
print('chars:', len(arr))
print('bytes utf8:', len(arr.encode('utf-8')))
# sanity: no empty fields
empty = [(i, k) for i, it in enumerate(items) for k, v in it.items() if not v]
print('empty fields:', empty)
# sanity: names sample
print('first:', items[0]['name'], '|', items[0]['url'])
print('last:', items[-1]['name'], '|', items[-1]['url'])
# full-text variant for comparison
items_full = []
sec = None
for l in lines:
    m3 = re.match(r'^### (.+?)（\d+）\s*$', l)
    if m3:
        sec = m3.group(1).strip(); continue
    if not l.startswith('| ['): continue
    cells = [unesc(c.strip()) for c in pat.split(l)][1:-1]
    c_asset, c_platform, c_type, c_what, c_value, c_mat, c_src = cells
    found = c_src if '【红队】' in c_src else '目录'
    items_full.append({'name': clean_name(c_asset), 'url': first_url(c_asset),
        'platform': c_platform, 'assetType': c_type, 'domain': sec,
        'what': c_what, 'valueForUs': c_value, 'maturity': c_mat, 'foundBy': found})
arr_full = '[\n' + ',\n'.join(json.dumps(it, ensure_ascii=False, separators=(chr(44), chr(58))) for it in items_full) + '\n]'
print('full-text chars:', len(arr_full), 'bytes:', len(arr_full.encode('utf-8')))
