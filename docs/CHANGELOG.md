# CHANGELOG — AgentCraft（代理工坊）

## 2026-10-24 專案初始化與需求盤點

- **初始化**：以 `/new-project-init` 完整模式建立骨架（CLAUDE.md、docs/、五個 workload blueprint、checkpoint / checkservice、convention 檢查、測試樣板）；`git init` 並綁定 `https://github.com/Blackjtsai/AgentCraft.git`。系統代號 ACT，DB `db_act_dev`，K8s 上雲，技術棧 Next.js + FastAPI + PostgreSQL + Redis。
- **需求盤點**：讀 `需求/文檔.md`、`17.png`、簡報封面與章節頁；POC repo（zip）讀了 README、設定、PRD 00 與 PLAN、Sitemap IA v3、Org/Seat/Role/Credits 提案；ARCHITECTURE、SCORING_RULES、程式碼與情境包內容**尚未細讀**。
- **Layer 切法**：8 個 Layer（基礎建設、身分、情境包與 Twin、Agent 與判定、學員 Web、安全營運、Studio、E2E）；Studio 暫排 MVP2。
- **工時估算**：以通用分級（人工開發基準，未計 AI 輔助）估 MVP1 約 88 人天（SSO 移 MVP2 後），需約 4 人並行；團隊人數待確認。
- **Site Map**：`docs/specs/SITEMAP.md`，前台 P1–P7 + Studio，後台依 POC 提案分 Org 後台（O1–O6）與系統後台（Y1–Y9）；後台 MVP1 以 CLI 代替。
- **POC 站台體驗**：登入並截圖 28 張（`docs/design/poc-screenshots/`）。觀察：方案確認卡為 P5 核心；Agent 出方案超過 10 分鐘；Studio 外洩 `ModelHTTPError`；手機、平板無橫向捲動。P6 與有成果的 P7 因需完成第一關，尚未取得。
- **決策與更新**：MVP3 目標改為 2027/05 正式上線、年底累計 10 萬人次（非 10 萬人）；**MVP1 登入流程：邀請碼 + email 驗證 → 寄 token 到信箱登入，SSO 後移 MVP2**（token 形式、有效期等待確認）。
- **誤判與修正**：(1) 先前說「讀過 POC」，實際只讀一部分，已在 POC-ANALYSIS 列明已讀 / 未讀；(2) 92 人天未註明是人工開發基準，已補說明並列入 TODO；(3) 初版後台只有 8 頁，讀完 Org 提案後改寫。
- **安全**：`需求/文檔.md` 含 POC 帳密，已與 `*.pptx`、`*.zip` 一併列入 `.gitignore`。

## 2026-10-26 網站地圖圖庫與回推 PRD 準備

- **網站地圖圖庫**：以 `diagram-design` skill（已安裝到 `~/.claude/skills/`）產出 `docs/design/diagram-gallery/`：前後台網站地圖第一層（前台、後台上下兩區塊；登入與註冊拆成兩個方塊）、前台第二層、後台第二層、POC 網站地圖、後台 MVP1 A0–A4 版，加 `index.html` 導覽首頁。
- **後台需求來源釐清**：Y1–Y9、O1–O6 來自 POC 提案（討論版，階段未定案）；Y6 情境管理 M1 起需要是使用者決定；A0–A4 來自 `MVP1-SCOPE.md`。第一層後台區塊畫的是 Y/O，未含 A0–A4（使用者決定不補）。
- **回推 PRD 準備**：使用者要先依 POC 與會議資訊自行回推 PRD，再與產品規劃師的 PRD 比較。決定用 `~/Documents/tai-builder-prd`（`/tai-prd-gen-v2 --mode draft`）；輸入資料放其 `docs/prd-requests/案件工作台/`（25 張截圖、背景、觀察紀錄、我的決定與立場）；盲測，不讀 `需求/AIP_Education-main/` 與既有 SITEMAP／POC-ANALYSIS。
- **誤判與修正**：觀察紀錄的截圖對照表依檔名與舊索引寫成，未逐張看圖，24（實為 Agent 執行中）、34（實為 429 錯誤）標錯，情境事件實為 `30-p5-after-run1`；由 tai-builder-prd 那邊的對話逐張看圖發現。已重看並更正觀察紀錄與 `poc-screenshots/README.md`，寫入 feedback memory。
- **版控防線**：`需求/AIP_Education-main/`（產品規劃團隊私有 repo 解壓縮內容）與 `docs/meetings/**/*.pptx` 加入 `.gitignore`；先前未列入，會被 commit。
- **同批 commit 的他次對話產物**（本次對話未參與，僅隨 checkpoint 一併提交）：`MVP1-SCOPE.md`、ADR-003／005、`UX-GUIDELINES.md`、`SCENARIO-INTAKE.md`、`sitemap.html`、`specs/templates/`、`web/template/`、`nas/`、`docs/meetings/`，及 CLAUDE.md、TASK、SDD、SITEMAP 等既有文件的修改。


## 2026-10-26 Agent 對話上下文設計（ADR-005）

- **討論結論**：Gemini `generateContent` 無狀態，SDK chat 只把歷史存在記憶體；隱式 / 明確快取只降低成本，不是記憶；Gemini 的 response id 不用於接續對話。決定自建紀錄表，每次依 `case_id` 組裝上下文。
- **設計**：`act_agent_request`（一次 LLM 呼叫一列，`request_id` 做冪等）與 `act_agent_turn`（歷史一則一列，不可變，存 Gemini 原始 parts）；同案件同時只允許一個進行中呼叫；摘要為新增一列、不刪舊列；MVP1 全量重播歷史並只做隱式快取（固定前綴在前）。
- **文件**：新增 `ADR-005-agent-conversation-context.md`（草稿）；TASK.md Layer 4 新增驗收條件與 2 天估算（合計 23.5 天）；SDD 待決 ADR 清單補入 ADR-005。
- **誤判與修正**：先把這份 ADR 編為 ADR-004，之後才發現 SDD.md 與 TODO.md 已把 ADR-004 預留給「LLM 供應商與 Gateway」，改為 ADR-005。寫入 feedback memory。
- **待確認**：Gemini 多輪 function calling 的思考簽章處理（Layer 4 以實際 API 驗證）、單次練習的對話輪數與工具結果大小（決定摘要是否進 MVP1）、是否經 AI Gateway。
