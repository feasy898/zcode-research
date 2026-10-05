# -*- coding: utf-8 -*-
# 裁判核实脚本：r2 红队候选（GitHub 仓库 + npm registry）
import json, urllib.request, urllib.parse

repos = [
    "THU-MAIC/OpenMAIC",
    "onyx-dot-app/onyx",
    "Canner/WrenAI",
    "robusta-dev/holmesgpt",
    "souzatharsis/podcastfy",
    "andrewyng/translation-agent",
    "cline/cline",
    "CherryHQ/cherry-studio",
    "SWE-Gym/SWE-Gym",
    "volcengine/verl",
    "browseros-ai/BrowserOS",
]
hdr = {"User-Agent": "asset-judge-r2", "Accept": "application/vnd.github+json"}

for r in repos:
    try:
        req = urllib.request.Request("https://api.github.com/repos/%s" % r, headers=hdr)
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.loads(resp.read())
        print("%s | full=%s | stars=%s | forks=%s | pushed=%s | license=%s | archived=%s" % (
            r, d.get("full_name"), d.get("stargazers_count"), d.get("forks_count"),
            d.get("pushed_at"), (d.get("license") or {}).get("spdx_id"), d.get("archived")))
        print("    desc: %s" % (d.get("description") or "")[:200])
    except Exception as e:
        print("%s | ERROR: %s" % (r, e))

# OpenMAIC 最新 release（红队声称 v1.1.2 / 2026-09-28）
try:
    req = urllib.request.Request("https://api.github.com/repos/THU-MAIC/OpenMAIC/releases/latest", headers=hdr)
    with urllib.request.urlopen(req, timeout=30) as resp:
        d = json.loads(resp.read())
    print("OpenMAIC latest release: %s at %s" % (d.get("tag_name"), d.get("published_at")))
except Exception as e:
    print("OpenMAIC release ERROR: %s" % e)

# npm registry 搜索（红队声称 9,245 / 76,416）
for q in ["keywords:mcp-server", "keywords:mcp"]:
    try:
        url = "https://registry.npmjs.org/-/v1/search?text=%s&size=3" % urllib.parse.quote(q)
        req = urllib.request.Request(url, headers=hdr)
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.loads(resp.read())
        print("npm search '%s': total=%s" % (q, d.get("total")))
    except Exception as e:
        print("npm '%s' ERROR: %s" % (q, e))
