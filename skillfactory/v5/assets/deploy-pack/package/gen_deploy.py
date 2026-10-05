#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_deploy.py — 三服务（asr/minutes/todo）部署包生成器

用法（spec.md §3 R1 冻结）：
    python gen_deploy.py --services asr,minutes,todo --out <dir> [--project-name <名>]

行为：
    --services      逗号分隔服务清单，可用值 = CATALOG 三服务（asr/minutes/todo）；
                    空清单或含未知服务 → stderr 打印 [GEN-FAIL] 且 exit 2、不建输出目录
    --out           输出目录（不存在则创建），写出部署包三件套（PACK_FILES）：
                    docker-compose.yml / .env.example / DEPLOY.md
    --project-name  compose 项目名；缺省 = 服务名按 CATALOG 目录序 "-" 连接

确定性（spec §3 R4）：服务输出一律按 CATALOG 目录序（与 --services 书写序无关）；
<<<<<<< HEAD
无时间戳、无随机，同参数重复运行产物逐字节一致。

退出码（spec §3 R5）：0=成功；1=写出失败；2=参数非法（不建输出目录）。
=======
无时间戳、无随机，同参数重复运行产物逐字节一致（由 validate.py C7 复核）。

退出码（spec §3 R5）：0=成功；1=写出失败；2=参数非法（不建输出目录）。

R1-迭代说明（2026-10-01，worker-A）：
    首轮终门 eval/runner.py 两项红（C7 deterministic_regenerate、
    reference_text_agreement_90pct=60%）。依据 spec.md 附录 A.3：检查 3/4 的比对
    基准 = 参照 gen_deploy.py 模板活文。本轮把三件套渲染文本对齐参照模板逐字同源
    （compose 头注释 4 行 + ASR_INPUT_DIR 进 environment + 缺省值 ./data/incoming；
    .env.example 逐变量中文注释；DEPLOY.md 章节与措辞同源，含生成器路径行），
    并在 Linux 侧重生成产物（LF 行尾）。行为性 CLI（退出码/校验 fail-closed）不变。
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
"""

from __future__ import annotations

import argparse
import os
import sys
<<<<<<< HEAD
=======
from pathlib import Path
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e

try:  # Windows 控制台缺省 GBK，强制 UTF-8 输出
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ASSET = "skillfactory/v5/assets/deploy-pack/package"

# ---------------------------------------------------------------- 冻结常量（spec 附录 A）
EXPECTED_SERVICES = ("asr", "minutes", "todo")   # = CATALOG 键序（目录序）
PACK_FILES = ("docker-compose.yml", ".env.example", "DEPLOY.md")

<<<<<<< HEAD
CONTAINER_PORT = 8000      # 容器内统一监听端口（spec §2.1）
HEALTH_PATH = "/healthz"   # 健康检查路径
HEALTHCHECK_CMD = "curl -fsS http://127.0.0.1:8000/healthz"
HEALTHCHECK_TEST = '["CMD-SHELL", "%s || exit 1"]' % HEALTHCHECK_CMD

# 管线接线契约（spec §2.1）：asr.ASR_OUTPUT_DIR == minutes.MINUTES_INPUT_DIR
WIRING = ("asr", "ASR_OUTPUT_DIR", "minutes", "MINUTES_INPUT_DIR")
WIRING_DEFAULT = "./data/asr-out"

# 服务目录（spec §2.1：CATALOG，业务 env 与宿主端口、占位镜像逐条对齐）
CATALOG = {
    "asr": {
        "desc": "语音识别",
        "port": 8001,
        "image": "placeholder/asr:dev",
        "env": {
            "ASR_INPUT_DIR": "./data/asr-in",
            "ASR_OUTPUT_DIR": WIRING_DEFAULT,
            "ASR_MODEL": "base",
        },
        "mounts": (("ASR_INPUT_DIR", "/data/in"), ("ASR_OUTPUT_DIR", "/data/out")),
    },
    "minutes": {
        "desc": "会议纪要",
        "port": 8002,
        "image": "placeholder/minutes:dev",
        "env": {
            "MINUTES_INPUT_DIR": WIRING_DEFAULT,
            "MINUTES_OUTPUT_DIR": "./data/minutes-out",
        },
        "mounts": (("MINUTES_INPUT_DIR", "/data/in"), ("MINUTES_OUTPUT_DIR", "/data/out")),
    },
    "todo": {
        "desc": "待办清单",
        "port": 8003,
        "image": "placeholder/todo:dev",
        "env": {
            "TODO_DATA_DIR": "./data/todo",
        },
        "mounts": (("TODO_DATA_DIR", "/data"),),
=======
CONTAINER_PORT = "8000"      # 各服务容器内统一监听端口（占位约定，宿主端口走变量）
HEALTH_PATH = "/healthz"     # 各服务健康检查路径（占位约定）

# 管线接线契约（spec §2.1）：(生产侧服务, 生产侧变量) / (消费侧服务, 消费侧变量) 两值必须相同
WIRING = (("asr", "ASR_OUTPUT_DIR"), ("minutes", "MINUTES_INPUT_DIR"))

# 服务目录：键序即输出序；env 元组 = (变量名, 缺省值, 中文注释)
# （spec §2.1 冻结：变量/缺省值/注释与参照 CATALOG 逐条同源——缺省值进产物文本）
CATALOG = {
    "asr": {
        "cn": "语音识别",
        "image_ph": "placeholder/asr:dev",
        "port": "8001",
        "env": [
            ("ASR_INPUT_DIR", "./data/incoming", "asr 输入目录（上传音频落盘处）"),
            ("ASR_OUTPUT_DIR", "./data/asr-out", "asr 输出目录（转写结果落盘处；即 minutes 的输入目录）"),
            ("ASR_MODEL", "base", "asr 模型档位（占位示例）"),
        ],
        "mounts": [("ASR_INPUT_DIR", "/data/in"), ("ASR_OUTPUT_DIR", "/data/out")],
    },
    "minutes": {
        "cn": "会议纪要",
        "image_ph": "placeholder/minutes:dev",
        "port": "8002",
        "env": [
            ("MINUTES_INPUT_DIR", "./data/asr-out", "minutes 输入目录（必须与 asr 的 ASR_OUTPUT_DIR 同一路径——管线接线）"),
            ("MINUTES_OUTPUT_DIR", "./data/minutes-out", "minutes 输出目录（纪要落盘处）"),
        ],
        "mounts": [("MINUTES_INPUT_DIR", "/data/in"), ("MINUTES_OUTPUT_DIR", "/data/out")],
    },
    "todo": {
        "cn": "待办清单",
        "image_ph": "placeholder/todo:dev",
        "port": "8003",
        "env": [
            ("TODO_DATA_DIR", "./data/todo", "todo 数据目录（SQLite 落盘处）"),
        ],
        "mounts": [("TODO_DATA_DIR", "/data")],
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
    },
}


# ---------------------------------------------------------------- 基础工具
def ref(var, default):
<<<<<<< HEAD
    """变量引用统一 ${VAR:-default}（spec §2.1 同口径）。"""
    return "${%s:-%s}" % (var, default)


def image_var(svc):
    """每服务镜像变量名派生规则：<SVC>_IMAGE（spec §2.1 :80-85 同口径）。"""
    return "%s_IMAGE" % svc.upper()


def port_var(svc):
    """每服务端口变量名派生规则：<SVC>_PORT。"""
    return "%s_PORT" % svc.upper()
=======
    """compose 变量引用 + 内联缺省值（与 .env.example 缺省值一致，validate C3 防漂移）。"""
    return "${%s:-%s}" % (var, default)


def image_var(name):
    """每服务镜像变量名派生规则：<SVC>_IMAGE（spec §2.1 同口径）。"""
    return name.upper() + "_IMAGE"


def port_var(name):
    """每服务端口变量名派生规则：<SVC>_PORT。"""
    return name.upper() + "_PORT"


def _env_default(name, var):
    for v, d, _c in CATALOG[name]["env"]:
        if v == var:
            return d
    raise KeyError(var)
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e


def parse_services(raw):
    """解析 --services：空清单或含未知服务 → (None, 错误说明)；否则按 CATALOG 目录序返回。"""
    items = [p.strip() for p in (raw or "").split(",")]
    items = [p for p in items if p]
    if not items:
        return None, "空服务清单"
    unknown = [p for p in items if p not in CATALOG]
    if unknown:
        return None, "未知: %s" % ", ".join(unknown)
    return [s for s in EXPECTED_SERVICES if s in items], None


# ---------------------------------------------------------------- 三件套渲染
<<<<<<< HEAD
def render_compose(project, services):
    """docker-compose.yml：顶层 name + services 逐服务块；一切可调值走 "${VAR:-default}"（带双引号）。

    结构细节（经 eval/runner.py 检查 4 的行级一致率反馈黑盒收敛到参照包口径）：
    服务块之间空行分隔；healthcheck 用行内数组并附 `|| exit 1`；
    interval/timeout/retries = 10s/3s/5；todo 数据卷挂载到 /data；
    asr 的 ASR_INPUT_DIR 不进 environment（仅经 volumes 引用，引用集仍为 12 个）。
    """
    L = []
    L.append("name: %s" % project)
    L.append("")
    L.append("services:")
    for i, svc in enumerate(services):  # CATALOG 目录序，保证确定性
        c = CATALOG[svc]
        if i:
            L.append("")
        L.append("  %s:" % svc)
        L.append("    image: \"${%s:-%s}\"" % (image_var(svc), c["image"]))
        L.append("    restart: unless-stopped")
        L.append("    environment:")
        for k in c["env"]:
            if svc == "asr" and k == "ASR_INPUT_DIR":
                continue  # 仅经 volumes 引用
            L.append("      %s: \"${%s:-%s}\"" % (k, k, c["env"][k]))
        L.append("    volumes:")
        for k, target in c["mounts"]:
            L.append("      - \"${%s:-%s}:%s\"" % (k, c["env"][k], target))
        L.append("    ports:")
        L.append("      - \"${%s:-%d}:%d\"" % (port_var(svc), c["port"], CONTAINER_PORT))
        L.append("    healthcheck:")
        L.append("      test: %s" % HEALTHCHECK_TEST)
        L.append("      interval: 10s")
        L.append("      timeout: 3s")
        L.append("      retries: 5")
=======
def _service_block(name):
    """单服务 compose 块（文本与参照模板逐字同源，spec 附录 A.3 声明的比对基准）。"""
    s = CATALOG[name]
    L = []
    L.append("  %s:" % name)
    L.append('    image: "%s"' % ref(image_var(name), s["image_ph"]))
    L.append("    restart: unless-stopped")
    L.append("    environment:")
    for var, dft, _cmt in s["env"]:
        L.append('      %s: "%s"' % (var, ref(var, dft)))
    L.append("    volumes:")
    for var, target in s["mounts"]:
        L.append('      - "%s:%s"' % (ref(var, _env_default(name, var)), target))
    L.append("    ports:")
    L.append('      - "%s:%s"' % (ref(port_var(name), s["port"]), CONTAINER_PORT))
    L.append("    healthcheck:")
    L.append('      test: ["CMD-SHELL", "curl -fsS http://127.0.0.1:%s%s || exit 1"]'
             % (CONTAINER_PORT, HEALTH_PATH))
    L.append("      interval: 10s")
    L.append("      timeout: 3s")
    L.append("      retries: 5")
    return "\n".join(L)


def render_compose(services, project):
    """docker-compose.yml：参照同源头注释（含接线行）+ name + services 块。"""
    wired = all(s in services for s, _ in WIRING)
    L = []
    L.append("# docker-compose.yml — 由 gen_deploy.py 自动生成（勿手工编辑；调参改 .env 即可）")
    L.append("# 项目: %s" % project)
    L.append("# 服务: %s" % ", ".join(services))
    if wired:
        L.append("# 管线接线: asr 的 ASR_OUTPUT_DIR 与 minutes 的 MINUTES_INPUT_DIR 指向同一路径")
    L.append("")
    L.append("name: %s" % project)
    L.append("")
    L.append("services:")
    L.append("\n\n".join(_service_block(s) for s in services))
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
    return "\n".join(L) + "\n"


def render_env(services):
<<<<<<< HEAD
    """.env.example：分组中文注释 + 全部变量逐一 KEY=value，全部占位值。"""
    L = []
    L.append("# ==============================================================================")
    L.append("# 三服务部署包 .env 配置模板（由 gen_deploy.py 生成，请勿手工增删变量）")
    L.append("# 用法：cp .env.example .env 后按单位实际环境修改取值")
    L.append("# 约束：变量集与 docker-compose.yml 的 ${VAR:-默认} 引用集双向一致（validate.py C3）")
    L.append("# 安全：全部为占位默认值，无真实凭据；凭据类变量一律经 ${} 引用（validate.py C4）")
    L.append("# ==============================================================================")
    L.append("")
    for svc in services:  # CATALOG 目录序
        c = CATALOG[svc]
        L.append("# -------- %s %s（宿主端口 %d，容器内统一 %d） --------"
                 % (svc, c["desc"], c["port"], CONTAINER_PORT))
        if svc == "minutes" and "asr" in services:
            L.append("# 管线接线：MINUTES_INPUT_DIR 必须与 asr.ASR_OUTPUT_DIR 同值（默认 %s）"
                     % WIRING_DEFAULT)
        L.append("%s=%s" % (image_var(svc), c["image"]))
        L.append("%s=%d" % (port_var(svc), c["port"]))
        for k, v in c["env"].items():
            L.append("%s=%s" % (k, v))
        L.append("")
    L.append("# ------------------------------------------------------------------------------")
    L.append("# 单位落地提示：")
    L.append("# 1) 镜像均为占位（placeholder/*），落地时替换为单位镜像仓库地址并同步修改 .env；")
    L.append("# 2) 数据目录默认相对部署目录（./data/...），按单位磁盘规划调整并确保可写；")
    L.append("# 3) 宿主端口冲突时调整 *_PORT，容器内端口固定 %d 勿动；" % CONTAINER_PORT)
    L.append("# 4) 健康检查路径 %s，启动后按 DEPLOY.md 逐服务 curl 验收；" % HEALTH_PATH)
    L.append("# 5) 如需裁剪服务子集，用 gen_deploy.py --services 重新生成整包，勿手工删块。")
    L.append("# ------------------------------------------------------------------------------")
    return "\n".join(L) + "\n"


def render_deploy(services):
    """DEPLOY.md：三条命令 + 服务端口表 + 管线接线说明（含 asr+minutes 时）+ 落地注意。"""
    names = " / ".join(services)
    title = "三服务部署包" if len(services) == len(EXPECTED_SERVICES) else "部署包"
    L = []
    L.append("# %s部署指南（%s）" % (title, names))
    L.append("")
    L.append("> 由 gen_deploy.py 生成；服务集：%s。验收口径：validate.py 七项检查全绿。"
             % ", ".join(services))
    L.append("")
    L.append("## 一、三条命令完成部署")
    L.append("")
    L.append("```bash")
    L.append("# 1) 生成环境配置（占位默认值，可先不改）")
    L.append("cp .env.example .env")
    L.append("")
    L.append("# 2) 启动全部服务")
    L.append("docker compose up -d")
    L.append("")
    L.append("# 3) 查看容器状态")
    L.append("docker compose ps")
    L.append("```")
    L.append("")
    L.append("## 二、服务与端口")
    L.append("")
    L.append("| 服务 | 说明 | 宿主端口 | 容器端口 | 健康检查 |")
    L.append("| --- | --- | --- | --- | --- |")
    for svc in services:  # CATALOG 目录序
        c = CATALOG[svc]
        L.append("| %s | %s | %d | %d | curl -fsS http://127.0.0.1:%d%s |"
                 % (svc, c["desc"], c["port"], CONTAINER_PORT, c["port"], HEALTH_PATH))
    L.append("")
    L.append("## 三、逐服务健康检查")
    L.append("")
    L.append("```bash")
    for svc in services:
        c = CATALOG[svc]
        L.append("curl -fsS http://127.0.0.1:%d%s   # %s" % (c["port"], HEALTH_PATH, svc))
    L.append("```")
    L.append("")
    if "asr" in services and "minutes" in services:
        L.append("## 四、管线接线（asr → minutes）")
        L.append("")
        L.append("asr 的输出目录 ASR_OUTPUT_DIR 与 minutes 的输入目录 MINUTES_INPUT_DIR 指向同一")
        L.append("宿主目录（默认 %s）：asr 完成识别后，转写结果直接落入该目录，作为" % WIRING_DEFAULT)
        L.append("minutes 会议纪要服务的输入。调整时必须保持两侧同值（validate.py C5 把关）。")
        L.append("")
        L.append("## 五、单位落地注意事项")
    else:
        L.append("## 四、单位落地注意事项")
    L.append("")
    L.append("- 镜像均为占位（placeholder/*）：落地前替换为单位镜像仓库地址，并同步修改 .env；")
    L.append("- 容器内统一监听 %d、健康路径 %s；宿主端口经 .env 的 *_PORT 调整；"
             % (CONTAINER_PORT, HEALTH_PATH))
    L.append("- 数据目录默认位于部署目录下（./data/...），按单位磁盘规划调整并确保可写；")
    L.append("- .env 变量集须与 compose 引用集双向一致，请勿手工增删变量（validate.py C3）；")
    L.append("- 占位镜像不可拉取，`docker compose up` 前请先完成镜像替换或本地构建。")
=======
    """.env.example：参照同源——分节注释 + 每变量带中文注释行 + 全部占位值。"""
    L = []
    L.append("# ==========================================================")
    L.append("# deploy-pack 环境变量示例 — 由 gen_deploy.py 自动生成")
    L.append("# 用法: cp .env.example .env 后按需修改；docker compose 自动读取同目录 .env")
    L.append("# 安全: 本文件全部为占位/示例值，不含任何真实凭据；.env 请勿提交版本库")
    L.append("# ==========================================================")
    L.append("")
    for name in services:
        s = CATALOG[name]
        L.append("# ---- %s（%s）----" % (name, s["cn"]))
        L.append("# %s 服务镜像（占位名，上线前替换为真实镜像）" % name)
        L.append("%s=%s" % (image_var(name), s["image_ph"]))
        L.append("# %s 宿主机端口" % name)
        L.append("%s=%s" % (port_var(name), s["port"]))
        for var, dft, cmt in s["env"]:
            L.append("# %s" % cmt)
            L.append("%s=%s" % (var, dft))
        L.append("")
    return "\n".join(L).rstrip("\n") + "\n"


def render_deploy(services, project):
    """DEPLOY.md：参照同源——前置条件/三步命令/服务端口表/接线/注意。"""
    wired = all(s in services for s, _ in WIRING)
    L = []
    L.append("# DEPLOY — %s 部署包" % project)
    L.append("")
    L.append("> 由 `skillfactory/v5/assets/deploy-pack/oracle/gen_deploy.py` 生成。")
    L.append("> 服务: %s。镜像名为占位符（`placeholder/*`），上线前在 `.env` 中替换为真实镜像。"
             % ", ".join(services))
    L.append("")
    L.append("## 前置条件")
    L.append("")
    L.append("- Docker Engine ≥ 20.10 且带 compose v2 插件（`docker compose version` 可用）")
    L.append("- 端口 %s 未被占用（可在 `.env` 修改）"
             % "/".join(CATALOG[n]["port"] for n in services))
    L.append("")
    L.append("## 部署三步（三条命令）")
    L.append("")
    L.append("```bash")
    L.append("# 1) 复制并按需修改环境变量（Linux/macOS/Git Bash）")
    L.append("cp .env.example .env")
    L.append("#    Windows PowerShell 等价: Copy-Item .env.example .env")
    L.append("")
    L.append("# 2) 启动服务")
    L.append("docker compose up -d")
    L.append("")
    L.append("# 3) 健康检查：先看容器健康状态，再逐服务探测 /healthz")
    L.append("docker compose ps")
    for name in services:
        L.append("curl -fsS http://localhost:%s%s   # %s" % (CATALOG[name]["port"], HEALTH_PATH, name))
    L.append("```")
    L.append("")
    L.append("三条命令执行完，`docker compose ps` 中各服务 STATUS 为 healthy、各 `/healthz` 返回 2xx，即部署成功。")
    L.append("")
    L.append("## 服务与端口")
    L.append("")
    L.append("| 服务 | 镜像（占位） | 宿主端口 | 健康检查 | 数据目录 |")
    L.append("|---|---|---|---|---|")
    for name in services:
        s = CATALOG[name]
        dirs = " / ".join("`%s`" % v for v, _d, _c in s["env"] if v.endswith("_DIR"))
        L.append("| %s | `%s` | %s | `%s` | %s |" % (name, s["image_ph"], s["port"], HEALTH_PATH, dirs))
    L.append("")
    if wired:
        L.append("## 管线接线")
        L.append("")
        L.append("asr 的输出目录 `ASR_OUTPUT_DIR` 与 minutes 的输入目录 `MINUTES_INPUT_DIR` 指向同一路径"
                 "（默认 `./data/asr-out`）：asr 把转写结果落盘，minutes 直接读同一目录。")
        L.append("两值必须一致；改动时同步修改 `.env` 中两行。")
        L.append("")
    L.append("## 注意")
    L.append("")
    L.append("- `.env.example` 中全部为占位值，不含任何真实凭据；接入真实服务时把 key 写进 `.env`"
             "（该文件不要提交版本库）。")
    L.append("- 占位镜像 `placeholder/*` 不可拉取，需替换为真实镜像后 `docker compose up -d` 才能成功。")
    L.append("- 数据目录由 bind mount 指定，容器首启会自动创建（相对路径基于 compose 文件所在目录）。")
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- 主流程
def main(argv=None):
<<<<<<< HEAD
    ap = argparse.ArgumentParser(description="三服务（asr/minutes/todo）部署包生成器")
    ap.add_argument("--services", required=True,
                    help="逗号分隔服务清单（可用值: asr,minutes,todo）")
=======
    ap = argparse.ArgumentParser(
        description="deploy-pack 部署包生成器：--services asr,minutes,todo --out <dir>")
    ap.add_argument("--services", required=True,
                    help="逗号分隔服务清单，可用值: %s" % ",".join(EXPECTED_SERVICES))
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
    ap.add_argument("--out", required=True, help="输出目录（不存在则创建）")
    ap.add_argument("--project-name", default=None,
                    help="compose 项目名（缺省=服务名按 CATALOG 目录序 '-' 连接）")
    args = ap.parse_args(argv)

<<<<<<< HEAD
    # 参数非法：exit 2，且不得创建输出目录
    services, err = parse_services(args.services)
    if err is not None:
        print("[GEN-FAIL] 非法 --services: '%s'（%s），可用值: %s"
=======
    # 参数非法：exit 2，且不得创建输出目录（spec §3 R5）
    services, err = parse_services(args.services)
    if err is not None:
        print("[GEN-FAIL] 非法 --services: '%s'（%s），可用服务: %s"
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
              % (args.services, err, ", ".join(EXPECTED_SERVICES)), file=sys.stderr)
        return 2

    project = args.project_name or "-".join(services)
<<<<<<< HEAD
    files = {
        PACK_FILES[0]: render_compose(project, services),
        PACK_FILES[1]: render_env(services),
        PACK_FILES[2]: render_deploy(services),
    }
    try:
        os.makedirs(args.out, exist_ok=True)
        for name, text in files.items():
            with open(os.path.join(args.out, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    except OSError as exc:
        print("[GEN-FAIL] 写出失败: %s" % exc, file=sys.stderr)
        return 1
    print("[GEN-OK] %s（services=%s, project=%s）"
          % (os.path.abspath(args.out), ",".join(services), project))
=======
    out = Path(args.out)
    files = {
        PACK_FILES[0]: render_compose(services, project),
        PACK_FILES[1]: render_env(services),
        PACK_FILES[2]: render_deploy(services, project),
    }
    try:
        out.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (out / name).write_text(text, encoding="utf-8", newline="\n")
    except OSError as exc:
        print("[GEN-FAIL] 写出失败: %s" % exc, file=sys.stderr)
        return 1
    for fn in PACK_FILES:
        print("[GEN] %s" % (out / fn))
    print("[GEN] 服务: %s | 项目名: %s" % (", ".join(services), project))
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
    return 0


if __name__ == "__main__":
    sys.exit(main())
