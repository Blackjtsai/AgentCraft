# Blueprint — 異質系統串接（UC-ACT 4.x）

> 版本：v0.2 ／ 最後更新：2026-10-24

## 技術棧

| 層 | 技術 |
| -- | ---- |
| 框架 | 各外部系統一個 client 模組（結構於各 Layer 開始前補入） |
| 語言 | Python 3.12 |
| 其他 | MCP client、OAuth、HTTP |

## 目錄結構

```
external/
├── [待實作後補充]
```

## 對外介面

| 外部系統 | UC | 提供團隊 | 用途 |
| -------- | -- | -------- | ---- |
| Orbit Digital Twin | 4.1 | Orbit | 模擬系統與資料，Agent 透過 MCP 呼叫 |
| LLM：Gemini API（是否經 AI Gateway 待確認） | 4.2 | Google / AI 大腦團隊 | LLM 推論 |
| 發信 API（MVP1，SMTP 暫不處理）、Google / Microsoft SSO（MVP2） | 4.3 | 外部服務 / 資安治理 | 登入 token 寄信（由 job 呼叫）；SSO 登入 |

## 當前 Layer 狀態

| Layer | UC 範圍 | 狀態 |
| ----- | ------- | ---- |
| 2 | 4.3.3 寄信（MVP1）；4.3.1–4.3.2 SSO 移 MVP2 | ⏳ |
| 3 | 4.1 | ⏳ |
| 4 | 4.2 | ⏳ |

## 關鍵業務約束

- Digital Twin 介面由 Orbit 提供，不是我方能自行更換；目前只有醫療業
- LLM 使用 Gemini API；是否經 AI Gateway 待確認
- 每個外部呼叫必須處理逾時、連線失敗、5xx 三種 sibling 失敗，且對使用者只顯示繁體中文訊息
- 認證失敗（401/403）立即放棄，不重試
