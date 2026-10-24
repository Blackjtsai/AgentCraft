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
