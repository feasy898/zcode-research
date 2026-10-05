import os, re, json, io

ROOT = r"D:/workspace/zcode研究/skillfactory/library/doubao"
rows = json.load(io.open(os.path.join(ROOT, "_analysis", "catalog_rows.json"), encoding="utf-8"))
data = {r["dir"]: r for r in json.load(io.open(os.path.join(ROOT, "_analysis", "fm.json"), encoding="utf-8"))}

# per-name notable-pattern annotations (only for packages actually read this session)
NOTES = {
    "doubao-pdf": "极简 front-matter；Overview 一句话路由到 editing/forms/reference 三个分层文档；Rules 清单含工具优先级链与视觉复核闭环",
    "ppt": "『权威经验』编号 MUST 清单；场景路由表；references 按 style/cli/xml/workflow 四类分层；每步指明必读文档；xml_lint.py 静态校验 + 截图视觉校验双验收；MUST RELOAD SKILL 多轮重载规则",
    "sheet": "云/本地环境判定规则；『交付契约』硬性规定交付形态；Canvas 模式字段表；references 按触发条件表挂载；『未完——继续 offset 续读』长文分页标记",
    "word": "『skill 边界』正/反例清单 + 体裁默认载体表；attachment_purpose.md 附件证据台账表；用户目录优先于内置资产",
    "lark-base": "写任务 pending→written→verified 状态机；『写任务验收矩阵』(交付物×必读回×通过条件)；快速路由表含『何时读 reference』列；身份降级链 user→bot",
    "lark-doc": "skill 边界声明不处理 docx/PDF；genres/ 体裁分层参考；与 word 互为在线/本地对照",
    "doubao-academic-researcher": "IRON RULES 不可覆盖规则 + 冲突回应模板；workflow.py 脚本门卫（阶段准入/handoff JSON/BLOCKED:* 路由）；sub-skills/ 四阶段子技能 + REQUIRED READ MAP；6 维质量门禁",
    "doubao-medical-literature-search": "受众/响应双模式路由；『不可破坏的硬约束』清单；agents/doubao.yaml 声明 UI 展示名与默认 prompt；assets 放 PPT/Word/飞书模板",
    "doubao-medical-literature-monitoring": "agents/doubao.yaml 的 default_prompt 用多行块承载运行细节",
    "doubao-stock-screening": "config/tool-routing.json 工具路由配置化；playbooks/ 按任务类型分剧本；『禁止项』与『降级处理』专节",
    "doubao-contract-reviewer": "立场闸门（先定我方立场再审）；三层输出标准（必改风险/可争取优化/形式完善）；module-cards 按交易模块加载；预检脚本可选降级不中断",
    "doubao-newmedia-writing": "『DO NOT USE WHEN』负面触发清单；genre-guide + samples 两级参考；先建占位文档再写入的工作流",
    "byted-mediakit-video": "capability 工具清单总表（工具×说明×命令×参考链接）；跨域路由写进 description；依赖 shared 入口包（缺失即报错）；permissions+requires.bins+cliHelp 全套声明",
    "byted-mediakit-shared": "纯路由入口 skill：能力范围表→领域 skill 优先加载映射；capability_count 元数据",
    "browser-use-automation": "compatibility 字段声明运行环境依赖；安全信任边界与『强制用户接管』清单（登录/验证码/支付必须 interaction.request_action）；站点规则仅作业务参考",
    "computer-use-automation": "compatibility 字段声明 computer_use_tool 依赖（同类写法）",
    "skill-creator-for-work": "官方元技能：渐近披露三级模型与 <500 行上限、自由度分级（高/中/低）、禁建 README 等冗余文件、front-matter 仅 name+description 的规范声明",
    "doubao-enterprise-search": "单文件无 references（17k 字全部内联）；路由判断含『硬性排除』清单与默认倾向；多轮继承规则",
    "seedream-50": "接力型 skill：只做 Prompt 组装，交接给 doubao-creative-design 执行；模板化 T2I/I2I prompt 结构",
    "doubao-cron-scheduler": "单文件；锚定时间与歧义澄清规则；登录态检查清单与失败处理分支",
    "doubao-game-designer": "正文仅 363 字的『薄入口』：一段任务定义+一句『每次完整读取 references/workflow.md』，全部内容下沉 references/",
    "doubao-journal-format": "反模式样本：51k 字边界检查全内联单个 SKILL.md；复合请求硬停止（先问 A/B 再动）；`Version` 大写 V 非规范字段",
    "doubao-wealth-planning": "『线上最高优先级规则：输出硬模板』置顶覆盖后文；evals/evals.json 结构化断言（route_to/must_include/must_not_include/数字须带内联来源）；config/schemas/tests 全套工程化",
    "doubao-ultimate-guide": "branches/ 每分支独立子目录；『总控先创建文档，分支只写内容』跨分支一致性规则；六类边界路由（不明/缺信息/不适用/多意图/冲突/强时效）",
    "verifier-hub": "compatibility 环境声明 + Windows 入口差异提示；『58 个子命令』式能力概括写入 description；JSON 输出含可引用 evidence 字段",
    "artifact-preview": "description 内嵌中英触发短语列表（『视觉自检』『preview pptx』等）；兼容性降级策略（缺依赖警告不崩溃）",
    "doubao-marketing-material-review": "metadata.author 团队署名 + metadata.version 双字段写法",
    "doubao-medical-report": "metadata.short-description 短描述字段（UI 二级展示）",
    "doubao-dpa-drafter": "metadata.dependency/python 字段（解析为空的声明残留）",
    "lark-attendance": "单句 description 的最小 lark 包（触发面窄是风险）",
    "lark-whiteboard": "description 末尾『不负责：…』负面边界句式",
    "lark-base（模板中心）": "",
}

def note_for(row):
    n = row["name"]
    if n in NOTES and NOTES[n]:
        return NOTES[n]
    f = row["feat"]
    if f and f != "极简(仅name+description)":
        return f
    return "—"

def first_sentence(desc, maxlen=110):
    if not desc:
        return "—"
    s = re.split(r"(?:。|！|；)", desc)[0]
    if len(s) > maxlen:
        s = s[:maxlen] + "…"
    return s

cats = {}
for r in rows:
    cats.setdefault(r["cat"], []).append(r)

order = ["文档办公","飞书协同","学术科研","医疗健康","金融投研","法律合规","电商跨境","内容创作","营销增长","媒体生成","浏览器/系统操作","平台工具","其他"]

L = []
L.append("# 豆包（Doubao）官方 Skill 包全量盘点目录")
L.append("")
L.append("> 来源：`D:/AI软件们/DoubaoWork/app/task-mode-resource/runtime-bundle/packages/` 下 106 个 `skill-*.zip`（另有 1 个 `base-*.zip` 为 Node 运行时、3 个 `dlc-*.zip` 为 lark-cli 等二进制依赖，均非 skill，未纳入本目录）。")
L.append("> 全部已解压至 `skillfactory/library/doubao/skill-<hash>/`，每个目录根下均有 SKILL.md（已逐个验证：106/106）。")
L.append("> 本目录为内部研究用途；表中『一句话能力』为对官方 description 首句的压缩转述，非原文整段复制。")
L.append("")
L.append("## 总览统计（实测）")
L.append("")
L.append("| 维度 | 实测值 |")
L.append("|---|---|")
L.append("| 包数量 | 106 |")
L.append("| front-matter 必备字段 | name 106/106，description 106/106 |")
L.append("| version 字段 | 24/106（另有 4 个把 version 放进 metadata） |")
L.append("| license 字段 | 9/106 |")
L.append("| permissions 字段 | 5/106（值全部为 `shell`，均属 byted-mediakit 系列） |")
L.append("| metadata 字段 | 30/106（子键：requires.bins 25、cliHelp 22、product/domain/capability_count 5、version 4、hub 2 等） |")
L.append("| compatibility 字段 | 3/106 |")
L.append("| description 长度 | 最短 20 字，中位数 182 字，最长 976 字；>500 字 8 个 |")
L.append("| SKILL.md 正文字数 | 最短 363 字，中位数约 7,185 字，最长 51,056 字（journal-format）；>2 万字 9 个 |")
L.append("| 目录形态 | references/（或 reference/）分层 89 包；scripts/ 42 包；assets/ 19 包；agents/（UI 元数据 yaml）20 包；evals/ 5 包；仅含 SKILL.md 的单文件包 11 个 |")
L.append("| agents/ 元数据 | agents/openai.yaml 13 个、agents/doubao.yaml 7 个，schema 均为 interface.{display_name, short_description, default_prompt} |")
L.append("| 内嵌 .git | 3 个包带完整 .git（如 doubao-game-designer、doubao-wealth-planning） |")
L.append("")
L.append("---")
L.append("")

total = 0
for cat in order:
    items = sorted(cats.get(cat, []), key=lambda x: x["name"])
    if not items:
        continue
    total += len(items)
    L.append(f"## {cat}（{len(items)}）")
    L.append("")
    L.append("| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |")
    L.append("|---|---|---|---|---|")
    for r in items:
        name_cell = f'**{r["name"]}**<br>`{r["dir"]}`'
        L.append(f'| {name_cell} | {r["ver"]} | {first_sentence(r["desc"])} | {r["struct"]}（{r["files"]} 文件） | {note_for(r)} |')
    L.append("")

assert total == 106, total
L.append("---")
L.append("")
L.append("## 类别说明与归类口径")
L.append("")
L.append("- **文档办公**：word / ppt / sheet / html / doubao-pdf / artifact-preview——本地与在线文档的创建编辑渲染。ppt/sheet 实际操作飞书在线件，归此类因其交付物是演示文稿/表格。")
L.append("- **飞书协同**：lark-* 17 个——飞书开放能力（Base/Docx/IM/Mail/Drive/Calendar/OKR/Task/Wiki/白板/会议/审批/考勤/通讯录/Markdown/meeting/workflow-standup-report/openapi-explorer）。")
L.append("- **学术科研**：调研/润色/评测/精读/期刊排版/开题/参考文献审计/批判性阅读。")
L.append("- **医疗健康**：文献检索/监控/解读/翻译、临床决策、体检报告、循证问答——医疗细分场景全家桶。")
L.append("- **金融投研**：个股筛选/财报分析/行业分析/一级二级公司研究/财务建模/财富规划/每日行情/多股对比。")
L.append("- **法律合规**：合同审查/起草/修订、DPA 起草、专利起草、合规评估、个人信息审计、营销材料审查。")
L.append("- **电商跨境**：选品/商品内容/商品问答/Listing 本地化/客服/电商提案/情感追踪/跨境电商合规税务物流；product-analysis / product-manager / product-qa 三个产品经理向 skill 因命名命中 product- 前缀归入此类。")
L.append("- **内容创作**：小说/图书/新媒体/多平台改写/创意设计/创意短剧/创意视频/头条日历/跨境增长内容。")
L.append("- **营销增长**：市场热点/营销策划/巨量引擎投放/公告解读。")
L.append("- **媒体生成**：mediakit 五件套（shared+audio/editing/image/video）+ seedream-50 / seedance-25 / seed-audio / doubao-video-extract。")
L.append("- **浏览器/系统操作**：browser-record-replay / browser-use-automation / computer-use-automation。")
L.append("- **平台工具**：app-builder / cron-scheduler / enterprise-search / identity / record / skill-creator-for-work / verifier-hub / pc-optimizer。")
L.append("- **其他**：doubao-data-analysis（业务数据分析）、doubao-visualization（图表图解）、doubao-game-designer（游戏策划）、doubao-questionnaire-designer（问卷调研）、doubao-human-signal（去 AI 味）、doubao-ultimate-guide（四合一攻略总控）、gift-card-redemption 与 student-discount-application（豆包平台运营件）。")
L.append("")
L.append("## 三代包风格（按 front-matter 丰富度分层）")
L.append("")
L.append("1. **极简代**（doubao-* 大多数，约 70 包）：front-matter 只有 `name` + `description`，全靠 description 触发，正文承载全部规范。")
L.append("2. **飞书 CLI 代**（lark-*、ppt/sheet）：加 `version` + `metadata.{requires.bins, cliHelp}`，宿主用 bins 探测 lark-cli 可用性、用 cliHelp 拉取命令帮助。")
L.append("3. **工程化代**（byted-mediakit-*、verifier-hub/artifact-preview、wealth-planning 等）：补齐 `license` / `permissions` / `compatibility` / `metadata.{product,domain,capability_count,hub}`，并配 evals/tests/schemas/config，接近可独立测试的软件包。")
L.append("")
L.append(f"> 生成时间：2026-09-29；生成脚本：`_analysis/parse_fm.py` + `_analysis/build_catalog.py` + `_analysis/gen_catalog_md.py`；原始解析数据：`_analysis/fm.json`、`_analysis/catalog_rows.json`。")

io.open(os.path.join(ROOT, "CATALOG.md"), "w", encoding="utf-8").write("\n".join(L))
print("CATALOG.md written,", len(L), "lines")
