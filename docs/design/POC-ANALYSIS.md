# POC 盤點 — AIP_Education（產品規劃團隊）

> 盤點日期：2026-10-24。來源：`需求/AIP_Education-main.zip`（`scottie-twm/AIP_Education`，私有 repo）。
> **本文件只記錄已讀到的內容。** 已讀：`README.md`、`pyproject.toml`、`.env.example`、`frontend/package.json`、`scenarios/industries.yaml`、`docs/prd/00_OVERVIEW.md`、`docs/prd/PRD_PLAN.md` 前半、`docs/AIP_Education_Sitemap_IA_v3.md` 全文、`docs/proposals/AIP_Education_Org_Seat_Role_Credits_Proposal.md` 全文（後台管理機制）。檔案清單已掃過，其餘檔案（含 `ARCHITECTURE.md` 60KB、`SCORING_RULES.md`、`DECISIONS.md`、Studio 文件、各情境包內容、程式碼）**尚未細讀**。
>
> **線上站台**：`https://aip-education.zeabur.app/` 已於 2026-10-24 登入體驗並截圖，約 28 張存於 `poc-screenshots/`（索引、觀察與未取得的畫面見 `poc-screenshots/README.md`）。已走過登入、P2、P3、P4、P5（含 Agent 對話至方案確認）、P7 空狀態、Studio；**P6（Skill）與有成果的 P7 尚未取得**，因需完成第一關。

## 1. 它是什麼

TAIONE「Agentic AI 人才培育網站」的 MVP1（POC）。學員在模擬企業情境指揮 Starter Agent 處理案件；第一關對話完成案件並提交報告，第二關把做法寫成 Skill 並以兩個新案件驗證。Agent 操作的系統與資料都是模擬的。

## 2. 提供什麼

| 項目 | 內容 |
| ---- | ---- |
| 情境包 | 4 個實際情境：med-01 門診異動、med-02 出院準備、med-03 護理交班、mfg-01 射出成型品質異常；另有 studio-example |
| 情境包結構 | `scenario.yaml`、`agent.yaml`、`judge.yaml`、`policies.yaml`、`skill.yaml`、`task_card*.md`、`systems/*.yaml`（模擬系統定義）、`cases/{original,general,exception}.json`、`handlers.py` |
| 模擬系統引擎 | `simulator/`，對外提供 MCP 端點；POC 自建，**production 改由 Orbit Digital Twin 提供** |
| 後端 | FastAPI；登入（邀請碼 + 暱稱）、學習紀錄、Skill、判定、每日用量、Studio |
| Agent | Pydantic AI + Gemini；Starter Agent 與 Studio 用不同模型 |
| 前端 | React 19 + Vite；頁面含 Welcome / Learning / Chat / TaskPanel / SystemsPanel / SkillPage / SwapTests / ResultsPage / StudioPage / Guides |
| 產業 | 醫療、製造、金融、零售（POC 時）、企業共通；目前只有醫療與製造有情境 |
| 測試 | pytest 回歸（每情境原案 / 換案）、Playwright e2e（含 sign-in、guides、scenario） |
| 文件 | PRD 00 總覽已寫；PRD_PLAN 規劃 01–13、20、21、30 共 15 份（**其餘尚未寫**）；另有 Sitemap IA v3、Design System HTML、Studio 指南、評分規則、Org/Seat/Credits 提案 |

## 3. 對我們最重要的結論

1. **PRD 的定位就是交給 RD 重做 production**，技術可換（PRD_PLAN §2 第 1 點）。我方不繼承 POC 技術棧，繼承的是**行為與需求**。
2. **不能換的只有與 Digital Twin 的介面**（Orbit 提供，MCP）。
3. **production 從零開始**：不搬 POC 帳號與資料；帳號改 **email**（magic link、Google、Microsoft SSO），首次註冊要邀請碼與顯示名稱。
4. **前台要預留、不實作**：組織歸屬、Playground、課程等級。下一階段才做：Playground、Level 2、後台管理、個資刪除、Studio 發布、個人檔案頁。
5. **規模目標**：PRD 寫 11 月約 60 個情境、5 個產業；至少 50 人同時使用。Orbit 目前只有醫療業，其他產業要等 Orbit。
6. **POC 已出現的風險訊號**：Studio 的 LLM 呼叫曾拋 `ModelHTTPError`；POC 為單容器部署（Cloud Run / Zeabur），與我們 K8s 多 workload 架構不同。

## 4. 未決事項（PRD 標「遇到先問 Scottie」）

- 回應時間目標
- 第 5 個產業（零售業 10/23 先拿掉）
- Orbit 非醫療業模擬系統與情境的交付時程
- Orbit Digital Twin 介面細節（要問 Orbit 團隊與 Architect）

## 5. 與我們 Layer 的對應

| POC / PRD 切片 | 我方 Layer |
| -------------- | ---------- |
| 1 底層：01 身分、02 情境包、03 Twin 串接 | Layer 1–3 |
| 2 Agent 與判定：04–07 | Layer 4、6 |
| 3 學員練習：10、20、21 | Layer 5、8 |
| 4 Studio：11 | Layer 7 |

## 6. 建議後續

- 細讀 `docs/ARCHITECTURE.md`、`Sitemap_IA_v3.md`（頁面與狀態規格，Layer 5 的主要依據）、`SCORING_RULES.md`（Layer 4 判定）
- PRD 01–13 寫出後，與 TASK.md 逐條對照，補驗收條件
- 未經使用者同意，不使用 POC 站台的 demo 帳密登入操作
