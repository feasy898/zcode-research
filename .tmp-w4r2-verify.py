import json, ssl, urllib.request

repos = [
    "modelcontextprotocol/modelcontextprotocol",
    "modelcontextprotocol/servers",
    "anthropics/claude-code-action",
    "anthropics/claude-code",
    "ollama/ollama",
    "bytedance/UI-TARS-desktop",
    "bytedance/agent-tars",
    "openai/openai-apps-sdk-examples",
    "openai/apps-sdk-ui",
    "microsoft/PyRIT",
    "higress-group/higress",
    "x402-foundation/x402",
    "awslabs/mcp",
]
ctx = ssl.create_default_context()
for r in repos:
    req = urllib.request.Request(
        "https://api.github.com/repos/" + r,
        headers={"User-Agent": "inventory-verify", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            d = json.load(resp)
        lic = (d.get("license") or {}).get("spdx_id")
        print(json.dumps({
            "repo": d.get("full_name"),
            "owner": (d.get("owner") or {}).get("login"),
            "owner_type": (d.get("owner") or {}).get("type"),
            "stars": d.get("stargazers_count"),
            "forks": d.get("forks_count"),
            "license": lic,
            "pushed_at": d.get("pushed_at"),
            "created_at": d.get("created_at"),
            "archived": d.get("archived"),
            "homepage": d.get("homepage"),
            "description": d.get("description"),
        }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"repo": r, "error": str(e)}, ensure_ascii=False))
