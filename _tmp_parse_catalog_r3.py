# -*- coding: utf-8 -*-
"""Parse skillfactory/v2/CATALOG.md asset rows into InventoryItem JSON (temp tool)."""
import json, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

SRC = r"D:\workspace\zcode研究\skillfactory\v2\CATALOG.md"
OUT = r"D:\workspace\zcode研究\_tmp_catalog_inventory.json"

text = open(SRC, encoding="utf-8").read()
lines = text.splitlines()

row_re = re.compile(r"^\|\s*\[")
link_re = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
sub_re = re.compile(r"^###\s+(.+?)\s*（\d+）\s*$")

EXPECTED = {
 "A1.1 能力封装开放标准": 3, "A1.2 Agent 互操作协议与官方实现": 6, "A1.3 协议扩展规范": 2,
 "A1.4 平台官方机制文档与参考仓": 7, "A1.5 官方教程与示例库": 5,
 "A2.1 官方技能规范与示例": 2, "A2.2 方法论技能集": 3, "A2.3 插件工程与官方插件包": 5,
 "A2.4 命令与 hooks": 2, "A2.5 子代理与规则定义合集": 5, "A2.6 平台插件样本·Dify 生态": 3,
 "A3.1 系统提示词语料档案": 4, "A3.2 结构化方法论与教材": 2, "A3.3 中文社区/个人 prompt 库": 3,
 "A3.4 prompt 管理与优化工具": 3,
 "A4.1 参考实现与框架": 2, "A4.2 开发调试工具": 1, "A4.3 任务域 server·办公协同": 6,
 "A4.4 任务域 server·浏览器/文档/电商": 4, "A4.5 网关与托管执行层": 5, "A4.6 注册表·目录·企业分发": 15,
 "A5.1 自托管平台与环境": 14, "A5.2 多代理编排框架": 14, "A5.3 语音与实时多模态": 2,
 "A5.4 浏览器/终端/GUI 操作底座": 8, "A5.5 网页数据采集底座": 2, "A5.6 沙箱与代码执行环境": 3,
 "A5.7 记忆与有状态 agent": 3,
 "A6.1 综合与终端基准": 5, "A6.2 工具交互基准·客服域": 4, "A6.3 任务域基准": 7,
 "A6.4 评测与观测平台": 7, "A6.5 技能安全评测": 6,
 "A7.1 行为观测与审计": 2, "A7.2 用量与成本": 2,
 "A8.1 官方插件/技能市场": 7, "A8.2 生态索引与 awesome 精选": 6, "A8.3 模板市场与聚合安装器": 3,
 "A8.4 国内平台商店": 5, "A8.5 内容场分发案例": 1,
 "B1.1 跨职能知识工作插件": 1, "B1.2 文档读写与解析工具": 3, "B1.3 中文办公生态技能": 1,
 "B2.1 短视频生产": 3, "B2.2 图文与图像生产": 4, "B2.3 skill 化内容产线": 1,
 "B2.4 社媒分发": 1, "B2.5 销售与成交": 1,
 "B3.1 深度研究与调研": 4, "B3.2 金融多代理研究": 2, "B3.3 科学研究与科研技能包": 2,
 "B4.1 结对编程与代码修改": 3, "B4.2 代码审查": 1, "B4.3 规格驱动开发方法论": 2,
}
EXPECTED_FORM = {"软件系统": 92, "目录渠道": 35, "文档教程": 13, "prompt模板": 8, "skill": 9,
                 "plugin": 10, "MCP": 13, "评测集": 19, "agent配置": 4, "标准规范": 9,
                 "hook": 2, "command": 1, "工作流模板": 1, "内容案例": 2}

items, skipped = [], []
sub = None

def split_row(line):
    parts = re.split(r"(?<!\\)\|", line)
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [p.replace("\\|", "|").strip() for p in parts]

for lineno, line in enumerate(lines, 1):
    if line.startswith("### "):
        m = sub_re.match(line.strip())
        sub = m.group(1).strip() if m else line[4:].strip()
        continue
    if row_re.match(line):
        cells = split_row(line)
        if len(cells) != 7:
            skipped.append((lineno, "cell_count=%d" % len(cells), line[:60]))
            continue
        asset, platform, form, what, value, maturity, source = cells
        m = link_re.search(asset)
        if not m:
            skipped.append((lineno, "no_link", line[:60]))
            continue
        items.append({
            "name": m.group(1).strip(),
            "url": m.group(2).strip(),
            "platform": platform,
            "assetType": form,
            "domain": sub,
            "domainMain": None,
            "what": what,
            "valueForUs": value,
            "maturity": maturity,
            "foundBy": source if "【红队】" in source else "目录",
        })
        items[-1].pop("domainMain")

cnt = Counter(x["domain"] for x in items)
form_cnt = Counter(x["assetType"].split("（")[0].strip() for x in items)
red_cnt = sum(1 for x in items if x["foundBy"].startswith("【红队】"))

json.dump(items, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

print("TOTAL:", len(items), "RED:", red_cnt, "SKIPPED:", len(skipped))
for s in skipped:
    print("SKIP:", s)
print("MISMATCH_SUBCAT:", json.dumps({k: (v, cnt.get(k, 0)) for k, v in EXPECTED.items() if cnt.get(k, 0) != v}, ensure_ascii=False))
print("MISMATCH_FORM:", json.dumps({k: (v, form_cnt.get(k, 0)) for k, v in EXPECTED_FORM.items() if form_cnt.get(k, 0) != v}, ensure_ascii=False))
print("EXTRA_SUBCAT:", json.dumps({k: v for k, v in cnt.items() if k not in EXPECTED}, ensure_ascii=False))
print("EXTRA_FORM:", json.dumps({k: v for k, v in form_cnt.items() if k not in EXPECTED_FORM}, ensure_ascii=False))
print("---- INDEX ----")
for i, x in enumerate(items, 1):
    code = (x["domain"] or "?").split(" ")[0]
    flag = "R" if x["foundBy"].startswith("【红队】") else "."
    print("%03d %s %s %s | %s" % (i, code, flag, x["url"], x["name"]))
