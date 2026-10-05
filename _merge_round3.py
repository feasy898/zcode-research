# -*- coding: utf-8 -*-
"""2026-09-30 合并轮：把 40 个净新增资产插入 CATALOG.md（只增，不改任何既有条目行）"""
import io, re, sys

PATH = r"D:\workspace\zcode研究\skillfactory\v2\CATALOG.md"
with io.open(PATH, "r", encoding="utf-8", newline="") as f:
    lines = f.readlines()  # 保留原有换行符

before_rows = sum(1 for l in lines if l.startswith("| ["))

def find_one(substr):
    idxs = [i for i, l in enumerate(lines) if substr in l]
    if len(idxs) != 1:
        raise SystemExit(u"ANCHOR not unique (%d): %s" % (len(idxs), substr[:70]))
    return idxs[0]

def insert_after(anchor, rows):
    i = find_one(anchor)
    eol = "\r\n" if lines[i].endswith("\r\n") else "\n"
    for j, row in enumerate(rows):
        lines.insert(i + 1 + j, row + eol)

def replace_once(old, new):
    i = find_one(old)
    lines[i] = lines[i].replace(old, new)

# ---------- 1) 分节标题计数 ----------
heads = [
 (u"## A1 标准·协议·官方参考（21）", u"## A1 标准·协议·官方参考（23）"),
 (u"### A1.2 Agent 互操作协议与官方实现（5）", u"### A1.2 Agent 互操作协议与官方实现（6）"),
 (u"### A1.3 协议扩展规范（1）", u"### A1.3 协议扩展规范（2）"),
 (u"## A2 技能·插件·配置件（16）", u"## A2 技能·插件·配置件（20）"),
 (u"### A2.1 官方技能规范与示例（1）", u"### A2.1 官方技能规范与示例（2）"),
 (u"### A2.2 方法论技能集（2）", u"### A2.2 方法论技能集（3）"),
 (u"### A2.5 子代理与规则定义合集（3）", u"### A2.5 子代理与规则定义合集（5）"),
 (u"## A3 提示词资产（11）", u"## A3 提示词资产（12）"),
 (u"### A3.1 系统提示词语料档案（3）", u"### A3.1 系统提示词语料档案（4）"),
 (u"## A4 MCP 工具生态（28）", u"## A4 MCP 工具生态（33）"),
 (u"### A4.4 任务域 server·浏览器/文档/电商（3）", u"### A4.4 任务域 server·浏览器/文档/电商（4）"),
 (u"### A4.5 网关与托管执行层（4）", u"### A4.5 网关与托管执行层（5）"),
 (u"### A4.6 注册表·目录·企业分发（12）", u"### A4.6 注册表·目录·企业分发（15）"),
 (u"## A5 平台·框架·运行时（35）", u"## A5 平台·框架·运行时（46）"),
 (u"### A5.1 自托管平台与环境（7）", u"### A5.1 自托管平台与环境（14）"),
 (u"### A5.2 多代理编排框架（12）", u"### A5.2 多代理编排框架（14）"),
 (u"### A5.4 浏览器/终端/GUI 操作底座（6）", u"### A5.4 浏览器/终端/GUI 操作底座（8）"),
 (u"## A6 评测·基准·观测（23）", u"## A6 评测·基准·观测（29）"),
 (u"### A6.1 综合与终端基准（3）", u"### A6.1 综合与终端基准（5）"),
 (u"### A6.3 任务域基准（4）", u"### A6.3 任务域基准（7）"),
 (u"### A6.5 技能安全评测（5）", u"### A6.5 技能安全评测（6）"),
 (u"## A8 目录·市场·分发渠道（18）", u"## A8 目录·市场·分发渠道（22）"),
 (u"### A8.1 官方插件/技能市场（5）", u"### A8.1 官方插件/技能市场（7）"),
 (u"### A8.4 国内平台商店（3）", u"### A8.4 国内平台商店（5）"),
 (u"## B1 办公·文档·知识工作（4）", u"## B1 办公·文档·知识工作（5）"),
 (u"### B1.2 文档读写与解析工具（2）", u"### B1.2 文档读写与解析工具（3）"),
 (u"## B2 内容·营销·销售经营（7）", u"## B2 内容·营销·销售经营（10）"),
 (u"### B2.1 短视频生产（2）", u"### B2.1 短视频生产（3）"),
 (u"### B2.2 图文与图像生产（2）", u"### B2.2 图文与图像生产（4）"),
 (u"## B3 研究·金融·科学（7）", u"## B3 研究·金融·科学（8）"),
 (u"### B3.1 深度研究与调研（3）", u"### B3.1 深度研究与调研（4）"),
 (u"## B4 软件工程·编码（4）", u"## B4 软件工程·编码（6）"),
 (u"### B4.1 结对编程与代码修改（2）", u"### B4.1 结对编程与代码修改（3）"),
 (u"### B4.3 规格驱动开发方法论（1）", u"### B4.3 规格驱动开发方法论（2）"),
]
for old, new in heads:
    replace_once(old, new)

# ---------- 2) 文件头计数 ----------
replace_once(u"**178 个唯一资产**，全部完成分类",
 u"178 个唯一资产；2026-09-30 合并轮 +40（75 条原始发现 → 同源合并 5 处、30 条为上轮已录条目去重跳过）→ **218 个唯一资产**，全部完成分类")
replace_once(u"共 47 个资产（原 17 + 续跑增补 30） |",
 u"共 77 个资产（原 17 + 续跑增补 30 + 2026-09-30 合并轮 30） |")
replace_once(u"软件系统 72 · 目录渠道 28 · 文档教程 13 · prompt模板 7 · skill 7 · plugin 10 · MCP 12 · 评测集 14 · agent配置 3 · 标准规范 7 · hook 2 · command 1 · 工作流模板 1 · 内容案例 1（合计 178）",
 u"软件系统 92 · 目录渠道 35 · 文档教程 13 · prompt模板 8 · skill 9 · plugin 10 · MCP 13 · 评测集 19 · agent配置 4 · 标准规范 9 · hook 2 · command 1 · 工作流模板 1 · 内容案例 2（合计 218）")
replace_once(u"A1 标准·协议·官方参考 21 · A2 技能·插件·配置件 16 · A3 提示词资产 11 · A4 MCP 工具生态 28 · A5 平台·框架·运行时 35 · A6 评测·基准·观测 23 · A7 治理·审计·成本 4 · A8 目录·市场·分发渠道 18 · B1 办公·文档·知识工作 4 · B2 内容·营销·销售经营 7 · B3 研究·金融·科学 7 · B4 软件工程·编码 4（合计 178）",
 u"A1 标准·协议·官方参考 23 · A2 技能·插件·配置件 20 · A3 提示词资产 12 · A4 MCP 工具生态 33 · A5 平台·框架·运行时 46 · A6 评测·基准·观测 29 · A7 治理·审计·成本 4 · A8 目录·市场·分发渠道 22 · B1 办公·文档·知识工作 5 · B2 内容·营销·销售经营 10 · B3 研究·金融·科学 8 · B4 软件工程·编码 6（合计 218）")

# ---------- 3) 新增条目行 ----------
R = {}

R["A1.2"] = [
u"| [Agent Client Protocol（ACP）](https://github.com/agentclientprotocol/agent-client-protocol)【红队】 | GitHub（agentclientprotocol 独立组织）+ 规范站 agentclientprotocol.com | 标准规范 | 编辑器/IDE 与编码 agent 间通信的开放协议，官方描述 \"A protocol for connecting any editor to any agent\"；本地 JSON-RPC over stdio、远程 HTTP/WebSocket，复用 MCP 的 JSON 表示，定位对标 LSP | 强启发。A1.2 已收 agent↔agent（A2A/ANP）与 agent↔前端（AG-UI），缺 agent↔编辑器环；是把能力封装为「可接入 IDE 的 agent 资产」的分发接口标准，课程讲协议矩阵时的必收参照。编码 agent 非课程主战场，故强启发 | 裁判独立实测 GitHub API：full_name 确为 agentclientprotocol/agent-client-protocol（已非 zed-industries，红队注记属实），4,351 stars、403 forks、Apache-2.0、pushed_at 2026-09-29（活跃维护中） | 【红队】形态盲区-续跑r1 |",
]
R["A1.3"] = [
u"| [modelcontextprotocol/ext-apps（MCP Apps）](https://github.com/modelcontextprotocol/ext-apps)【红队】 | GitHub（modelcontextprotocol 官方组织）+ 文档站 apps.extensions.modelcontextprotocol.io | 标准规范 | MCP Apps 协议官方 spec 与 SDK 仓，官方 description 实测：\"spec & SDK of MCP Apps protocol - standard for UIs embedded AI chatbots, served by MCP servers\"——由 MCP 服务器向聊天机器人提供可嵌入运行的 UI 应用 | 强启发。与已收 ext-skills 完全平行的官方扩展仓，形态互补：skills 封装能力、Apps 封装带 UI 的可分发应用，是「AI 能力封装为可分发资产」的前沿官方形态，与配置体系（MCP）直接相关。当前主战场（办公/内容/个体经营课程）尚未用到嵌入式 UI 应用形态，故强启发 | 裁判独立实测 GitHub API：2,879 stars、392 forks、TypeScript、pushed_at 2026-09-25（活跃）、license NOASSERTION；文档正文未读，能力描述仅依据官方 description 字段 | 【红队】形态盲区-续跑r1 |",
]
R["A2.1"] = [
u"| [BrowserOS Skills（browseros-ai/skills）](https://github.com/browseros-ai/skills) | GitHub（browseros-ai 组织，BrowserOS 同组织；BrowserOS 本体 13,775★/AGPL-3.0） | skill | 安装即 `npx skills add browseros-ai/skills --skill browseros`；browseros 技能经 browseros-cli 提供 54 条命令（导航、交互、截图、内容抽取），让 Claude Code/Gemini CLI/Codex/Cursor 等任意编码 agent 直接控制真实浏览器 | \"npx skills add <org>/<repo>\" 是 agent 技能包分发范式的最小完整实例——我们的资产若做成该格式即可被主流编码 agent 直接安装消费 | 17★，pushed 2026-03-31——小而清晰的官方技能包（组织 15 仓，本体活跃 pushed 2026-09-29）；同组织 moltyflow（18★，\"StackOverflow for AI agents\"）为有趣延伸 | 搜索-同源深挖-续跑r2 |",
]
R["A2.2"] = [
u"| [MAIC-Vibe](https://github.com/THU-MAIC/MAIC-Vibe) | GitHub（THU-MAIC 组织） | skill | README 原文：\"A workshop for AI-native skills — small artifacts that help non-engineers become fluent collaborators with AI coding tools\"；含 skills/ai-native-coach/（Claude Code 技能）等小工具，主张在真实工作中纠偏\"逐行读完再信、先学框架再动手\"等前 AI 时代习惯 | 与我们业务（AI 能力封装+课程体系）假设完全同构的最小参照：面向非工程师的技能包课程怎么做、课什么，可直接对照设计我们的课程 SKU | 8★，pushed 2026-04-29——早期实验性，价值在内容设计而非社区规模；中英双语 README | 搜索-同源深挖-续跑r2〔形态注记：JSON 原标\"提示词集\"，实体含 Claude Code skill（skills/ai-native-coach/），按 skill 形态落格〕 |",
]
R["A2.5"] = [
u"| [Context Hub（context-hub）](https://github.com/andrewyng/context-hub) | GitHub（andrewyng，translation-agent 同作者）+ npm（@aisuite/chub） | 软件系统 | README 原文：给编码 agent 提供\"curated, versioned docs\"，解决\"agents hallucinate APIs and forget what they learn in a session\"；全部内容以 markdown 开放维护在本仓，`npm install -g @aisuite/chub` 后 `chub search` 使用；配套 andrewyng/context-hub-skill（agent skill） | 与我们\"把 AI 能力封装为可分发资产\"完全同构的参照：知识→版本化 markdown 库→npm CLI 分发→agent skill 挂载的完整链路，14K★ 验证了该模式的需求 | 13,984★，MIT，pushed 2026-05-31；npm 包 @aisuite/chub（README 徽章核实）；比 openworker（18,363★，README 未说明用途，未纳入）核实度高 | 搜索-同源深挖-续跑r2〔待归类：编码 agent 版本化文档/上下文供给形态，暂按\"agent 上下文配置件\"就近入 A2.5〕 |",
u"| [Cline Community Prompts（cline/prompts）](https://github.com/cline/prompts) | GitHub（cline 组织） | agent配置 | README 原文：社区驱动的 Cline 规则与工作流合集，规则以 .clinerules/ 目录下 kebab-case 的 md 文件维护，经 fork+PR 贡献，可直接从 Cline 扩展内置 \"Prompts Library\" 浏览应用；同组织另有 cline/clinerules（21★）与 cline/skills（35★，Cline 官方在用技能集） | 提示词资产\"GitHub 仓库为源、产品内置库直接消费、PR 社区贡献\"的分发范式实例，对我们沉淀课程提示词资产和组织社区贡献可直接套用 | 1,213★，pushed 2026-02-27（近 7 个月无新 push，稳定但放缓）；cline/mcp-marketplace（787★）与 cline/kanban（1,342★，并行跑 CLI agent 的本地 web 应用）为同组织备选 | 搜索-同源深挖-续跑r2〔形态注记：JSON 原标\"提示词集\"，实体为 .clinerules 规则文件合集，按 agent配置形态落格，与 PatrickJS/awesome-cursorrules 同位〕 |",
]
R["A3.1"] = [
u"| [system-prompts-and-models-of-ai-tools（原始上游仓）](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)【红队】 | GitHub（x1xhlol 个人） | prompt模板 | 各主流 AI 工具系统提示词与内部工具原文档案，description 实测列举 Claude Code、Cursor、Devin、Manus、Kiro、Lovable、NotionAI、Perplexity 等数十款工具 | 直接可用。清单 A3.1 只录了它的 GitCode 中文汉化版，原始一手来源缺席；系统提示词是工程语料，翻译有损，原文仓不可被译本实质替代——判非异名同物。做提示词语料库应以一手原文为准、镜像仅作加速，143,942 stars 为 A3.1 全段最高量级 | 裁判独立实测 GitHub API：143,942 stars、34,801 forks、GPL-3.0、pushed_at 2026-08-11（约 7 周前更新，仍活跃维护节奏）、未归档 | 【红队】任务盲区-续跑r1 |",
]
R["A4.4"] = [
u"| [GitHub 官方 MCP Server（github/github-mcp-server）](https://github.com/github/github-mcp-server)【红队】 | GitHub（github 官方组织） | MCP | GitHub 官方 MCP Server（官方描述即 \"GitHub's official MCP Server\"），为 agent 提供仓库/issue/PR 等 GitHub 操作工具面 | 直接可用。A4 已收 Google Workspace/Gmail/Shopify/Cloudflare Playwright/Context7，唯独缺 GitHub 官方 server；与配置体系（MCP 配置）和 B4 软件工程产线直接互补，最不该漏的官方任务域 server | 裁判独立实测 GitHub API：33,274 stars、5,067 forks、pushed_at 2026-09-29T14:44:04Z（当日活跃）、MIT、未归档，description 字段逐字核实 | 【红队】任务盲区-续跑r1〔待归类：编码协作域任务 server，A4.3/A4.4 细类均为办公/浏览器/电商域，暂就近入 A4.4〕 |",
]
R["A4.5"] = [
u"| [aisuite](https://github.com/andrewyng/aisuite) | GitHub（andrewyng 账号，translation-agent 同作者） | 软件系统 | \"Simple, unified interface to multiple Generative AI providers\"（API 简介）：一套类 OpenAI 接口统一调用各家 LLM 厂商，适合做厂商无关的评测/课程代码层 | 评测与课程体系的多厂商适配层直接参考：把 GLM 等国产模型接入统一接口的轻量封装模式，可复用到我们的打分器/出卷器管线 | 16,318★/1,723 forks，MIT，pushed 2026-09-18，活跃成熟；同作者另一仓库 translation-agent 已停更（pushed 2024-08-04），aisuite 是其现役主仓 | 搜索-同源深挖-续跑r2〔待归类：多厂商模型统一接口层，非 MCP 专属，与 OpenRouter/LiteLLM 同层暂入 A4.5，宜增设「模型网关」细类〕 |",
]
R["A4.6"] = [
u"| [npm registry（MCP server / 技能包默认分发渠道）](https://registry.npmjs.org/)（registry 根 + [npmjs.com/search](https://www.npmjs.com/search?q=mcp-server) 搜索页 + registry /-/v1/search API，三源合并条目）【红队】 | npm registry | 目录渠道 | 全球 JS 包注册表，MCP server 与 agent 技能包事实上的主分发通道（npx 安装）；清单收录了十余个 MCP 目录站，唯独缺上游包注册表本体；实测 registry 搜索 API：keywords:mcp-server 约 9,247-9,248 包（宽口径 text=mcp-server 命中 393,761，宽松分词计数只作量级）、keywords:mcp 76,425；Sentry/Notion/Chrome DevTools 等厂商官方 MCP server 均以 npm 包分发且周更活跃（@sentry/mcp-server 0.42.0、@notionhq/notion-mcp-server 2.5.2），头部包 chrome-devtools-mcp 月下载约 790 万、@notionhq/notion-mcp-server 约 67 万/月 | 【裁判判：直接可用】(1) 自研 MCP/技能包的默认发布渠道（@scope 官方包命名惯例、版本化、语义化发布皆可在此直接观测）；(2) 供应链安全评测的天然抽样对象池，规模足以支撑\"技能/MCP 供应链风险\"评测集抽样；(3) npm 周下载量是免费可查的市场需求信号，可用于选品与竞品监测；MCP 形态资产的零成本默认上架渠道，与阿里云百炼（国内渠道）构成双渠道策略 | 裁判 2026-09-30 本机实跑搜索 API：text=keywords:mcp-server → total=9,247、text=keywords:mcp → total=76,425（与红队 09-29 实测 9,245/76,416 吻合，属日增长）；官方 @modelcontextprotocol/server-filesystem dist-tags.latest=2026.8.31（modified 2026-09-17）；api.npmjs.org 下载统计实测 @modelcontextprotocol/server-filesystem 周下载 624,049（2026-09-21~09-27） | 【红队】渠道盲区-续跑r2；裁判 r2 独立复跑核实 + 搜索-邻接域-续跑r2 + 搜索-形态补全-续跑r2（三源合并条目）〔待归类：npm 并非 MCP 专属，按 TAXONOMY §二.1 严格应归 A8，暂按\"MCP/技能包默认包分发渠道\"语义就近入 A4.6〕 |",
u"| [阿里云百炼 MCP（官方托管 MCP 服务 + MCP 市场 + 云部署计费）](https://docs.bailian.console.aliyun.com/zh/model-studio/mcp-introduction)（百炼文档入口 + [help.aliyun.com/zh/model-studio/mcp](https://help.aliyun.com/zh/model-studio/mcp) 帮助文档入口，合并条目）【红队】 | 阿里云百炼（Model Studio）官方文档 | 目录渠道 | 阿里云百炼官方托管 MCP 服务 + 用户自定义 MCP 云部署：基础模式按调用秒计费 0.000156 元/秒、极速模式另收部署费 0.000036 元/秒；《qwen api 如何接入 MCP》实测：经 Qwen Responses API 的 tools 参数挂载 MCP server（当前仅支持 SSE、最多 10 个），计费分两层——模型推理按 token、MCP 服务费用以各 MCP 服务的计费为准；含「开通云部署 MCP 服务」入口与内置 WebParser（网页解析）示例；补上国内渠道版图唯一空缺的阿里系（清单已有火山/Dify/百度/扣子/腾讯/Kimi） | 【裁判判：强启发】国内能力分发参照系：按秒计费的托管 MCP 执行价可直接抄进我们的成本模型；官方托管 + 按 MCP 服务独立计费的商业化形态是我方 MCP 资产在国内分发/计费的对接样板；课程讲国内 MCP 托管模式时与火山引擎 MCP 市场成对对照 | 裁判 2026-09-30 WebFetch 复访实测文档页在线，两档费率原文逐句确认；英文文档同步核实（BYO endpoint，可接 ModelScope 托管 server，英文页标注更新于 2026-09-28）；MCP 市场本体在登录态控制台，裁判与红队均未登录、市场条目数未核实（如实保留此限制）；注意 help.aliyun.com/zh/model-studio/mcp-service 旧链接实测已 404 | 【红队】渠道盲区-续跑r2；裁判 r2 独立复访核实 + 搜索-邻接域-续跑r2（合并条目） |",
u"| [@modelcontextprotocol/server-filesystem（npm 上的 MCP 官方参考 server 包）](https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem) | npm registry | 目录渠道（MCP server / 技能包默认包分发渠道） | registry API 实测：latest 版本 2026.8.31，描述「MCP server for filesystem access」，repo 指向 github.com/modelcontextprotocol/servers，modified 2026-09-17；api.npmjs.org 下载统计实测周下载 624,049（2026-09-21~09-27）；keywords:mcp-server 搜索 API 亦实测可用，返回大量第三方 MCP server 包 | 证明『把 agent 能力封装成 npm 包』是 MCP 生态默认分发形态，我们发布能力资产可完全复用此通道；npm 周下载量是免费可查的市场需求信号，可用于选品与竞品监测 | 高频活跃：单包周下载 62 万+，版本号按日期滚动（2026.8.31） | 搜索-跳板扩展-续跑r2〔注记：server 本体已含于 A4.1 modelcontextprotocol/servers（Filesystem），本条以 npm 包分发面立目〕〔待归类：非 MCP 专属包分发面，同 npm registry 暂入 A4.6〕 |",
]
R["A5.1"] = [
u"| [Dify 平台本体（langgenius/dify）](https://github.com/langgenius/dify)【红队】 | GitHub（langgenius 官方组织） | 软件系统 | 可视化编排 Agentic workflow 与 RAG pipeline 的一体化开源平台，官方描述：\"Build Agentic workflows, RAG pipelines, with rich AI model and tool support on one collaborative workspace\"，自带插件生态 | 直接可用。清单 A8.4 收了 Dify 插件市场、A2.6 收了其 DeepSeek/MCP 插件与 Agent Strategies，本体缺席构成引用依赖倒置的硬缺口；国内最主流自托管 agent 平台，是办公/个体经营场景应用宿主与课程必收参照，也可作被评测平台 | 裁判独立实测 GitHub API（2026-09-29）：157,495 stars、24,825 forks、pushed_at 2026-09-29T14:36:35Z（当日活跃）、未归档、license NOASSERTION（商用需核许可文本） | 【红队】渠道盲区-续跑r1 |",
u"| [Langflow](https://github.com/langflow-ai/langflow)【红队】 | GitHub（langflow-ai 官方组织） | 软件系统 | 可视化构建与部署 AI agent 和工作流的低代码平台（官方描述：\"Langflow is a powerful tool for building and deploying AI-powered agents and workflows\"），组件图式编排 | 强启发。与已收 n8n/LibreChat/Coze Studio 同属 A5.1 却缺席的国际侧可视化编排代表；其组件/模板生态是能力资产分发的参照系。可视化编排主位已由 Dify 补上，故判强启发而非直接可用 | 裁判独立实测 GitHub API：155,367 stars、10,154 forks、pushed_at 2026-09-29T14:40:30Z（当日活跃）、MIT、未归档 | 【红队】渠道盲区-续跑r1 |",
u"| [RAGFlow](https://github.com/infiniflow/ragflow)【红队】 | GitHub（infiniflow 官方组织） | 软件系统 | 开源 RAG 引擎，官方描述：\"RAGFlow is a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with Agent capabilities\" | 直接可用。A5.1 整段无 RAG/知识库专项平台，属结构性空白；文档问答/知识工作正是雇主课程主战场，RAG 引擎是该场景最常见宿主环境 | 裁判独立实测 GitHub API：91,492 stars、10,863 forks、pushed_at 2026-09-29T14:56:58Z（当日活跃）、Apache-2.0、未归档 | 【红队】渠道盲区-续跑r1 |",
u"| [FastGPT](https://github.com/labring/FastGPT)【红队】 | GitHub（labring 官方组织） | 软件系统 | 基于 LLM 的知识库问答平台，GitHub 官方描述确认含数据处理、RAG 检索、可视化 AI 工作流编排等开箱能力 | 直接可用。与 RAGFlow 一并补上 A5.1 的 RAG 空白，且补的是中文生态位；对面向国内客户交付知识型 agent 有直接参照价值 | 裁判独立实测 GitHub API：29,769 stars、7,326 forks、pushed_at 2026-09-29T14:38:56Z（当日活跃）、license NOASSERTION（商用需核许可文本） | 【红队】渠道盲区-续跑r1 |",
u"| [Cherry Studio（桌面端 AI 客户端宿主，支持 MCP + Agent Skills）](https://github.com/CherryHQ/cherry-studio)【红队】 | GitHub | 软件系统（桌面客户端形态） | Electron 桌面 AI 客户端（Windows/Mac/Linux）：统一接入各大 LLM、300+ 预置助手、自主 Agent、MCP server 集成、企业级知识库；仓库 topics 含 agent-skills，即已支持技能加载 | 【裁判判：直接可用】清单 A5.1 宿主全是自托管 Web 形态、桌面客户端为零，形态不重复：它是把 MCP/技能投放到\"非开发者桌面端\"的现成宿主——个体经营者学员最容易上手的落地环境，课程实验与配置体系教学可直指此宿主 | 裁判 2026-09-30 GitHub API 实测：52,239 stars / AGPL-3.0 / pushed 2026-09-29，与红队口径一致；AGPL-3.0 双轨（社区开源+商业许可）以仓库 license 字段与红队描述互证 | 【红队】形态盲区-续跑r2；裁判 r2 独立复跑核实〔注记：桌面客户端形态宿主，非自托管 Web 服务，按 A5.1 宿主语义就近〕 |",
u"| [verl（HybridFlow：LLM/agentic RL 后训练框架；实测已迁 verl-project 组织）](https://github.com/verl-project/verl)【红队】 | GitHub（字节 Seed 发起，已迁移至 verl-project 组织） | 软件系统（RL 训练框架形态） | 面向生产的 RL 后训练框架（RLHF/RLVR）：PPO/GRPO/GSPO/DAPO 等算法 + SFT；multi-turn rollout 与工具调用（agentic RL）、search tool/Sandbox Fusion 集成、VLM 多模态 RL；兼容 Qwen3 系等并支持 671B 级数百卡扩展，硬件覆盖 NVIDIA/AMD ROCm/华为昇腾 | 【裁判判：强启发】清单形态覆盖推理/编排/评测/观测而\"训练/RL 框架\"为零；雇主手握 2×V100S GPU 机（anolis-gpu-01），verl 是从\"会评\"走向\"会训\"的 agentic RL 底座，国产（字节）出品且昇腾可用，适配国内算力环境 | 裁判 2026-09-30 GitHub API 实测：API 规范名已变为 verl-project/verl（红队\"已迁移组织\"说法确认，引用请用新地址）、23,694 stars / Apache-2.0 / pushed 2026-09-29，与红队口径一致 | 【红队】形态盲区-续跑r2；裁判 r2 独立复跑核实（确认组织迁移）〔待归类：训练/RL 框架形态，A5 无对应细类，暂按自托管运行时底座就近入 A5.1，宜增设「训练·RL 框架」细类〕 |",
u"| [Uni-Agent（uni-agent）](https://github.com/verl-project/uni-agent) | GitHub（verl-project 组织，verl 同组织；verl 原字节 Seed 发起，volcengine/verl 已 301 迁移至 verl-project/verl，23,695★，本次 API 实测确认） | 软件系统（RL 训练框架形态） | README 标题：\"Uni-Agent: Train Long-Horizon Agents at Scale\"——训练长时程 agent 的框架，\"Bring any exi(sting)...\"（可接现有 agent，README 截断处未读全）；文档 uni-agent.readthedocs.io | verl 生态中专门面向 agentic RL 的组件：若我们把打分器/agent 做后训练（如 mutual P0 打分器复盘），它是比 verl 本体更对口的入口；也补齐\"评测→训练\"闭环的国产可用件 | 640★，Apache-2.0，pushed 2026-09-28，活跃；同组织 verl-omni（1,137★，多模态扩散/omni 模型 RL）、verl-recipe（335★，端到端 RL 配方）可作延伸 | 搜索-同源深挖-续跑r2〔待归类：长程 agent RL 训练框架，A5 无对应细类，同 verl 暂入 A5.1，宜增设「训练·RL 框架」细类〕 |",
]
R["A5.2"] = [
u"| [CrewAI](https://github.com/crewAIInc/crewAI)【红队】 | GitHub（crewAIInc 官方组织） | 软件系统 | 角色化（role-playing）多代理编排框架，GitHub 官方描述：\"Framework for orchestrating role-playing, autonomous AI agents\"，以 Agent/Task/Crew 抽象组队 | 直接可用。A5.2 已收 LangGraph/Google ADK/smolagents/deepagents 等，却缺角色制范式的最高声量代表——编排课程与能力封装章节的最大单点盲区 | 裁判独立实测 GitHub API：59,182 stars、8,607 forks、pushed_at 2026-09-29T15:06:46Z（当日活跃）、MIT、未归档 | 【红队】任务盲区-续跑r1 |",
u"| [Microsoft Agent Framework（MAF）](https://github.com/microsoft/agent-framework)【红队】 | GitHub（microsoft 官方组织） | 软件系统 | 微软现役官方多语言 agent 与多代理工作流框架（Python/.NET），生态对接 Microsoft Foundry/Azure OpenAI/OpenAI/Copilot SDK，含 MS Learn 官方文档与 PyPI/NuGet 包 | 直接可用。清单已收 OpenAI Agents SDK、LangGraph、Google ADK，唯独缺微软现役官方框架；企业客户课程与交付栈补上微软系一环 | 裁判独立实测 GitHub API：13,863 stars、pushed_at 2026-09-29T14:58:42Z（当日活跃）、MIT；对照实测 microsoft/autogen（61,218 stars）最后推送 2026-04-15——官方重心确已迁至 MAF，选型应取 MAF | 【红队】任务盲区-续跑r1 |",
]
R["A5.4"] = [
u"| [Stagehand（browserbase/stagehand）](https://github.com/browserbase/stagehand)【红队】 | GitHub（browserbase 官方组织）+ 官网 stagehand.dev | 软件系统 | 网页数据抽取与站点交互 SDK，官方描述实测：\"The SDK to extract data and interact with any site on the web\"，TypeScript 为主、构建于 Playwright/CDP 之上，官方 README 提及与 Claude Code/Codex/Mastra 等集成 | 强启发。A5.4 已有 Python 库形态（browser-use）与 CLI 形态（vercel-labs/agent-browser），缺生产级 TS SDK 形态；对把浏览器作业封装成可复用/可分发组件（雇主核心命题）、搭网页任务评测产线是现成底座，个体经营场景（社媒/电商运营自动化）有潜在课程场景。形态增量属补强而非硬缺口，故强启发 | 裁判独立实测 GitHub API：25,460 stars、1,744 forks、MIT、TypeScript、pushed_at 2026-09-29（活跃）、未归档 | 【红队】形态盲区-续跑r1 |",
u"| [BrowserOS（开源 Agentic 浏览器，Chromium fork）](https://github.com/browseros-ai/BrowserOS)【红队】 | GitHub | 软件系统（浏览器应用形态） | 开源 Chromium fork（含 ungoogled-chromium 隐私补丁），新标签页内置 AI agent；双产品线：BrowserOS（人类用浏览器+agent，可自带 API key 或 Ollama 本地模型）与 BrowserOS neo（面向 agent 的第二浏览器，经 MCP 连接 Claude Code/Codex/Cursor 等 coding agent）；自带 MCP server，差异点是全本地运行（127.0.0.1）且保留真实登录态 | 【裁判判：强启发】清单 A5.4 全是库/CLI 形态（browser-use/stagehand/codex 等）、\"浏览器产品\"形态为零且不重复：带登录态的本地执行底座与已有库形态互补；对课程则是给个体经营者演示浏览器自动化的可视化载体，对配置体系是 MCP 连接的另一类宿主 | 裁判 2026-09-30 GitHub API 实测：13,775 stars / 1,467 forks / AGPL-3.0 / pushed 2026-09-29，与红队口径一致；最近 release 具体日期未单独核实（红队已如实注明页面未显示） | 【红队】形态盲区-续跑r2；裁判 r2 独立复跑核实 |",
]
R["A6.1"] = [
u"| [TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany)【红队】 | GitHub（TheAgentCompany 组织，官网 the-agent-company.com） | 评测集 | 以数字员工方式（浏览网页、写代码、跑程序、与虚拟同事沟通）评测 agent 完成真实职业任务的基准，官方描述 \"An agent benchmark with tasks in a simulated software company\"，含官网/Leaderboard/论文 arXiv 2412.14161 | 强启发。A6.1 缺「知识工作综合任务」基准位，其任务设计与计分法对雇主建评测体系（办公/知识工作主战场）可直接对标；但项目已停滞且需自建浏览器+执行环境，作设计参照而非拿来即用 | 裁判独立实测 GitHub API：786 stars、126 forks、MIT、最后推送 2025-11-17（至 2026-09-29 约 10 个月未更新，使用注意时效）；官网为 JS 渲染，以 GitHub README/API 为准 | 【红队】任务盲区-续跑r1 |",
u"| [GAIA（General AI Assistants Benchmark）](https://huggingface.co/datasets/gaia-benchmark/GAIA)【红队】 | Hugging Face Datasets（gaia-benchmark 组织） | 评测集 | 通用 AI 助理基准官方数据集，HF cardData 实测 pretty_name 为 \"General AI Assistants Benchmark\"，gated 发放并带防污染条款 | 直接可用（评测体系标准件）。A6 各细类无任何通用助理基准，GAIA 是该位事实行业标准，评测体系与课程实验绕不开；gated=auto 意味着使用需申请，课程设计需预留该门槛 | 裁判独立实测 HF API：gated=auto、非私有、854 likes、10,754 downloads、lastModified 2025-10-28；GitHub 侧 gaia-benchmark/GAIA 实测 404（红队注记属实，主库在 HF） | 【红队】任务盲区-续跑r1 |",
]
R["A6.3"] = [
u"| [SWE-Gym（软件工程 agent 开源训练环境 + 数据集）](https://github.com/SWE-Gym/SWE-Gym)【红队】 | GitHub（数据集与模型在 Hugging Face SWE-Gym 组织） | 评测集 | 首个用于训练真实世界软件工程 agent 与验证器的开源训练环境（ICML 2025 论文配套）：11 个 Python 仓库 2.4K 真实任务 + 可执行环境 + 测试验证；支持 OpenHands/Moatless 两种 scaffold，用于拒绝采样微调、轨迹训练验证器 best-of-n 与在线 RL；数据集/模型在 Hugging Face，提供预构建 Docker 镜像 | 【裁判判：强启发】清单 A6 全是\"测\"（评测集/评测平台）而无\"训\"：SWE-Gym 是\"环境即资产+评测训练闭环\"的最小完整样本，其 HF 数据集可复用于雇主已有 LoRA/微调类资产线；判强启发而非直接可用，因 commit 少且非持续迭代产品 | 裁判 2026-09-30 GitHub API 实测：747 stars / 46 forks / Apache-2.0 / pushed_at=2025-07-29（约 14 个月未推送）——与红队\"34 commits、非持续迭代型\"的降级标注一致，采信 | 【红队】形态盲区-续跑r2；裁判 r2 独立复跑核实〔形态注记：训练环境+数据集，清单 14 形态中无此形态，暂按最接近的评测集落格〕 |",
u"| [cline-bench](https://github.com/cline/cline-bench) | GitHub（cline 组织，Cline 本体同组织） | 评测集 | README 原文：\"Real-world coding benchmarks derived from actual Cline user sessions\"——从真实用户会话提取、经人工 verified 的工程任务；本地 Docker 测试 + Daytona 云执行，依赖 Python 3.13/uv/LLM API key；任务在 tasks/ 目录；出处 cline.bot/blog/cline-bench-initiative | \"从真实使用会话构造评测集\"的方法论样板，直接可借鉴到我们评测体系（mutual 打分器、AI_Web_School 出卷器）的任务采集与验证流程 | 39★，Apache-2.0（组织列表），pushed 2025-12-11，README 标题即 \"early access\"——早期/内测阶段，但组织背景（cline 69,555★ 主仓）可信 | 搜索-同源深挖-续跑r2 |",
u"| [SWE-Gym 数据集（SWE-Gym/SWE-Gym）](https://huggingface.co/datasets/SWE-Gym/SWE-Gym) | Hugging Face（SWE-Gym 组织；GitHub 侧 SWE-Gym/SWE-Gym 747★，arXiv 2412.21139，ICML 2025） | 评测集 | 数据集卡实测：2,438 条训练实例、源自 11 个 Python 仓库、按 SWE-Bench 流程采集；字段含 problem_statement/patch/test_patch/PASS_TO_PASS/FAIL_TO_PASS（即带可执行验证的训练环境）；MIT；train split 约 214MB | 唯一开源的 SWE agent 训练环境级数据（非纯静态题）：字段结构是\"任务+补丁+测试+通过判定\"的标范，可套用到我们的打分器训练数据设计与 holdout 纪律（FAIL_TO_PASS 分离可对应我们的 golden 不入训） | 34,412 下载/29 赞，lastModified 2025-05-10——论文配套定稿不再更新；同组织 SWE-Gym-Lite（11,640 下载）、OpenHands-SFT-Trajectories（821 下载）及 8 个 Agent/Verifier 模型构成完整收割物合集 | 搜索-同源深挖-续跑r2〔形态注记：数据集，按 14 形态体系暂归最接近的评测集形态落格〕 |",
]
R["A6.5"] = [
u"| [Lakera Agent Breaker（原 Gandalf 提示注入靶场）](https://play.lakera.ai/agent-breaker)【红队】 | Lakera（在线靶场站点） | 内容案例 | 免费交互式提示注入靶场：GenAI 应用商店场景（页面原文 \"an entire app store of GenAI applications - and every single one of them can be hacked\"），逐关攻击目标含抽取系统提示词、窃取敏感数据、操纵 LLM 攻击其他用户；每次攻击按 0-100 评分、75+ 解锁下一关、含总榜排行榜 | 【裁判判：强启发】清单评测/安全资产全是数据集与扫描框架，\"在线交互靶场\"形态为零：可直接嵌入安全课程作交互实验环节，其\"关卡化+评分+解锁+排行榜\"机制是游戏化评测设计的现成范本，贴合课程体系建设 | 裁判 2026-09-30 实测：WebFetch 仅得 JS 壳（标题 \"Lakera – Test your AI hacking skills\"），改用 web_reader 取得正文，评分/解锁/排行榜/攻击目标原文逐句确认。在线服务非开源项目，无 stars/release 可考，运营方为安全公司 Lakera | 【红队】形态盲区-续跑r2；裁判 r2 独立复访核实〔形态注记：在线交互靶场，按内容案例形态落格；A6×内容案例矩阵格由「—」改 ●1〕 |",
]
R["A8.1"] = [
u"| [Salesforce AgentExchange（原 AppExchange，企业级 agent 统一市场）](https://agentexchange.salesforce.com/)（官方店面 + [营销页 salesforce.com/agentforce/agentexchange](https://www.salesforce.com/agentforce/agentexchange/) + [appexchange.salesforce.com](https://appexchange.salesforce.com/) 旧址，三源合并条目）【红队】 | Salesforce 官网 | 目录渠道 | 官方店面页实测（HTTP 200）：\"AgentExchange is the unified marketplace to discover, buy, and deploy trusted agents, apps, and capabilities that extend Salesforce\"；营销页实测标题 \"AgentExchange: One Unified Marketplace for the Agentic Enterprise\"，CTA 直链店面；页面自述分发第三方 agents、sub-agents、MCP servers，可在 Agentforce Builder 内直接接入，发现由 Data Cloud 语义驱动，含统一账单、私有报价与安全审核；appexchange.salesforce.com 页面标题即「Salesforce AppExchange is now AgentExchange」，证实原 AppExchange 已整体品牌转型 | 【裁判判：强启发】企业级 CRM 生态的 agent/MCP 商品化上架样板，补齐清单 A8 完全缺失的\"企业软件市场\"分发通道；课程讲能力分发渠道时与 Claude Marketplace、AWS Marketplace 构成三足对照；listing 组织方式、与宿主平台（Agentforce/CRM）的\"发现-购买-激活\"集成、partner 上架路径是企业级 agent 资产定价与上架标准样板。我们资产尚未到企业市场上架阶段，故记强启发而非直接可用 | 裁判 2026-09-30 WebFetch 复访实测营销页在线：\"find, evaluate, and plug in trusted third-party agents, sub-agents, and MCP servers\"、\"Discover and deploy ready-to-use agents and tools directly within Agentforce Builder\"、15,000+ Partnerblazers 均确认；店面 agentexchange.salesforce.com 亦实测 200（店面条目标题 \"AgentExchange \\| Marketplace for Agents, Apps & Capabilities\"，「\\|」为 GFM 表格转义）；⚠️ salesforce.com/agentexchange/ 旧址在一轮实测中经 curl 与 WebFetch 双通道 404（跟随重定向追加 ?bc=HL，疑似区域/反爬拦截）；listing 具体条目量为动态加载未核实，市场含 50+ 在线 MCP server、200+ 合作伙伴之说仅来自二手搜索结果 | 【红队】渠道盲区-续跑r2；裁判 r2 独立复访核实 + 搜索-邻接域-续跑r2 + 搜索-形态补全-续跑r2（三源合并条目） |",
u"| [AWS Marketplace「AI Agents & Tools」分类（企业采购级 agent/MCP 分发位）](https://aws.amazon.com/marketplace/solutions/ai-agents-and-tools)【红队】 | AWS 官网 | 目录渠道 | AWS Marketplace 内 AI agents 专项分类：pre-built agents、agent tools（页面明确列 MCP servers、knowledge bases、guardrails、web search tools）、agent 开发方案与专业服务；支持 pay-as-you-go 与合同订阅、私有报价，可部署于 Amazon Bedrock AgentCore | 【裁判判：强启发】\"企业软件采购流程\"这条与 GitHub/MCP 目录站完全不同的分发通道；其 PAYG/合同双轨定价是我们 MCP/agent 资产面向企业客户时的定价参照，也是评测体系应覆盖的采购形态 | 裁判 2026-09-30 WebFetch 复访实测：原文 \"ready-to-integrate tools including MCP servers, knowledge bases, guardrails, and web search tools\"、\"pay-as-you-go and contract subscriptions\"、Bedrock AgentCore 专节、Forrester 2025-05 TEI 引证（采购省时 60%）均确认 | 【红队】渠道盲区-续跑r2；裁判 r2 独立复访核实 |",
]
R["A8.4"] = [
u"| [文心智能体平台 AgentBuilder](https://agents.baidu.com)【红队】 | 百度（官网） | 目录渠道 | 百度基于文心大模型的智能体开发与分发平台，支持 prompt 编排低成本开发智能体 | 直接可用（渠道位）。A8.4 只有 Dify 插件市场/Kimi+ 广场/腾讯元器，漏百度头部入口；裁判实测页面 description 原文含「为智能体开发者提供相应的流量分发路径，完成商业闭环」，其分发+商业闭环模式可作渠道设计直接参照 | 裁判独立实测（python 直抓，2026-09-29）：HTTP 200，title「文心智能体平台AgentBuilder \\| 想象即现实」（「\\|」为 GFM 表格转义，站方原标题含竖线），官方 description 全文抓取成功；平台内部智能体列表为 JS 应用，规模未逐一核实 | 【红队】渠道盲区-续跑r1 |",
u"| [扣子商店（coze.cn/store）](https://www.coze.cn/store)【红队】 | 扣子/字节（官网） | 目录渠道 | 扣子国内版官方商店入口，与清单已收的 Coze Studio（平台本体，A5.1）、Coze Loop（评测，A6.4）构成三条线，本条补渠道位 | 直接可用（渠道位）。清单收了扣子的本体与评测却无官方商店，属渠道盘点硬缺口；国内最大体量 agent 商店之一 | 裁判独立实测（python 直抓）：HTTP 200，title「扣子 - AI Agent智能办公平台 - 扣子用AI重塑生产力与工作效率」，keywords 含「扣子, Coze, AI Agent, 智能办公」；商店条目列表为前端 JS 渲染未能抓取，规模未核实（诚实注记） | 【红队】渠道盲区-续跑r1 |",
]
R["B1.2"] = [
u"| [translation-agent（Andrew Ng 反思翻译工作流）](https://github.com/andrewyng/translation-agent)【红队】 | GitHub（andrewyng） | 软件系统 | 三段式反思机器翻译：初译→LLM 反思提出改进建议→按建议优化译文；可控正式/非正式语气、术语表一致性、地区方言；单函数接口 | 【裁判判：强启发】价值在方法论而非工具：三段式\"初稿-评审-修订\"工作流与雇主判官实验室同构，是现成的提示词工程教学案例，可打包为方法论 skill/课程资产；作生产工具不合格 | 裁判 2026-09-30 GitHub API 实测：5,817 stars / MIT / pushed_at=2024-08-04（近两年未动），与红队\"29 commits、自述 not mature software\"的降级标注一致——红队此条未美化，采信其方法论定位 | 【红队】任务盲区-续跑r2；裁判 r2 独立复跑核实〔待归类：翻译/本地化任务域在 B 段无主类目，暂按\"文档读写转换\"就近入 B1.2，宜增设「翻译·本地化」任务域〕 |",
]
R["B2.1"] = [
u"| [Podcastfy（NotebookLM 播客功能开源替代）](https://github.com/souzatharsis/podcastfy)【红队】 | GitHub（souzatharsis） | 软件系统 | 把网页、PDF、图片、YouTube、自定义主题转多语言音频对话播客（NotebookLM 播客功能开源替代）：100+ LLM 生成对话稿、TTS 支持 OpenAI/Google/ElevenLabs/Edge、多说话人对话式 TTS；Python API / CLI / FastAPI / Docker 部署 | 【裁判判：直接可用】课程资产音频化（课程→播客/音频课）的现成生产管线，正中内容创作主战场；\"多模态输入→脚本→TTS\"管线本身也是可封装分发的资产 | 裁判 2026-09-30 GitHub API 实测：6,578 stars / Apache-2.0，与红队口径一致；但 pushed_at=2026-05-04，已约 5 个月无推送——红队未披露此停更事实，引用时注意维护风险（功能成型可用，与红队其余声称无矛盾） | 【红队】任务盲区-续跑r2；裁判 r2 独立复跑核实（补充停更事实）〔待归类：音频/播客生产无对应细类，暂按\"音视频内容生产\"就近入 B2.1〕 |",
]
R["B2.2"] = [
u"| [OpenMAIC（清华多 Agent 互动课堂）](https://github.com/THU-MAIC/OpenMAIC)【红队】 | GitHub（THU-MAIC 组织，清华大学团队） | 软件系统 | 输入主题或文档生成沉浸式课程：语音讲解、白板画图、随堂提问、互动测验（单选/多选/简答）+ AI 实时批改、.pptx 课件生成导出、MP4 导出、圆桌辩论、PBL、3D/思维导图/在线编程等交互模式；Docker Compose / Vercel / 本地 pnpm 三种部署 | 【裁判判：直接可用】与雇主评测与课程体系业务线（AI_Web_School 出卷器方向）同域的开源竞品：测验生成+AI 批改+课件生成正是自有能力的对标物，可作评测标的、功能基准或 MIT 协议下二开集成对象——这是本轮全部候选中离雇主主业最近的一条 | 裁判 2026-09-30 GitHub API 实测：39,524 stars / 6,130 forks / license=MIT / pushed 2026-09-29；releases/latest 实测 v1.1.2 发布于 2026-09-28，与红队声称逐一吻合（红队无夸大）。652 commits 口径未单独复验 | 【红队】任务盲区-续跑r2；裁判 r2 独立复跑核实〔待归类：教育教学任务域在 B 段无主类目，暂按\"课件/图文内容生产\"就近入 B2.2，宜增设「教育教学」任务域〕 |",
u"| [MAIC-UI](https://github.com/THU-MAIC/MAIC-UI) | GitHub（THU-MAIC 组织，OpenMAIC 清华团队同组织） | 软件系统 | README 原文：\"Making Interactive Courseware with Generative UI\"，论文 arXiv 2604.25806——53 名高中生 3 个月真实课堂部署，证明 MAIC-UI 提升学习自主性并降低结果差距；把抽象知识生成可交互课件，支持真实课堂的稳定生成结果 | 清华多 agent 课堂生态中比 OpenMAIC 本体更贴近\"课件生产\"的一环，其课堂实测方法论（53 人 3 个月）是我们做 AI 课程评测的实验设计参考 | 168★，pushed 2026-05-06；有论文+真实课堂部署背书；同组织 dsh-openmaic（83★）把 OpenMAIC 接入 DeepSeek Harness（工具注册 + 苏格拉底教学 skill，服务端 open.maic.chat） | 搜索-同源深挖-续跑r2〔待归类：教育教学任务域，同 OpenMAIC 暂入 B2.2〕 |",
]
R["B3.1"] = [
u"| [WrenAI（GenBI / text-to-SQL Agent 引擎）](https://github.com/Canner/WrenAI)【红队】 | GitHub（Canner 组织） | 软件系统 | 开源 GenBI 引擎：MDL 语义层（YAML/Markdown 定义、Git 管理）、受治理 text-to-SQL（dry-plan 校验、行数限制、结构化错误）、Agent 直接生成并部署仪表盘；对接 Claude Code/Cursor/Cline/MCP 等 50+ agent，`npx skills add Canner/WrenAI` 一条命令装 skill；20+ 数据源 | 【裁判判：强启发】两头有价值：(1) 办公/经营数据分析是课程主战场的邻接场景；(2) \"语义层 + npx skills add 技能包分发\"本身就是把能力封装为可分发资产的成熟范本，对配置体系（skill 分发机制）有直接参照价值 | 裁判 2026-09-30 GitHub API 实测：17,781 stars / pushed 2026-09-29 / license=NOASSERTION（多许可混合；红队标注 Apache-2.0 核心 + AGPL-3.0/CC-BY-4.0 部分、商用需分模块核许可——该警示属实且必要） | 【红队】任务盲区-续跑r2；裁判 r2 独立复跑核实〔待归类：数据分析/BI 任务域在 B 段无主类目，暂按\"数据调研分析\"就近入 B3.1，宜增设「数据分析·BI」任务域〕 |",
]
R["B4.1"] = [
u"| [Cline（本体：SDK/IDE 扩展/CLI/桌面应用多形态分发的自主编码 agent）](https://github.com/cline/cline)【红队】 | GitHub | 软件系统（IDE 扩展形态 agent） | 开源自主编码 agent，同一能力以 VSCode 扩展、CLI（npm i -g cline，支持 headless/CI）、桌面应用、SDK（@cline/sdk）等多形态分发；支持 MCP、Plan/Act 模式、.clinerules、skills、插件系统、多代理团队与定时任务 | 【裁判判：直接可用】清单只收了 Cline 的插件分发机制文档三页（A1.4），本体缺位——文档切片与本体非同一物，不构成重复。本体恰是雇主核心命题\"一套 AI 能力封装为多种可分发形态\"的最完整活样本；其 .clinerules/skills/插件三层封装结构可直接对照进配置体系课程 | 裁判 2026-09-30 GitHub API 实测：69,552 stars / 7,550 forks / Apache-2.0 / pushed 2026-09-29，与红队口径一致；JetBrains 插件闭源一点未单独复验（README 口径采信） | 【红队】形态盲区-续跑r2；裁判 r2 独立复跑核实 |",
]
R["B4.3"] = [
u"| [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)【红队】 | GitHub（bmad-code-org 组织） | 软件系统（方法论+可安装工作流包） | Breakthrough Method for Agile AI Driven Development（官方描述实测核实），围绕角色化代理团队组织敏捷软件交付的方法论框架，topics 含 agile/sdlc/spec-driven-development/context-engineering | 强启发。B4.3 仅收 github/spec-kit，BMAD 补上更重的方法论形态——非单点工具而是整套角色化代理工作流，可直接拆解进方法论课程与交付模板资产；声量 5.3 万 star 级为该段最大缺席者。license 为 NOASSERTION，商用复用前须人工核查许可文本 | 裁判独立实测 GitHub API：53,629 stars、6,040 forks、pushed_at 2026-09-29T12:49:45Z（高频活跃）、license=NOASSERTION（红队注记属实）、未归档 | 【红队】形态盲区-续跑r1 |",
]

anchors = {
 "A1.2": u"16,101★/1,459 forks，MIT，2026-09-29 当日推送、非 archived（API 实测） | 【红队】形态盲区-续跑r2 |",
 "A1.3": u"701★/59 forks，pushed 2026-09-29（API 实测） | 搜索-复检再扩展-r2 |",
 "A2.1": u"178.9k★/21.1k forks，当日推送（2026-09-29 实测）；文档技能非开源 | 搜索-GitHub技能合集-r1 |",
 "A2.2": u"抓取页面 271.5k★；skills.sh 总安装 4.3M（teach 725.5K）；活跃 | 搜索-新渠道深挖-r2 |",
 "A2.5": u"40.9k★/3.5k forks，77 open PR（2026-09-29 实测） | 搜索-厂商官方与海外平台-r1 |",
 "A3.1": u"镜像 star 18/10 提交；条目级汉化程度未逐条核实（如实） | 搜索-国内社区与内容场-r1 |",
 "A4.4": u"官方维护 npm @shopify/dev-mcp，免费 | 搜索-任务域-内容与经营-r1 |",
 "A4.5": u"【红队】形态盲区-续跑r2〔待归类：非 MCP 专属，同 OpenRouter 暂按网关语义就近放置，宜增设「模型网关」细类〕 |",
 "A4.6": u"引用前需渲染页面或读 repo README 确认 | 【红队】渠道盲区-续跑r2 + 搜索-邻接域-续跑r2（合并条目） |",
 "A5.1": u"搜索-同源深挖-续跑r2（经 open-webui 组织仓库列表发现，同源：Open WebUI 插件生态） |",
 "A5.2": u"【红队】形态盲区-续跑r2〔待归类：agent 前端框架，A5.2 现有细类以编排为主，暂就近放置〕 |",
 "A5.4": u"⚠️ AGPL-3.0 对商用集成有传染性约束 | 搜索-同源深挖-续跑r1 |",
 "A6.1": u"实测 684★，MIT，~2,815 commits，由 Generality Labs（UK AISI、Arcadia Impact、Vector Institute 参与）维护，活跃开发 | 搜索-同源深挖-续跑r2（经 UKGovernmentBEIS 组织仓库列表发现，同源：Inspect AI） |",
 "A6.3": u"训练代码尚未完全放出 | 搜索-同源深挖-续跑r2（经 xlang-ai 组织仓库列表发现，同源：OSWorld） |",
 "A6.5": u"实测 244★，MIT，1,316+ commits；有独立文档站/Slack/Docker 沙箱/防数据污染 canary GUID；pre-1.0（未见正式 release），DeepMind/Anthropic/MATS 等有使用痕迹 | 搜索-同源深挖-续跑r2（经 UKGovernmentBEIS 组织仓库列表发现，同源：Inspect AI） |",
 "A8.1": u"863 connectors 与 2,000+ 两处页面口径不同，如实并记 | 【红队】渠道盲区-续跑r2 + 搜索-邻接域-续跑r2（合并条目） |",
 "A8.4": u"页面在，首页约 24 个精选智能体；总量与用户数未公布（如实标注） | 【红队】渠道盲区-r1 |",
 "B1.2": u"~187.5k★/406 commits，MIT（2026-09-29 实测） | 搜索-任务域-办公文档-r1 |",
 "B2.1": u"8k★/298 commits，MIT；页面未显示最近提交，疑似更新放缓（如实） | 搜索-任务域-内容与经营-r1 |",
 "B2.2": u"8.5k★/118 commits，Apache-2.0；作者明示 iclightai.com 为假冒站（实测） | 搜索-任务域-内容与经营-r1 |",
 "B3.1": u"~27.6k★/498 commits，MIT，2026 年仍活跃；明确仅教育用途 | 搜索-新渠道深挖-r2 |",
 "B4.1": u"GitHub API 2026-09-29 实测：20,445★/2,239 forks，MIT，pushed 2026-09-28，独立官网 swe-agent.com，活跃维护 | 搜索-同源深挖-续跑r1 |",
 "B4.3": u"~139.3k★/2,087 commits，MIT，多语言 README，活跃 | 搜索-新渠道深挖-r2 |",
}

for sec, anchor in anchors.items():
    insert_after(anchor, R[sec])

# ---------- 4) 文件头说明行 ----------
insert_after(u"> 2026-09-29 续跑增补轮：红队续跑 r1/r2 共 57 条原始发现",
 [u"> 2026-09-30 合并轮：输入 75 条原始发现 → 同源合并 5 处 → 70 个本轮唯一资产，其中 30 条与既有目录重复（2026-09-29 续跑增补轮已录入目）按去重纪律跳过 → **净新增 40 条**入目（178→218）；【红队】标记 47→77；〔待归类〕/〔形态注记〕明细见文末 2026-09-30 合并轮核对。"])

# ---------- 5) 覆盖度矩阵：A6×内容案例 — → ●1，并加注记 ----------
replace_once(u"| A6 评测·基准·观测 | — | — | — | — | — | — | — | — | ●6 | ●5 | — | — | — | — |",
             u"| A6 评测·基准·观测 | — | — | — | — | — | — | — | — | ●6 | ●5 | — | — | — | ●1 |")
insert_after(u"> 2026-09-29 续跑增补注记：新增 46 条全部落入上表已 ● 的格",
 [u"> 2026-09-30 合并轮注记：新增 40 条亦全部落入上表已 ● 的格，唯 A6×内容案例原记「—」（语义不相干），本轮 Lakera Agent Breaker（在线交互靶场，A6.5）入目后该格改记 ●1；其余格内条数仍为增补前口径，待统一重算。"])

# ---------- 6) gaps #15 标注已填充 ----------
replace_once(u"15. **B4×MCP**：缺编码域 MCP——Context7 偏文档注入，PR-Agent 类审查能力可 MCP 化为服务。",
 u"15. **B4×MCP**：缺编码域 MCP——Context7 偏文档注入，PR-Agent 类审查能力可 MCP 化为服务。【2026-09-30 合并轮·已填充：github/github-mcp-server（A4.4，仓库/issue/PR 官方 MCP 工具面）补上编码/开发协作域 MCP 空缺；按 TAXONOMY §二.1 MCP 专属一律归 A4，故填充物落 A4.4 而非 B4 落格】")

# ---------- 7) 文末统计核对追加 ----------
stats = [
 u"",
 u"**2026-09-30 合并轮核对**（在 178 条口径之外的新增）：",
 u"",
 u"- 输入 75 条原始发现 → 同源合并 5 处（Salesforce AgentExchange ×3→1、npm registry ×3→1、阿里云百炼 MCP ×2→1）→ 70 个本轮唯一资产；其中 30 条经逐条比对确认为 2026-09-29 续跑增补轮已录入目（Agent Plugins Specification、AG-UI Protocol、Building effective agents、Cline Plugins 四源分发、AI Agents for Beginners、HF Agents Course、OpenRouter、LiteLLM、火山引擎 MCP 市场、OpenClaw、Open WebUI、OpenHands、claude-agent-sdk-python、LangGraph、Google ADK、CopilotKit、openai/codex、gemini-cli、browser-use、gorilla、xlam-function-calling-60k、SWE-bench、OSWorld、Inspect AI、LMArena、mcp-scan、AgentDojo、Garak、cursor.directory、Claude Marketplace），按去重纪律跳过 → **净新增 40 个唯一资产**，总数 178→218 ✓（主类目条数增补后：A1=23、A2=20、A3=12、A4=33、A5=46、A6=29、A7=4、A8=22、B1=5、B2=10、B3=8、B4=6）",
 u"- 合并明细：Salesforce AgentExchange（salesforce.com/agentforce/agentexchange 营销页 + agentexchange.salesforce.com 店面 + appexchange.salesforce.com 旧址，三合一）· npm registry（registry.npmjs.org 根 + npmjs.com/search 搜索页 + registry /-/v1/search API，三合一）· 阿里云百炼 MCP（docs.bailian.console.aliyun.com 文档 + help.aliyun.com/zh/model-studio/mcp 帮助页，二合一）",
 u"- 【红队】净新增 30 条（净新增 40 条中 30 条来源含【红队】），红队总标记 47→77",
 u"- 〔待归类〕注记 12 条：github/github-mcp-server（编码协作域任务 server，暂入 A4.4）、npm registry 与 @modelcontextprotocol/server-filesystem（非 MCP 专属包分发渠道，按 §二.1 严格应归 A8，暂入 A4.6）、aisuite（模型网关层，暂入 A4.5，与 OpenRouter/LiteLLM 同注）、verl 与 Uni-Agent（RL 训练框架，A5 无对应细类，暂入 A5.1）、OpenMAIC 与 MAIC-UI（教育教学任务域，B 段无主类目，暂入 B2.2）、WrenAI（数据分析/BI 任务域，暂入 B3.1）、Podcastfy（音频/播客生产，暂入 B2.1）、translation-agent（翻译/本地化任务域，暂入 B1.2）、Context Hub（编码 agent 上下文供给，暂入 A2.5）；〔形态注记〕5 条：Lakera Agent Breaker（在线交互靶场按内容案例落格，A6×内容案例矩阵格由「—」改 ●1）、SWE-Gym（训练环境+数据集暂按评测集落格）、SWE-Gym 数据集（数据集暂按评测集落格）、Cline Community Prompts（.clinerules 规则文件按 agent配置落格）、MAIC-Vibe（含 Claude Code skill 按 skill 落格）；另 Cherry Studio 为桌面客户端形态注记（暂入 A5.1）",
 u"- 机会点清单变动：gaps #15（B4×MCP 编码域 MCP）已填充——github/github-mcp-server；其余 14 条 gaps 本轮未填充，维持原状",
]
lines.extend([s + (u"\r\n" if u"\r\n" in "".join(lines[-3:]) else u"\n") for s in stats])

with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.writelines(lines)

after_rows = sum(1 for l in lines if l.startswith("| ["))
print("entry rows before/after:", before_rows, after_rows)
print("total lines after:", len(lines))
hong = sum(1 for l in lines if l.startswith("| [") and u"【红队】" in l.split(u"| 平台")[0][:0] + l)
print("rows containing 红队 marker (rough):", sum(1 for l in lines if l.startswith("| [") and u"【红队】" in l))
