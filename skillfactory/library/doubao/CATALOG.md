# 豆包（Doubao）官方 Skill 包全量盘点目录

> 来源：`D:/AI软件们/DoubaoWork/app/task-mode-resource/runtime-bundle/packages/` 下 106 个 `skill-*.zip`（另有 1 个 `base-*.zip` 为 Node 运行时、3 个 `dlc-*.zip` 为 lark-cli 等二进制依赖，均非 skill，未纳入本目录）。
> 全部已解压至 `skillfactory/library/doubao/skill-<hash>/`，每个目录根下均有 SKILL.md（已逐个验证：106/106）。
> 本目录为内部研究用途；表中『一句话能力』为对官方 description 首句的压缩转述，非原文整段复制。

## 总览统计（实测）

| 维度 | 实测值 |
|---|---|
| 包数量 | 106 |
| front-matter 必备字段 | name 106/106，description 106/106 |
| version 字段 | 24/106（另有 4 个把 version 放进 metadata） |
| license 字段 | 9/106 |
| permissions 字段 | 5/106（值全部为 `shell`，均属 byted-mediakit 系列） |
| metadata 字段 | 30/106（子键：requires.bins 25、cliHelp 22、product/domain/capability_count 5、version 4、hub 2 等） |
| compatibility 字段 | 3/106 |
| description 长度 | 最短 20 字，中位数 182 字，最长 976 字；>500 字 8 个 |
| SKILL.md 正文字数 | 最短 363 字，中位数约 7,185 字，最长 51,056 字（journal-format）；>2 万字 9 个 |
| 目录形态 | references/（或 reference/）分层 89 包；scripts/ 42 包；assets/ 19 包；agents/（UI 元数据 yaml）20 包；evals/ 5 包；仅含 SKILL.md 的单文件包 11 个 |
| agents/ 元数据 | agents/openai.yaml 13 个、agents/doubao.yaml 7 个，schema 均为 interface.{display_name, short_description, default_prompt} |
| 内嵌 .git | 3 个包带完整 .git（如 doubao-game-designer、doubao-wealth-planning） |

---

## 文档办公（6）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **artifact-preview**<br>`skill-cb8086694dfbc1ce1c21fab63fcc1b3b` | 2.1 | Render workspace artifacts (pdf/pptx/docx/xlsx/html/png/jpg/txt/zip) into text + page screenshots + thumbnail … | 仅SKILL.md+散文件（30 文件） | description 内嵌中英触发短语列表（『视觉自检』『preview pptx』等）；兼容性降级策略（缺依赖警告不崩溃） |
| **doubao-pdf**<br>`skill-afc0aaec9a5ef56bbcb128e81327f28d` | — | 用于处理所有 PDF 相关任务，包括读取、创建、编辑、转换、内容提取、页面处理、表单填写和扫描件解析 | scripts/（15 文件） | 极简 front-matter；Overview 一句话路由到 editing/forms/reference 三个分层文档；Rules 清单含工具优先级链与视觉复核闭环 |
| **html**<br>`skill-a5bed54ddd046e91809433ca10be30f8` | — | 专门设计、生成和修改可直接在浏览器中打开的 HTML 页面或已发布的 Miaoda 妙搭链接 | references/+scripts/（9 文件） | 极简 front-matter，触发全靠 description |
| **ppt**<br>`skill-3f345a337e8b5d02f0ab7506dcdffbfa` | 1.0.13 | 飞书幻灯片：创建和编辑幻灯片 | references/+scripts/（68 文件） | 『权威经验』编号 MUST 清单；场景路由表；references 按 style/cli/xml/workflow 四类分层；每步指明必读文档；xml_lint.py 静态校验 + 截图视觉校验双验收；MUST RELOAD SKILL 多轮重载规则 |
| **sheet**<br>`skill-62a51cd03807846890e25c40aa92b12b` | 3.2.3 | 表格全场景（本地 Excel/CSV 与飞书/doubao 在线表格）：创建、读写、分析、计算、建模、语义处理、可视化与美化 | references/+scripts/（44 文件） | 云/本地环境判定规则；『交付契约』硬性规定交付形态；Canvas 模式字段表；references 按触发条件表挂载；『未完——继续 offset 续读』长文分页标记 |
| **word**<br>`skill-2b5409855c605c9770f4e1e8c9d6283b` | 1.0.30 | Office Word 的阅读、新建和修改使用此技能 | references/+assets/（18 文件） | 『skill 边界』正/反例清单 + 体裁默认载体表；attachment_purpose.md 附件证据台账表；用户目录优先于内置资产 |

## 飞书协同（17）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **lark-approval**<br>`skill-fe93caa28ec4b12b70c665f26c888b30` | 1.2.0 | 飞书审批：查询和处理审批待办/已办/实例，搜索可发起审批定义、查看定义详情并发起原生审批实例 | references/（17 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-attendance**<br>`skill-598ff636a0e64e2b4ce5a6103cb7257f` | 1.0.0 | 飞书考勤打卡：查询自己的考勤打卡记录 | 单文件(仅SKILL.md)（1 文件） | 单句 description 的最小 lark 包（触发面窄是风险） |
| **lark-base**<br>`skill-30ee3da3189d08ee2d8aeebd1841ef26` | 1.4.1 | 多维表格：可视化表格数据库与业务系统，可搭建台账/进度/项目/订单/客户/排班等业务场景，具备多表联动、多视图看板、表单问卷收集、仪表盘、自动化工作流、表格行列权限，支撑持续运营业务闭环 | references/（32 文件） | 写任务 pending→written→verified 状态机；『写任务验收矩阵』(交付物×必读回×通过条件)；快速路由表含『何时读 reference』列；身份降级链 user→bot |
| **lark-calendar**<br>`skill-d7376f2aa4b12b5b1f01fbd70ba002c0` | 1.0.0 | 飞书日历：管理日历日程和会议室 | references/（15 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-contact**<br>`skill-103b964ea088e98cea458120aeacf440` | 1.0.0 | 飞书 / Lark 通讯录:按姓名 / 邮箱解析成 open_id,或按 open_id 反查姓名 / 部门 / 邮箱 / 联系方式 / 个人状态 / 签名,以及按关键词搜索当前用户可见的机器人 / 智能体(agent) | references/（4 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-doc**<br>`skill-94b0a64ab313c0c444497d9623686270` | — | 飞书/豆包在线文档（`/docx`、`/wiki`）的阅读、新建和修改以及操作思维笔记，使用此技能 | references/（23 文件） | skill 边界声明不处理 docx/PDF；genres/ 体裁分层参考；与 word 互为在线/本地对照 |
| **lark-drive**<br>`skill-899adabe25b5689a827ef75527f93ddf` | 1.0.0 | 飞书云空间（云盘/云存储）：管理 Drive 文件和文件夹，包含上传/下载、创建文件夹、复制/移动/删除、查看元数据、查询权限设置、评论/权限/订阅、标题、版本、飞书文档密级标签（secure labels）和本地文件导… | references/（63 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-im**<br>`skill-4129cdacab6f5fbf1179d10c638e92b4` | 1.0.0 | 飞书即时通讯：收发消息和管理群聊 | references/（59 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-mail**<br>`skill-63e907b2558fef94bd38ebc95050dcda` | 1.0.0 | 飞书邮箱：Use when user mentions 起草邮件、写邮件、草稿、发送/回复/转发邮件、查阅邮件、看邮件、搜索邮件、邮件文件夹、邮件标签、邮件联系人、监听新邮件、邮件收信规则等 | references/+assets/（35 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-markdown**<br>`skill-1a848ac0ba3254e2602da14a49a428cb` | 1.2.2 | 飞书 Markdown：查看、创建、上传、编辑和比较飞书中的原生 Markdown 文件 | references/（6 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-meeting**<br>`skill-1ea9978c6b74cd24b1ec7c29cf9b1c0a` | 1.0.0 | 飞书视频会议：查询会议记录与会议产物(纪要/逐字稿/妙记)、妙记搜索/上传/下载/编辑 | references/+scenes/（25 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-okr**<br>`skill-4b22c55ae5d62070bc8edf5f11259b37` | 1.0.0 | 飞书 OKR：管理目标与关键结果 | references/（26 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-openapi-explorer**<br>`skill-6444f4f0d82f17f94bb63ef2d60c60e0` | 1.0.0 | 飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口 | 单文件(仅SKILL.md)（1 文件） | requires.bins 依赖声明；version 字段（front-matter 完整度中上） |
| **lark-task**<br>`skill-41594a8e6b61916402fb2a71dbcc4d47` | 1.0.0 | 飞书任务：管理任务、清单和任务智能体 | references/（18 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-whiteboard**<br>`skill-6532bef9d4f6ff96872e448dc897c6e1` | 1.0.0 | 飞书画板：查询和编辑飞书云文档中的画板 | references/+scenes/（31 文件） | description 末尾『不负责：…』负面边界句式 |
| **lark-wiki**<br>`skill-7e207611f542ee906ad35d802161fdf9` | 1.0.3 | 飞书知识库：管理知识空间、空间成员和文档节点 | references/（14 文件） | requires.bins 依赖声明；cliHelp 探测命令；version 字段（front-matter 完整度中上） |
| **lark-workflow-standup-report**<br>`skill-5e21a971df08e058363a00000041db66` | 1.0.0 | 日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要 | 单文件(仅SKILL.md)（1 文件） | requires.bins 依赖声明；version 字段（front-matter 完整度中上） |

## 学术科研（8）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-academic-evaluator**<br>`skill-cfd0abd2a96a07786a5de1961a418b32` | — | 用资深审稿人和导师的眼光，对科研工作做"只看不改"的诊断 | references/+sub-skills/（8 文件） | 极简 front-matter，触发全靠 description |
| **doubao-academic-polish**<br>`skill-ca6f46167a165dd50d214b44ddecd4f2` | — | 学术论文正文写作、结构设计与语言润色总入口 | 仅SKILL.md+散文件（53 文件） | 极简 front-matter，触发全靠 description |
| **doubao-academic-researcher**<br>`skill-9d7a8684b608a41d194e178d6d8ab077` | — | 通用学术文献调研Skill，面向研究者、学生和论文写作者在未锁定具体论文题目前摸清某学术方向、概念、机制、热点前沿、学术史或选题依据 | references/+scripts/+sub-skills/（21 文件） | IRON RULES 不可覆盖规则 + 冲突回应模板；workflow.py 脚本门卫（阶段准入/handoff JSON/BLOCKED:* 路由）；sub-skills/ 四阶段子技能 + REQUIRED READ MAP；6 维质量门禁 |
| **doubao-critical-reading-companion**<br>`skill-6f9064259f49979f1c5e6eabcbf1c669` | — | 深度解读文章，把新闻、长评或宣传文案等非学术公共文本转成便于理解、可追溯的阅读地图 | reference/（5 文件） | 极简 front-matter，触发全靠 description |
| **doubao-journal-format**<br>`skill-090298bb3a1ba839794595149b780353` | — | 用于对学术论文类 Word/DOCX 文档进行期刊、学校、会议或课程要求的格式排版与修复 | references/+scripts/+assets/（14 文件） | 反模式样本：51k 字边界检查全内联单个 SKILL.md；复合请求硬停止（先问 A/B 再动）；`Version` 大写 V 非规范字段 |
| **doubao-paper-close-reading**<br>`skill-63302ad8e81cc2bf56db8a2fb5436721` | — | 用于用户提供一篇或少量学术论文后，进行专业深度精读，讲清研究问题、研究故事、方法或理论机制、关键证据、实验结果、可信边界、复现风险与研究启示，并生成高级 Markdown 报告和飞书文档 | assets/（2 文件） | 极简 front-matter，触发全靠 description |
| **doubao-reference-audit**<br>`skill-07df3d5a79c9ae195240b95a5034276f` | — | 用于用户提交论文、学位论文或参考文献清单后，系统审查参考文献真实性、题录准确性、文内—文后对应关系以及正文主张是否得到被引文献支持，并生成专业、清晰、可直接指导修改的论文引用审计报告与飞书文档 | scripts/+assets/（3 文件） | 极简 front-matter，触发全靠 description |
| **doubao-research-proposal**<br>`skill-f7ebd5ce4aa1315792405b40fe4bed08` | — | 用于国自然、国社科等基金申请、开题报告、博士后/人才计划、研究计划书等学术提案的撰写、审查和优化 | references/+assets/（14 文件） | 极简 front-matter，触发全靠 description |

## 医疗健康（7）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-answer-with-medical-evidence**<br>`skill-3e946c0a93287fcff4826260cc67b00a` | — | 健康问题循证咨询，患者或家属提出健康或医学问题时使用，患者提问优先使用本技能，适用于需要围绕相关症状、疾病、检查、用药、治疗或预后问题，结合医学文献进行回答的场景 | references/+scripts/+agents/+assets/（11 文件） | 极简 front-matter，触发全靠 description |
| **doubao-clinical-decision-support**<br>`skill-3fad7dcc0a472ace40fd35612c64ed65` | — | 循证医学临床辅助决策 Skill | references/+scripts/+agents/+assets/（17 文件） | 极简 front-matter，触发全靠 description |
| **doubao-medical-literature-interpretation**<br>`skill-26dc082893cc118843a179cffbf7b7de` | — | 医学文献解读 Skill | references/+scripts/+agents/+assets/（8 文件） | 极简 front-matter，触发全靠 description |
| **doubao-medical-literature-monitoring**<br>`skill-0459b763842d9e1950595ec96f4d7b8e` | — | 医学进展跟踪 Skill | references/+scripts/+agents/+assets/（9 文件） | agents/doubao.yaml 的 default_prompt 用多行块承载运行细节 |
| **doubao-medical-literature-search**<br>`skill-23a5327f5651218c72d3c2c94e53989c` | — | 医学文献检索分析 Skill | references/+scripts/+agents/+assets/（17 文件） | 受众/响应双模式路由；『不可破坏的硬约束』清单；agents/doubao.yaml 声明 UI 展示名与默认 prompt；assets 放 PPT/Word/飞书模板 |
| **doubao-medical-literature-translation**<br>`skill-4d6d8ca4f1cea673ad65c493c87f34f0` | — | 医学文献翻译 Skill，面向医学领域文献资料翻译 | references/+scripts/+agents/+assets/（11 文件） | 极简 front-matter，触发全靠 description |
| **doubao-medical-report**<br>`skill-8d2103eae0d346132e2bc3fb490e9179` | — | 必须在用户需要医学报告解读时使用 | references/+scripts/+agents/+assets/（17 文件） | metadata.short-description 短描述字段（UI 二级展示） |

## 金融投研（9）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-daily-stock**<br>`skill-e0704b9983124d9890a724cb2147914d` | — | 用于单一上市股票的个股日报，解释涨跌和异动原因，梳理行情、资金流、新闻公告、板块联动、技术面、预期与风险 | references/+agents/（9 文件） | 极简 front-matter，触发全靠 description |
| **doubao-earnings-analysis**<br>`skill-c226a9fcc54de98ccc92aac20f4fb767` | — | 上市公司财报/季报/年报/业绩的深度因果分析，覆盖A股、港股、美股和中概股 | references/+scripts/（23 文件） | 极简 front-matter，触发全靠 description |
| **doubao-finance-model-builder**<br>`skill-dd857e42d797c0b098e726e0fa0305f1` | — | 对 A 股、港股和美股上市公司执行中文、可审计且带机器阻断质量门的三表预测、DCF、LBO或可比公司估值 | references/+scripts/+assets/（116 文件） | 极简 front-matter，触发全靠 description |
| **doubao-industry-analysis**<br>`skill-6fde60d522a3b8cac4029e33e8272e7a` | — | 针对某一行业（半导体、新能源、医药、消费等）的中长期基本面与产业研究，覆盖行业定义与规模、产业链与竞争格局、政策与驱动力、景气周期、趋势研判与三情景、盈利质量与落地建议 | references/+scripts/+agents/（15 文件） | 极简 front-matter，触发全靠 description |
| **doubao-private-company**<br>`skill-bc261fdc23e8573a1e4f548da63201fa` | — | 评估一级市场、私募股权或创业项目的初步投资价值，基于BP、Deck、财务和访谈资料输出Screening Report、投资逻辑、红旗、情景、尽调缺口和初步建议 | references/+scripts/+schemas/+evals/+tests/+config/（163 文件） | 极简 front-matter，触发全靠 description |
| **doubao-public-company-analysis**<br>`skill-666edb3a9c400301e2a400f9c5a3ac99` | — | 分析上市公司的商业模式、竞争优势、行业位置、财务质量、估值、风险与投资观点 | references/+scripts/+schemas/+evals/+tests/+config/（64 文件） | 极简 front-matter，触发全靠 description |
| **doubao-stock-screening**<br>`skill-da884df46a60f716b761504cc2dd0cac` | — | 用于 A 股、港股、美股及其他股票市场的股票筛选、候选股构建、指定股票比较、行业筛选、主题概念筛选、产业链环节筛选、策略风格筛选和龙头识别 | references/+config/+templates/+playbooks/（49 文件） | config/tool-routing.json 工具路由配置化；playbooks/ 按任务类型分剧本；『禁止项』与『降级处理』专节 |
| **doubao-wealth-planning**<br>`skill-5e84a530ca1db13e950dbc89ee470800` | — | 为个人或家庭构建目标导向的财富规划，覆盖现金流、应急资金、债务、保障、教育/养老等目标、资产配置、情景压力测试与行动清单 | references/+scripts/+schemas/+evals/+tests/+config/（166 文件） | 『线上最高优先级规则：输出硬模板』置顶覆盖后文；evals/evals.json 结构化断言（route_to/must_include/must_not_include/数字须带内联来源）；config/schemas/tests 全套工程化 |
| **multi-stock-comparison**<br>`skill-07a5e2600eac11236f7f267cb4a74724` | — | 对两家及以上上市公司或股票进行横向研究，覆盖大盘与板块、外围市场、供应链、重要新闻与监管、商业模式、经营财务、成长、预期、估值、股价、组合以及 A/H 股与跨上市地相对价值 | references/+scripts/（29 文件） | 极简 front-matter，触发全靠 description |

## 法律合规（9）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-compliance-assessment-public**<br>`skill-cb1e094de2695ac6f6d0a00ace83d8e9` | — | 基于公开法律来源开展交互式合规评估并生成可审阅报告 | references/+scripts/+assets/（28 文件） | 极简 front-matter，触发全靠 description |
| **doubao-contract-amendment**<br>`skill-2ed73725a90baacdd4d31f2aa76e3eb0` | — | 用于在已签原协议基础上，依据用户提供的新情况起草补充协议、变更协议或终止协议 | references/（2 文件） | 极简 front-matter，触发全靠 description |
| **doubao-contract-drafting**<br>`skill-5df9d24d9188ca654bb093d4caecd5ad` | — | 直接起草中国大陆商业合同并生成无批注、无颜色、中文字体正确的可编辑 Word 文件 | references/+scripts/（24 文件） | 极简 front-matter，触发全靠 description |
| **doubao-contract-reviewer**<br>`skill-c7fdfe955913a17baea1a8b6753a5b1a` | — | doubao-contract-reviewer 是面向大众用户的合同审查 Skill，适合在豆包/豆包 Turbo 中审查各类合同 | references/+scripts/（4 文件） | 立场闸门（先定我方立场再审）；三层输出标准（必改风险/可争取优化/形式完善）；module-cards 按交易模块加载；预检脚本可选降级不中断 |
| **doubao-dpa-drafter**<br>`skill-e3aa922fc5bafa4b46649679d1798705` | — | DPA数据处理协议专业起草 | references/+scripts/（15 文件） | metadata.dependency/python 字段（解析为空的声明残留） |
| **doubao-ecommerce-compliance-tax-logistics**<br>`skill-8a5998abc95675999ebb81867911a594` | — | Cross-border ecommerce compliance, tax, IP, customs, tariff, HS code, fulfillment, warehousing, China import, … | references/（12 文件） | 极简 front-matter，触发全靠 description |
| **doubao-marketing-material-review**<br>`skill-249166944c13372c77061e4d69aade6f` | 1.0 | 营销素材审核 | 单文件(仅SKILL.md)（1 文件） | metadata.author 团队署名 + metadata.version 双字段写法 |
| **doubao-patent-drafting**<br>`skill-9266bd10fe61547449fec1e6e76b7db0` | — | 用户要求基于技术交底书撰写或修改中国发明、实用新型专利申请文件，或者审查已有权利要求书时使用 | references/+scripts/+sub-skills/（7 文件） | 极简 front-matter，触发全靠 description |
| **doubao-personal-info-audit**<br>`skill-ee68dae572e30ba038330591455a9f6e` | — | 开展中国个人信息保护合规审计、审计触发判断、证据登记与证明力评价、事实和不确定性分析、数据分类、处理活动盘点、法律角色和处理情形识别、适用规则检索、上下位法与配套规范衔接、26模块107子项评价、风险与整改设计，并生成可… | references/+scripts/+assets/（69 文件） | 极简 front-matter，触发全靠 description |

## 电商跨境（9）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-customer-service**<br>`skill-861469de16bdbd1b5f294695995fd38e` | — | 生成电商在线文字客服的可执行处理方案和正式交付文档 | references/+templates/（17 文件） | 极简 front-matter，触发全靠 description |
| **doubao-ecommerce-proposal**<br>`skill-907b9d0c4581ab64db3282833b2e31ff` | — | 电商活动策划专家 | references/（5 文件） | 极简 front-matter，触发全靠 description |
| **doubao-listing-localization**<br>`skill-0a25baf0b6e176840bf4b25490d8b9d1` | — | Cross-border ecommerce Listing and Product Optimization for Amazon, TEMU, Walmart Marketplace, TikTok Shop, Sh… | references/（10 文件） | 极简 front-matter，触发全靠 description |
| **doubao-product-analysis**<br>`skill-098d38f5a3f43cdf1676e4ce301cf06d` | — | 围绕具体产品、产品想法或存量方案，产出用于产品进入、定位、竞争策略、上市路径、能力建设与路线图决策的证据型分析报告 | references/+assets/（7 文件） | 极简 front-matter，触发全靠 description |
| **doubao-product-content**<br>`skill-a7eb0a21e88e2b2c761bb6194d5ce7a9` | — | 生成或优化电商商品标题、详情文案和商品页静态图片 | references/+scripts/+agents/（21 文件） | 极简 front-matter，触发全靠 description |
| **doubao-product-manager**<br>`skill-1a1963e906d5c401c51c026f529f86dd` | — | 将产品想法、用户反馈、研究数据、云文档、附件和已有方案转化为有依据的产品判断、策略、MVP、优先级、Roadmap、PRD、用户故事、验收标准或方案评审 | references/+scripts/（15 文件） | 极简 front-matter，触发全靠 description |
| **doubao-product-qa**<br>`skill-07c702753395022576e1e78ccc1fd5c1` | — | 将 PRD、原型、网页、接口、代码、测试记录和多轮上下文转成可追踪的 QA 基线、风险用例、执行证据、Bug 与发布判断 | references/+scripts/+agents/+assets/+tests/（102 文件） | 极简 front-matter，触发全靠 description |
| **doubao-product-selection**<br>`skill-aa4b5b6425df400ee9f75407ba20c714` | — | 电商选品与品类机会分析技能 | 单文件(仅SKILL.md)（1 文件） | 极简 front-matter，触发全靠 description |
| **doubao-sentiment-tracker**<br>`skill-aceb00b7207087342325d6fcc46a7981` | — | 当用户在网页端或电脑客户端需要进行舆情监控、调研、社交媒体反馈收集、用户评价、品牌声量追踪时使用 | references/+agents/（6 文件） | 极简 front-matter，触发全靠 description |

## 内容创作（9）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-book-writer**<br>`skill-fd8723aef8a54dd5ff41811997d89e16` | — | 豆包办公里的非虚构长文档工作台 | references/+scripts/+sub-skills/（72 文件） | 极简 front-matter，触发全靠 description |
| **doubao-creative-design**<br>`skill-739c4782187e0e1c53d0c38abc66703f` | — | 当用户要求从零生成、设计商业/社交媒体创意图片，或做系列延展、多比例适配时使用 | references/（18 文件） | 极简 front-matter，触发全靠 description |
| **doubao-creative-drama**<br>`skill-791fc7025b35309f09b931d8a2e51d97` | — | 当用户提出短篇短剧、动画短片、微电影、剧情视频、AI视频、影视化短片、动态漫、宣传片、预告片等**单集 5-10 分钟以内**的短篇制作需求，或包含"做个短剧"、"拍个微电影"、"弄个动画短片"、"写个短剧剧本"、"画个… | references/（6 文件） | 极简 front-matter，触发全靠 description |
| **doubao-creative-video**<br>`skill-531e521f8e77b486f55706be2602b7fe` | — | 当用户需要通用视频生成、视频创作、视频提示词规划或文生/图生视频时使用，包括创意视频、产品广告、商品广告、UGC口播/带货/信息流视频、marketing/TVC风格广告、企业宣传片、商务视频、品牌形象片、产品功能介绍、… | references/（4 文件） | 极简 front-matter，触发全靠 description |
| **doubao-cross-border-growth-content**<br>`skill-6ef23dc79d3f0e1a39b7e42f7e12cdaf` | — | Evidence-grounded cross-border ecommerce content operations for short-video and livestream scripts, UGC or cre… | references/+scripts/（16 文件） | 极简 front-matter，触发全靠 description |
| **doubao-headlines-calendar**<br>`skill-eaf5c493536763f20f60b9fa54a3a7f2` | — | 跨平台内容生成、改写、评估和A/B测试标题，并结合账号定位、受众、产能和节点规划可执行的周度或月度内容选题日历 | references/+scripts/（8 文件） | 极简 front-matter，触发全靠 description |
| **doubao-multiplatform-rewrite**<br>`skill-13fc4695615ef076c2e46ac0b2fc718d` | — | 基于用户提供的已有素材（母稿、文章、新闻稿、活动稿、产品稿、报告摘要、访谈素材、口播稿、散乱素材等），改写成可发布的多平台分发版本，标准场景为≥2个平台，有素材的单平台改写也可支持，覆盖微信公众号、短视频脚本、微博等平台 | references/（12 文件） | 极简 front-matter，触发全靠 description |
| **doubao-newmedia-writing**<br>`skill-f2a8c68464b3c1f80b1e8b0316fa168b` | — | 用于生成、改写、优化并默认以飞书文档/Lark Doc 交付中文新媒体内容，覆盖小红书图文笔记、微信公众号文章、3 分钟以内短视频分镜脚本，以及上述类型的复合创作方案 | references/（23 文件） | 『DO NOT USE WHEN』负面触发清单；genre-guide + samples 两级参考；先建占位文档再写入的工作流 |
| **doubao-novel-writing**<br>`skill-9a6d62c1a3fcd6ff54318a79cffa0dd5` | — | 用于网文小说创作、改写、续写、诊断、卖点包装、市场调查和编辑视角分析 | references/+scripts/+evals/（10 文件） | 极简 front-matter，触发全靠 description |

## 营销增长（4）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-announcement-analysis**<br>`skill-f3f247c3161b9ff60d89e8464df2af39` | — | 搜索并解读上市公司公告，覆盖 A股（沪深北）、港股（HKEX）、美股（SEC EDGAR）三大市场 | references/+scripts/（27 文件） | 极简 front-matter，触发全靠 description |
| **doubao-market-hotspot**<br>`skill-6143212a80dafddf3a9c5dba1840e64b` | — | 把宏观、政策、监管、供需、地缘、行业或公司事件转化为公司、行业与公开市场的因果影响分析，覆盖事件状态、基线、传导渠道、财务与估值影响、直接及高阶影响、priced-in判断、情景、监控与证伪 | references/+scripts/+schemas/+evals/+tests/+config/（63 文件） | 极简 front-matter，触发全靠 description |
| **doubao-marketing-plan**<br>`skill-9a1fc87b6dfbc652321fb7471edbce13` | — | 首席营销策划官 | references/（5 文件） | 极简 front-matter，触发全靠 description |
| **doubao-oceanengine-adops-agent**<br>`skill-6a293591d44ba7b56a89723dae156648` | — | 字节UG自动化投放Agent 的巨量引擎只读盯盘与数据分析 Skill | references/+agents/+assets/（5 文件） | 极简 front-matter，触发全靠 description |

## 媒体生成（9）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **byted-mediakit-audio**<br>`skill-263384a266b113960d8b393b4b4a2728` | 0.2.1 | 面向音频文件或视频中的音轨，处理语音边界定位、音频媒资信息探测、音频转码与码流封装适配、人声与背景声分离等目标 | reference/（6 文件） | requires.bins 依赖声明；cliHelp 探测命令；product/domain 归属；license 字段；permissions 声明(shell)；version 字段（front-matter 完整度中上） |
| **byted-mediakit-editing**<br>`skill-52d2686c64803679b30cab66dda0256f` | 0.2.1 | 面向音频、视频或图片素材组成成片的编辑制作目标，适用于时间线裁剪与拼接、速度和音量调整、视频滤镜、运镜特效、转场、画面裁切旋转翻转、字幕压制、局部模糊、动图截取、淡入淡出、音视频提取与合流、音频混合以及多画面空间组合等操… | reference/（22 文件） | requires.bins 依赖声明；cliHelp 探测命令；product/domain 归属；license 字段；permissions 声明(shell)；version 字段（front-matter 完整度中上） |
| **byted-mediakit-image**<br>`skill-e9640cf7dd453cd61a9e1de4e5cf2974` | 0.2.1 | 面向单张或批量图片的视觉处理、质量优化、内容理解与基础编辑目标，适用于图片尺寸缩放与体积治理、质量优先缩小体积、明确体积上限/质量值/格式转换的压缩、元信息探测、裁剪旋转翻转与圆角、颜色与锐化清晰度调整、负片、模糊与打码… | reference/（24 文件） | requires.bins 依赖声明；cliHelp 探测命令；product/domain 归属；license 字段；permissions 声明(shell)；version 字段（front-matter 完整度中上） |
| **byted-mediakit-shared**<br>`skill-0155e0700fe60480e64462936fc9e13d` | 0.2.1 | MediaKit 是面向音视频与图像处理的专业工具集，覆盖音视频剪辑与合成、音频媒资探测与人声分离、视频理解与增强、图像增强与内容理解等工作流 | reference/（3 文件） | 纯路由入口 skill：能力范围表→领域 skill 优先加载映射；capability_count 元数据 |
| **byted-mediakit-video**<br>`skill-6d7a40e381e76fc8c73b8dfe2a38c787` | 0.2.1 | 面向视频文件的智能处理、媒资理解、画质治理与画质检测、抽帧、隐私保护、字幕与水印处理、精彩片段与高光拆条分析生成、剧情结构化与剧本整理、场景与语义分段、画面文字识别、视频转码转封装及人像或绿幕抠像等目标 | reference/（31 文件） | capability 工具清单总表（工具×说明×命令×参考链接）；跨域路由写进 description；依赖 shared 入口包（缺失即报错）；permissions+requires.bins+cliHelp 全套声明 |
| **doubao-video-extract**<br>`skill-fce738a0eeb3fa43b81adac5f74a62fa` | — | 可提取、下载、解析、理解在线视频或本地视频文件 | references/+scripts/（53 文件） | 极简 front-matter，触发全靠 description |
| **seed-audio**<br>`skill-6cc06ce155d62f977cdfd0544a1ab745` | 0.2.0 | 用自然语言描述生成目标音频 | references/（3 文件） | version 字段（front-matter 完整度中上） |
| **seedance-25**<br>`skill-07a8c729b0e5233caf7131bef55c7376` | — | 使用seedance2.5模型生成视频,使用 Seedance 2.5 按用户原始提示词生成视频，禁止改写提示词或切换模型，并在生成前补齐时长、比例和检索所得的必要信息后向用户确认原样透传提示词、不润色视频 prompt… | 单文件(仅SKILL.md)（1 文件） | 极简 front-matter，触发全靠 description |
| **seedream-50**<br>`skill-1417b29973e6675d7cc097b0cf82b36b` | — | 当用户明确要求使用“5.0”“5.0 Pro”“5.0pro”“Seedream 5.0 Pro”生成、编辑、重绘或延展图片时，必须调用此 Skill | 单文件(仅SKILL.md)（1 文件） | 接力型 skill：只做 Prompt 组装，交接给 doubao-creative-design 执行；模板化 T2I/I2I prompt 结构 |

## 浏览器/系统操作（3）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **browser-record-replay**<br>`skill-3a40ced2ec19e4f9f9066bf979b5f312` | — | Develop, record, debug, and deliver reusable browser RPA Skills with the browser built into Doubao. Use for sa… | references/+agents/（6 文件） | 极简 front-matter，触发全靠 description |
| **browser-use-automation**<br>`skill-e8b6eb9f86c79e56fc70a1e3ed19a786` | — | Control websites exclusively through the CNGC Browser Use stack: `computer_use_tool` with `plane=\"bu\"` and `… | references/（10 文件） | compatibility 字段声明运行环境依赖；安全信任边界与『强制用户接管』清单（登录/验证码/支付必须 interaction.request_action）；站点规则仅作业务参考 |
| **computer-use-automation**<br>`skill-64b33f2ad6ae097dbbe70261f6b53aa0` | — | Use this Windows Computer Use skill whenever the user wants to open, switch to, or operate a desktop app or lo… | 单文件(仅SKILL.md)（1 文件） | compatibility 字段声明 computer_use_tool 依赖（同类写法） |

## 平台工具（8）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-app-builder**<br>`skill-b13f8e677a563c7fad5d5cb971f17cb2` | — | 统一处理应用级和工程级产品的设计、开发、编辑及产物问答（单页html和h5的开发和设计不要使用这个skill） | reference/（15 文件） | 极简 front-matter，触发全靠 description |
| **doubao-cron-scheduler**<br>`skill-c25e1a6d14b8b3751923b8def385bb24` | — | 创建、查看、更新或删除定时任务：一次性提醒、周期任务、后台监控、多轮编辑已有任务、登录态/权限敏感任务 | 单文件(仅SKILL.md)（1 文件） | 单文件；锚定时间与歧义澄清规则；登录态检查清单与失败处理分支 |
| **doubao-enterprise-search**<br>`skill-ef15d08b8a132f0f8879f7ea7dd72dc0` | — | 判断是否调用 `enterprise_agentic_search` 工具前，必须先完整读取 `doubao-enterprise-search` skill | 单文件(仅SKILL.md)（1 文件） | 单文件无 references（17k 字全部内联）；路由判断含『硬性排除』清单与默认倾向；多轮继承规则 |
| **doubao-identity**<br>`skill-16ba2193b90892fefbb3f640c2ae34f3` | — | 当用户询问豆包工作、豆包专业版、豆包会员与付费服务（包含权益、充值、退款、发票、订阅、连续包月/包年比较、学生优惠、录音转写、创作额度等）、平台规则与隐私安全（使用条款、隐私政策、内容安全、客服投诉、聊天记录存储/删除/… | references/（6 文件） | 极简 front-matter，触发全靠 description |
| **doubao-pc-optimizer**<br>`skill-7ab40cedd855dc30da4c0ce83d0bd02a` | — | 用户需要清理磁盘垃圾、释放空间、处理电脑卡顿或开机慢、优化 Windows/macOS 性能、提升游戏帧率、生成安全清理脚本，或提到 C 盘满、磁盘空间不足、掉帧、运行慢时使用 | references/+scripts/+agents/（11 文件） | 极简 front-matter，触发全靠 description |
| **doubao-record**<br>`skill-69d323e83107ae501bc68116483f5832` | — | 启动当前飞书会话的录音 | 单文件(仅SKILL.md)（1 文件） | 极简 front-matter，触发全靠 description |
| **skill-creator-for-work**<br>`skill-6029eb84e8a494e03cfdaf144da253e7` | — | 创建有效 Skill 的指南 | references/+scripts/（6 文件） | 官方元技能：渐近披露三级模型与 <500 行上限、自由度分级（高/中/低）、禁建 README 等冗余文件、front-matter 仅 name+description 的规范声明 |
| **verifier-hub**<br>`skill-416a081b7921c7a80d46eff9751c72c0` | 2.1 | Deterministic artifact verifier CLI (file/xlsx/docx/pdf/pptx/text/archive/rubric) for pre-delivery artifact ch… | references/（18 文件） | compatibility 环境声明 + Windows 入口差异提示；『58 个子命令』式能力概括写入 description；JSON 输出含可引用 evidence 字段 |

## 其他（8）

| 名称（解压目录） | 版本 | 一句话能力 | 目录结构特征 | 值得借鉴的写法 |
|---|---|---|---|---|
| **doubao-data-analysis**<br>`skill-3a385ecc9f04a65b5aa266c0967fca26` | — | 结构化业务数据分析：附件读取与口径核验、定向筛选、规则/阈值判定、指标异动归因、漏斗/留存/实验分析、经营复盘及可审计报告 | references/+scripts/+agents/（15 文件） | 极简 front-matter，触发全靠 description |
| **doubao-game-designer**<br>`skill-16c0c9701f05d6bff1746e22b3bb0d92` | — | 把游戏创意、参考作品、现有方案、配置或试玩证据转化为玩法成立、规则闭合、数值可复算且能进入制作的 GDD、玩法方案与系统规格 | references/+scripts/+agents/（74 文件） | 正文仅 363 字的『薄入口』：一段任务定义+一句『每次完整读取 references/workflow.md』，全部内容下沉 references/ |
| **doubao-human-signal**<br>`skill-8a10c84639c6cb6dab3dbf482140a93c` | — | 去除或避免文本中的 AI 味 | references/+agents/（13 文件） | 极简 front-matter，触发全靠 description |
| **doubao-questionnaire-designer**<br>`skill-d77268dcd14762bfc38cf8f3731e2153` | — | 用户研究一站式助手,覆盖四大能力:①问卷设计(按调研目标产出可落地问卷,含试填优化,交付 Word/飞书文档);②访谈提纲(题量按诉求动态确定、含追问轮次/方向/触发条件的深访提纲);③开放题原声打标(五步工作流建立标签… | references/（6 文件） | 极简 front-matter，触发全靠 description |
| **doubao-ultimate-guide**<br>`skill-a73a1dfd0b0dba29339b610fb312483a` | — | 统一攻略创作总控 Skill：根据用户需求路由到旅游攻略、健身攻略、美食烹饪教程、游戏攻略四个分支，默认先创建飞书/Lark 文档容器，再读取对应分支 Skill 生成内容并写入同一个文档 | branches/（64 文件） | branches/ 每分支独立子目录；『总控先创建文档，分支只写内容』跨分支一致性规则；六类边界路由（不明/缺信息/不适用/多意图/冲突/强时效） |
| **doubao-visualization**<br>`skill-c2626f849256b8e5c00651ff69addb8e` | — | 当回答涉及趋势、占比、比较、流程、机制、因果、架构、关系、时间线、状态机、算法步骤、参数变化、原图证据，或用户明确要求图表、图解、标注、动态/交互演示时使用 | references/+scripts/+agents/+schemas/（25 文件） | 极简 front-matter，触发全靠 description |
| **gift-card-redemption**<br>`skill-1199def7f62a07895bd7adfe5deead9b` | — | 查询豆包订阅礼品卡的可兑换状态和套餐，并在确认后完成兑换 | references/（3 文件） | 极简 front-matter，触发全靠 description |
| **student-discount-application**<br>`skill-b44daad2dd2dfef2fbdb73c43b8069cb` | — | 办理豆包专业版学生优惠申请：引导用户绑定抖音、完成学生认证并领取权益 | references/+agents/（13 文件） | 极简 front-matter，触发全靠 description |

---

## 类别说明与归类口径

- **文档办公**：word / ppt / sheet / html / doubao-pdf / artifact-preview——本地与在线文档的创建编辑渲染。ppt/sheet 实际操作飞书在线件，归此类因其交付物是演示文稿/表格。
- **飞书协同**：lark-* 17 个——飞书开放能力（Base/Docx/IM/Mail/Drive/Calendar/OKR/Task/Wiki/白板/会议/审批/考勤/通讯录/Markdown/meeting/workflow-standup-report/openapi-explorer）。
- **学术科研**：调研/润色/评测/精读/期刊排版/开题/参考文献审计/批判性阅读。
- **医疗健康**：文献检索/监控/解读/翻译、临床决策、体检报告、循证问答——医疗细分场景全家桶。
- **金融投研**：个股筛选/财报分析/行业分析/一级二级公司研究/财务建模/财富规划/每日行情/多股对比。
- **法律合规**：合同审查/起草/修订、DPA 起草、专利起草、合规评估、个人信息审计、营销材料审查。
- **电商跨境**：选品/商品内容/商品问答/Listing 本地化/客服/电商提案/情感追踪/跨境电商合规税务物流；product-analysis / product-manager / product-qa 三个产品经理向 skill 因命名命中 product- 前缀归入此类。
- **内容创作**：小说/图书/新媒体/多平台改写/创意设计/创意短剧/创意视频/头条日历/跨境增长内容。
- **营销增长**：市场热点/营销策划/巨量引擎投放/公告解读。
- **媒体生成**：mediakit 五件套（shared+audio/editing/image/video）+ seedream-50 / seedance-25 / seed-audio / doubao-video-extract。
- **浏览器/系统操作**：browser-record-replay / browser-use-automation / computer-use-automation。
- **平台工具**：app-builder / cron-scheduler / enterprise-search / identity / record / skill-creator-for-work / verifier-hub / pc-optimizer。
- **其他**：doubao-data-analysis（业务数据分析）、doubao-visualization（图表图解）、doubao-game-designer（游戏策划）、doubao-questionnaire-designer（问卷调研）、doubao-human-signal（去 AI 味）、doubao-ultimate-guide（四合一攻略总控）、gift-card-redemption 与 student-discount-application（豆包平台运营件）。

## 三代包风格（按 front-matter 丰富度分层）

1. **极简代**（doubao-* 大多数，约 70 包）：front-matter 只有 `name` + `description`，全靠 description 触发，正文承载全部规范。
2. **飞书 CLI 代**（lark-*、ppt/sheet）：加 `version` + `metadata.{requires.bins, cliHelp}`，宿主用 bins 探测 lark-cli 可用性、用 cliHelp 拉取命令帮助。
3. **工程化代**（byted-mediakit-*、verifier-hub/artifact-preview、wealth-planning 等）：补齐 `license` / `permissions` / `compatibility` / `metadata.{product,domain,capability_count,hub}`，并配 evals/tests/schemas/config，接近可独立测试的软件包。

> 生成时间：2026-09-29；生成脚本：`_analysis/parse_fm.py` + `_analysis/build_catalog.py` + `_analysis/gen_catalog_md.py`；原始解析数据：`_analysis/fm.json`、`_analysis/catalog_rows.json`。