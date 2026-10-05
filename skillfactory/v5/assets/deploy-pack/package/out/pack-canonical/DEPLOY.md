<<<<<<< HEAD
# 三服务部署包部署指南（asr / minutes / todo）

> 由 gen_deploy.py 生成；服务集：asr, minutes, todo。验收口径：validate.py 七项检查全绿。

## 一、三条命令完成部署

```bash
# 1) 生成环境配置（占位默认值，可先不改）
cp .env.example .env

# 2) 启动全部服务
docker compose up -d

# 3) 查看容器状态
docker compose ps
```

## 二、服务与端口

| 服务 | 说明 | 宿主端口 | 容器端口 | 健康检查 |
| --- | --- | --- | --- | --- |
| asr | 语音识别 | 8001 | 8000 | curl -fsS http://127.0.0.1:8001/healthz |
| minutes | 会议纪要 | 8002 | 8000 | curl -fsS http://127.0.0.1:8002/healthz |
| todo | 待办清单 | 8003 | 8000 | curl -fsS http://127.0.0.1:8003/healthz |

## 三、逐服务健康检查

```bash
curl -fsS http://127.0.0.1:8001/healthz   # asr
curl -fsS http://127.0.0.1:8002/healthz   # minutes
curl -fsS http://127.0.0.1:8003/healthz   # todo
```

## 四、管线接线（asr → minutes）

asr 的输出目录 ASR_OUTPUT_DIR 与 minutes 的输入目录 MINUTES_INPUT_DIR 指向同一
宿主目录（默认 ./data/asr-out）：asr 完成识别后，转写结果直接落入该目录，作为
minutes 会议纪要服务的输入。调整时必须保持两侧同值（validate.py C5 把关）。

## 五、单位落地注意事项

- 镜像均为占位（placeholder/*）：落地前替换为单位镜像仓库地址，并同步修改 .env；
- 容器内统一监听 8000、健康路径 /healthz；宿主端口经 .env 的 *_PORT 调整；
- 数据目录默认位于部署目录下（./data/...），按单位磁盘规划调整并确保可写；
- .env 变量集须与 compose 引用集双向一致，请勿手工增删变量（validate.py C3）；
- 占位镜像不可拉取，`docker compose up` 前请先完成镜像替换或本地构建。
=======
# DEPLOY — asr-minutes-todo 部署包

> 由 `skillfactory/v5/assets/deploy-pack/oracle/gen_deploy.py` 生成。
> 服务: asr, minutes, todo。镜像名为占位符（`placeholder/*`），上线前在 `.env` 中替换为真实镜像。

## 前置条件

- Docker Engine ≥ 20.10 且带 compose v2 插件（`docker compose version` 可用）
- 端口 8001/8002/8003 未被占用（可在 `.env` 修改）

## 部署三步（三条命令）

```bash
# 1) 复制并按需修改环境变量（Linux/macOS/Git Bash）
cp .env.example .env
#    Windows PowerShell 等价: Copy-Item .env.example .env

# 2) 启动服务
docker compose up -d

# 3) 健康检查：先看容器健康状态，再逐服务探测 /healthz
docker compose ps
curl -fsS http://localhost:8001/healthz   # asr
curl -fsS http://localhost:8002/healthz   # minutes
curl -fsS http://localhost:8003/healthz   # todo
```

三条命令执行完，`docker compose ps` 中各服务 STATUS 为 healthy、各 `/healthz` 返回 2xx，即部署成功。

## 服务与端口

| 服务 | 镜像（占位） | 宿主端口 | 健康检查 | 数据目录 |
|---|---|---|---|---|
| asr | `placeholder/asr:dev` | 8001 | `/healthz` | `ASR_INPUT_DIR` / `ASR_OUTPUT_DIR` |
| minutes | `placeholder/minutes:dev` | 8002 | `/healthz` | `MINUTES_INPUT_DIR` / `MINUTES_OUTPUT_DIR` |
| todo | `placeholder/todo:dev` | 8003 | `/healthz` | `TODO_DATA_DIR` |

## 管线接线

asr 的输出目录 `ASR_OUTPUT_DIR` 与 minutes 的输入目录 `MINUTES_INPUT_DIR` 指向同一路径（默认 `./data/asr-out`）：asr 把转写结果落盘，minutes 直接读同一目录。
两值必须一致；改动时同步修改 `.env` 中两行。

## 注意

- `.env.example` 中全部为占位值，不含任何真实凭据；接入真实服务时把 key 写进 `.env`（该文件不要提交版本库）。
- 占位镜像 `placeholder/*` 不可拉取，需替换为真实镜像后 `docker compose up -d` 才能成功。
- 数据目录由 bind mount 指定，容器首启会自动创建（相对路径基于 compose 文件所在目录）。
>>>>>>> 4f26eaab8cf326432c79fee06da6a9aae47b661e
