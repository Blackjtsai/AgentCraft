# SETUP — AgentCraft（代理工坊）

> 環境部署清單，逐項確認就緒。就緒 ✅ / 未完成 ❌
> **初期在本機執行**（使用者 2026-10-24）；kubectl、K8s 叢集、NAS 掛載等上雲項目延後。
> 狀態欄為初始化時的預設，請於 Layer 1 開始前實際檢查並更新。

## 環境工具

| 項目 | 版本需求 | 安裝指令 | 狀態 |
| ---- | -------- | -------- | ---- |
| git | 任意 | — | ✅（已 `git init`，remote 已綁定） |
| uv | 最新 | `brew install uv` | ❌ 待檢查 |
| Python | 3.12（由 uv 管理） | `uv python install 3.12` | ❌ 待檢查 |
| Node.js | LTS（20+） | `brew install node` | ❌ 待檢查 |
| PostgreSQL | 16 | `brew install postgresql@16` | ❌ 待檢查 |
| Redis | 7+ | `brew install redis` | ❌ 待檢查 |
| kubectl | 對應叢集版本 | `brew install kubectl` | ❌ 待檢查 |
| Docker | 最新 | Docker Desktop | ❌ 待檢查 |
| pre-commit | 最新 | `brew install pre-commit` | ❌ 待檢查 |

## 外部資源

| 項目 | 取得方式 | 狀態 |
| ---- | -------- | ---- |
| Orbit Digital Twin 連線資訊 | 向 Orbit 團隊索取 | ❌ 待取得 |
| AI Gateway 端點與金鑰 | 向 AI 大腦團隊索取 | ❌ 待取得 |
| Google OAuth Client（MVP2） | 向資安治理團隊 / 雲端主控台申請 | ⏸ 延後 |
| Microsoft OAuth Client（MVP2） | 同上 | ⏸ 延後 |
| 發信 API（登入 token，MVP1 必要；SMTP 暫不處理） | 待定 | ❌ 待定 |
| Gemini API Key | Google AI Studio / 公司帳號 | ❌ 待取得 |
| K8s 叢集與 namespace | 向基礎設施團隊申請 | ❌ 待申請 |
| NAS 掛載（協定、路徑、容量、備份、ReadWriteMany） | 向基礎設施團隊確認；本機規約見 `nas/README.md` | ❌ 待確認 |

## 安裝步驟

[待 Layer 1 確認專案結構後補充]

## 服務啟動

本機開發服務：PostgreSQL、Redis、api、web、job。檢查請執行 `/checkservice`。

```sh
brew services run postgresql@16
brew services run redis
createdb db_act_dev
createdb db_act_test
pre-commit install
```
