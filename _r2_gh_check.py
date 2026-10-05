# -*- coding: utf-8 -*-
"""r2 复检脚本：GitHub API 核实仓库线索（star/pushed_at/更名/README 头部）。
安全约束：仅 http/https；host 白名单；解析 DNS 后拒绝私有/环回/保留地址。"""
import base64
import ipaddress
import json
import socket
import sys
import urllib.parse
import urllib.request

ALLOWED_HOSTS = {"api.github.com", "raw.githubusercontent.com"}
UA = {"User-Agent": "r2-verify-script", "Accept": "application/vnd.github+json"}


def check_url(url):
    u = urllib.parse.urlparse(url)
    if u.scheme not in ("http", "https"):
        raise ValueError("scheme not allowed: %s" % url)
    host = u.hostname
    if host not in ALLOWED_HOSTS:
        raise ValueError("host not in allowlist: %s" % host)
    for _fam, _typ, _proto, _canon, sa in socket.getaddrinfo(host, 443):
        ip = ipaddress.ip_address(sa[0])
        if (ip.is_private or ip.is_loopback or ip.is_reserved
                or ip.is_link_local or ip.is_multicast or ip.is_unspecified):
            raise ValueError("host resolves to private/reserved addr: %s -> %s" % (host, ip))


def get(url):
    check_url(url)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fetch_readme(full_name):
    for fn in ("README.md", "readme.md", "README.rst"):
        try:
            raw = get("https://raw.githubusercontent.com/%s/HEAD/%s" % (full_name, fn))
            return raw.decode("utf-8", "replace")
        except Exception:
            continue
    return None


def repo(name):
    out = {"requested": name}
    try:
        data = json.loads(get("https://api.github.com/repos/%s" % name))
    except urllib.error.HTTPError as e:
        out["error"] = "HTTP %d" % e.code
        print(json.dumps(out, ensure_ascii=False))
        return
    except Exception as e:
        out["error"] = repr(e)
        print(json.dumps(out, ensure_ascii=False))
        return
    full = data["full_name"]
    out["full_name"] = full
    out["renamed_or_moved"] = (full.lower() != name.lower())
    out["stars"] = data["stargazers_count"]
    out["forks"] = data["forks_count"]
    out["open_issues"] = data["open_issues_count"]
    out["pushed_at"] = data["pushed_at"]
    out["created_at"] = data["created_at"]
    out["archived"] = data["archived"]
    out["description"] = (data.get("description") or "")[:220]
    out["homepage"] = data.get("homepage") or ""
    out["topics"] = (data.get("topics") or [])[:12]
    rd = fetch_readme(full)
    out["readme_head"] = " ".join(rd[:1600].split()) if rd else "(readme fetch failed)"
    print(json.dumps(out, ensure_ascii=False))


def org(name):
    try:
        data = json.loads(get(
            "https://api.github.com/orgs/%s/repos?sort=pushed&per_page=15" % name))
    except Exception as e:
        print(json.dumps({"org": name, "error": repr(e)}, ensure_ascii=False))
        return
    for d in data:
        print(json.dumps({
            "org": name,
            "full_name": d["full_name"],
            "stars": d["stargazers_count"],
            "pushed_at": d["pushed_at"],
            "description": (d.get("description") or "")[:150],
        }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    for arg in sys.argv[1:]:
        if arg.startswith("org:"):
            org(arg[4:])
        else:
            repo(arg)
