# 系統設計說明書（SDD）— AgentCraft（代理工坊）

> 版本：v0.1 / 建立日期：2026-10-24

## 1. 系統概述

人才培育網站（代號 ACT）。學員在模擬企業情境中指揮 AI Agent 解題（第一關），把解法寫成 Skill（第二關），再以新案例換案驗證。我方為前台平台團隊，負責 product 層級系統；Agent 平台、MCP 整合、AI 大腦（AI Gateway）、模擬系統（Orbit Digital Twin）由他團隊提供。

需求來源與盤點：`需求/文檔.md`、`需求/17.png`、`需求/主權AI_ Eason.pptx`、`docs/design/POC-ANALYSIS.md`。

## 2. UC 清單

> UC 編號格式：`UC-ACT {大類}.{第一層}.{第二層}.{第三層}`
> 此清單依需求自動展開，開發過程中持續維護。P1–P7 為 POC 產品規劃的頁面編號。

| UC 編號 | 名稱 | API / 元件 | 負責人 | 狀態 |
| ------- | ---- | ---------- | ------ | ---- |
| UC-ACT 3.1 | 基礎建設 | — | — | ⏳ |
| UC-ACT 3.1.1 | 環境架構 | K8s / PostgreSQL / Redis | — | ⏳ |
| UC-ACT 3.1.1.1 | K8s 環境與 CI/CD | — | — | ⏳ |
| UC-ACT 3.1.1.2 | PostgreSQL 與 Redis 佈署 | — | — | ⏳ |
| UC-ACT 3.1.1.3 | 組態與機密管理 | — | — | ⏳ |
| UC-ACT 3.1.2 | 資料層 | PostgreSQL | — | ⏳ |
| UC-ACT 3.1.2.1 | 核心 Schema（含組織歸屬） | — | — | ⏳ |
| UC-ACT 3.1.2.2 | Migration 工具與標準 8 欄 | — | — | ⏳ |
| UC-ACT 3.2 | WEB | web/ | — | ⏳ |
| UC-ACT 3.2.1 | P1 註冊 / 登入 | — | — | ⏳ |
| UC-ACT 3.2.2 | P2 我的學習 | — | — | ⏳ |
| UC-ACT 3.2.3 | P3 探索產業 / P4 情境選擇 | — | — | ⏳ |
| UC-ACT 3.2.4 | P5 案件工作台（第一關） | — | — | ⏳ |
| UC-ACT 3.2.5 | P6 撰寫並驗證 Skill（第二關） | — | — | ⏳ |
| UC-ACT 3.2.6 | P7 我的成果 | — | — | ⏳ |
| UC-ACT 3.2.7 | Studio 情境製作頁 | — | — | ⏳ |
| UC-ACT 3.2.8 | 共用：Design System、響應式、繁中、**使用教學頁與首次互動導覽** | — | — | ⏳ |
| UC-ACT 3.2.9 | MVP1 管理後台畫面（A0 殼與登入、A1 帳號與邀請碼、A2 情境管理、A3 用量與紀錄、A4 稽核） | web/（admin） | — | ⏳ |
| UC-ACT 3.3 | API | api/ | — | ⏳ |
| UC-ACT 3.3.1 | 身分（MVP1：邀請碼 + email token 登入、Session；SSO 與同 email 合併於 MVP2） | — | — | ⏳ |
| UC-ACT 3.3.2 | 產業與情境查詢 | — | — | ⏳ |
| UC-ACT 3.3.3 | 案件與對話（SSE 串流、方案確認、停止、重設本案） | — | — | ⏳ |
| UC-ACT 3.3.4 | Skill（建立、版本、啟用、AI 起草） | — | — | ⏳ |
| UC-ACT 3.3.5 | 學習狀態與成果 | — | — | ⏳ |
| UC-ACT 3.3.6 | Studio | — | — | ⏳ |
| UC-ACT 3.3.7 | 每人每日用量限制 | — | — | ⏳ |
| UC-ACT 3.4 | Backend | backend/ | — | ⏳ |
| UC-ACT 3.4.1 | 平台工程師 CLI（邀請碼、用量上限、demo 帳號） | — | — | ⏳ |
| UC-ACT 3.4.2 | 情境包（規格、載入、上線前檢查、**後台動態管理與版本**） | — | — | ⏳ |
| UC-ACT 3.4.3 | Agent 執行（對話、方案確認、Skill 注入、工具限制） | — | — | ⏳ |
| UC-ACT 3.4.4 | 完成判定與 AI 初評 | — | — | ⏳ |
| UC-ACT 3.5 | JOB | job/ | — | ⏳ |
| UC-ACT 3.5.1 | 換案測試非同步執行 | — | — | ⏳ |
| UC-ACT 3.5.2 | 用量彙總與每日重置 | — | — | ⏳ |
| UC-ACT 3.5.3 | AI 初評非同步執行 | — | — | ⏳ |
| UC-ACT 3.5.4 | 情境上線前檢查批次（Studio） | — | — | ⏳ |
| UC-ACT 3.4.2.4 | 情境視覺素材（上傳、驗證、版本、預設圖） | — | — | ⏳ |
| UC-ACT 3.5.5 | 郵件寄送 job（outbox，每分鐘撈未發送） | — | — | ⏳ |
| UC-ACT 4.1 | 異質系統：Orbit Digital Twin | external/ | — | ⏳ |
| UC-ACT 4.1.1 | MCP 連線與認證 | — | — | ⏳ |
| UC-ACT 4.1.2 | sandbox 隔離與重設 | — | — | ⏳ |
| UC-ACT 4.1.3 | 斷線 / 變慢降級 | — | — | ⏳ |
| UC-ACT 4.2 | 異質系統：LLM（Gemini API；是否經 AI Gateway 待確認） | external/ | — | ⏳ |
| UC-ACT 4.2.1 | LLM 呼叫封裝 | — | — | ⏳ |
| UC-ACT 4.2.2 | 逾時、5xx、限流處理 | — | — | ⏳ |
| UC-ACT 4.3 | 異質系統：身分與寄信 | external/ | — | ⏳ |
| UC-ACT 4.3.1 | Google SSO（MVP2） | — | — | ⏸ |
| UC-ACT 4.3.2 | Microsoft SSO（MVP2） | — | — | ⏸ |
| UC-ACT 4.3.3 | 發信 API client（SMTP 暫不處理） | — | — | ⏳ |
| UC-ACT 5.1 | 營運：日誌、指標、告警 | — | — | ⏳ |
| UC-ACT 5.2 | 端對端與壓力測試 | — | — | ⏳ |

## 3. 架構決策

見 `docs/decisions/`。待決：ADR-001 Agent 執行位置、ADR-002 Job 佇列套件、ADR-003 MVP1 登入 token 與郵件 outbox（草稿，見 `docs/decisions/ADR-003-mvp1-login-token-and-mail-outbox.md`）、ADR-004 LLM 供應商與 Gateway、ADR-005 Agent 對話上下文由自建紀錄表組裝（草稿，見 `docs/decisions/ADR-005-agent-conversation-context.md`）。

## 4. API 規格

[待實作後補充]

## 5. 資料 Schema

[待 DDL 確認後補充]

## 版本記錄

| 版本 | 日期 | 摘要 |
| ---- | ---- | ---- |
| v0.1 | 2026-10-24 | 初始建立，依需求展開 UC 清單 |
| v0.2 | 2026-10-24 | MVP1 登入改為邀請碼 + email token；UC 4.3.1、4.3.2（SSO）移 MVP2；3.3.1 描述同步 |
| v0.4 | 2026-10-24 | 新增 UC 3.2.9 MVP1 管理後台畫面（使用者決定 MVP1 要有後台畫面，不以 CLI 代替） |
| v0.3 | 2026-10-24 | 新增 UC 3.5.5 郵件寄送 job；3.4.2 納入後台動態情境管理；4.2 改為 Gemini API；4.3.3 改為發信 API client |
