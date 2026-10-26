# TODO — AgentCraft（代理工坊）

> 進度唯一來源。每次對話查進度從此檔讀取，不從記憶體查。
> 任務說明請查 `docs/design/TASK.md`；UC 清單請查 `docs/design/SDD.md`；架構請查 `docs/design/ARCHITECTURE.md`。
> 格式：`[ ]` 待辦 / `[x]` 完成 / `[-]` 進行中
> 任務項目請附 UC 編號，例：`[ ] UC-ACT 3.1.1.1 K8s 環境與 CI/CD`

---

## 啟動前待辦（初始化遺留）

- [x] 團隊人數：PM/SA 1 人 + SD/PG 1 人（2026-10-24 使用者回覆）
- [ ] **決定 MVP1 範圍**：全範圍約 91 人天、2 人實際約 35–40 人天，11 月底不可行；選垂直切片（A）或延期（B），見 TASK.md「總量與時程對照」
- [ ] 向產品規劃團隊（Scottie）確認：回應時間目標、第 5 個產業、Orbit 非醫療業交付時程
- [ ] 向 Orbit 團隊取得 Digital Twin 介面資訊（MCP 端點、認證、sandbox 隔離與重設能力）
- [ ] 確認 Agent 執行位置（api 內嵌 vs Agent 平台團隊的 Pod）→ 寫成 ADR-001
- [x] Layer 7（Studio）已改列 MVP1
- [ ] 向產品規劃團隊確認「人次」定義（每次登入 / 每個情境練習 / 每次 Agent 對話？）與預期同時並行數，作為 Layer 6、8 壓測目標
- [x] 登入 POC 並截圖（2026-10-24，存於 `docs/design/poc-screenshots/`，索引與觀察見該資料夾 README）
- [ ] 取得 P6（Skill 編輯、換案驗證）與 P7 有成果狀態的截圖：POC 第一關已走到一半，被 Gemini 免費額度（每日 20 次）擋住；約 23 小時後恢復，或請使用者提供有額度的帳號 / 自行登入擷取
- [ ] **LLM 額度設計**：POC 免費方案每日 20 次即耗盡；MVP1 需付費額度、供應商端 429 的繁中處理與排隊重試、與應用層每人每日限額分開設計（接 Gemini API 資料）
- [ ] 回應時間目標：POC 實測 Agent 出方案超過 10 分鐘，需向產品規劃團隊定義目標並確認是否為 POC 限制
- [ ] 後台規劃納入 TASK.md / SDD.md UC（依 `docs/specs/SITEMAP.md` §3，待確認 MVP2 範圍）
- [ ] Layer 1 Schema 預留：org_id、Seat / 角色、LLM 呼叫 token 計量、稽核 log 表、情境版本（見 SITEMAP §3.7）
- [x] 登入 token 規則已定：一次性、10 分鐘、僅首次需邀請碼、outbox + job 每分鐘寄送（見 ADR-003 草稿）
- [x] 登入 token 為連結
- [ ] 登入 token 剩餘細節：發信 job / 發信 API 細節（使用者之後提供）；ADR-003 的 6 項建議是否採納（token 雜湊、寄後清內文、flag 狀態、SKIP LOCKED、防帳號列舉、輪詢間隔）
- [ ] LLM 串接資料（使用者之後提供）：Gemini API 是否經 AI Gateway、API Key、模型與用量（ADR-004）
- [ ] ADR-005（對話上下文）待確認：思考簽章處理以實際 API 驗證、用 POC 紀錄估算對話輪數與工具結果大小以決定摘要是否進 MVP1；Layer 4 開始時展開細項
- [x] 使用教學範圍已定：M1 靜態教學頁 + 首次互動導覽，動畫 M2；內容由產品規劃團隊提供（待取得文字）
- [x] 打包部署（K8s、CI/CD、容器化、NAS 掛載，UC 3.1.1.1）**最後處理**（使用者 2026-10-24），已移到 Layer 8 之後
- [x] 決定：MVP1 要有前後台畫面，至少 50 人同時使用（使用者 2026-10-24）；已寫入 `docs/design/MVP1-SCOPE.md`
- [x] 決定（使用者 2026-10-24）：POC 上有的功能 MVP1 全做（含 Studio）、先不管人力、300 人試用放雲端、最後一週才部署、後台只有 admin（密碼開發期固定）
- [ ] **部署週必查**：admin 密碼改為強密碼（由環境變數提供）、後台來源限制與登入限流、程式與 git 內無明文密碼
- [ ] 確認 MVP1-SCOPE §5：「50 人」是否同時 50 人、MVP1 開放哪些情境、雲端環境（供應商、網域、HTTPS、NAS）、Studio 的 LLM 用量限制
- [ ] **請確認**前台 Template（`web/template/index.html`）與 Site Map（`docs/specs/sitemap.html`）：頁面、區塊順序、素材位置、後台階段、待確認清單
- [ ] 確認 MVP1 300 人試用是在本機還是雲端（影響最後部署是否一定在 11 月底前完成）
- [ ] 確認情境視覺素材（U-11）：素材由誰製作、版權與 AI 生成規範；向基礎設施團隊確認 NAS 掛載方式（協定、ReadWriteMany、備份）與是否有 CDN；MVP1 只做封面 + 橫幅 + 產業預設圖是否可接受
- [ ] 把 `docs/specs/templates/SCENARIO-TASKCARD-TEMPLATE.md` 交給產品規劃團隊試填一個情境，收集格式回饋；確認 Orbit 任務卡格式（SCENARIO-INTAKE §6 S-1～S-6）
- [ ] 確認「約 60 種情境」的真實狀態：POC 站台目前只開 3 個（醫療 2、製造 1），zip 內有 4 個情境包；60 是 PRD 的 11 月目標，且依賴 Orbit 提供模擬系統與任務卡。誰把任務卡轉成情境包（PRD 指平台工程師，是否就是我方）
- [ ] 與產品規劃團隊對齊 `docs/specs/UX-GUIDELINES.md` §6 的 Q-1～Q-6；Layer 4 設計 SSE 事件時納入 §4 的事件類型
- [ ] 確認動態情境管理在 MVP1 的形式：API/CLI 或最小管理畫面（畫面 +3 天）；情境包改存 DB 並有版本（Layer 1 Schema 預留）
- [ ] 確認 TASK.md 工時是否以「人工開發」或「AI 輔助開發」為基準，並於 Layer 1 驗收後用實際值校準
- [x] 建立第一個本地 commit（2026-10-24 checkpoint）
- [ ] push 到 `https://github.com/Blackjtsai/AgentCraft.git`（待使用者核准；需 GitHub 認證）

- [ ] **TASK／SITEMAP 一致性修正**（2026-10-26 code review 發現，屬他次對話產物，需使用者確認後改）：(1) TASK Layer 1–6 小計約 88 與各 Layer 增減不符（約 93？），TODO 另寫約 91；(2) Layer 4 的 UC 4.2.1／4.2.2 驗收與估算仍寫「經 Gateway」，與 Gemini API 決定衝突；(3) UC 3.2.1／3.3.1.3 驗收仍寫三種登入方式，MVP1 只有 email 連結；(4) SITEMAP §3.6 M1 後台列同時保留「無畫面 CLI」舊文，Y6、Y9 階段仍寫 M2／取代 CLI，與 A0–A4 衝突；(5) Layer 3 動態情境 API 與 Layer 6 後台畫面（3.2.9.3）的相依與 +3 天畫面估算可能重複計算；(6) 開發期 admin 密碼預設值的存放位置寫進 SETUP／CLAUDE.md（`.env` 不進版控、`.env.example` 空值、未設定則拒絕啟動）

## 回推 PRD（以 POC 與會議資訊先回推，之後與產品規劃師的 PRD 比較）

> 2026-10-26 決定：只依 POC 畫面與會議資訊回推，**不讀** `需求/AIP_Education-main/` 與我方 SITEMAP／POC-ANALYSIS（盲測，比較才有意義）。工具：`~/Documents/tai-builder-prd`（`/tai-prd-gen-v2`）；輸入在其 `docs/prd-requests/案件工作台/`。

- [-] 以 `tai-builder-prd` 產出「案件工作台」PRD 草稿（`--mode draft`；輸入含截圖、背景、觀察紀錄、我的決定與立場）；產出在其 `docs/prd-output/案件工作台/`
- [ ] 逐張核對觀察紀錄中未標 ★ 的截圖標註（已核對：24、28、30 兩張、33、34、35）；36 與 11–23 其餘待核
- [ ] 確認 `我的決定與立場.md` 第六節各規則的來源（我的決定，或來自產品規劃團隊文件）
- [ ] PRD 產出後複製到 `docs/design/prd-reverse/`（標「回推版，未經確認」），並整理待確認問題（Q）作為會議提問清單
- [ ] 取得產品規劃師的 PRD 後，比較：文件結構與粒度、業務規則與狀態、我方 Q 是否已有答案
- [ ] 決定其餘功能（登入註冊、我的學習、探索與情境選擇、Skill、我的成果、情境製作、共用機制、後台 4 份）是否也用此工具回推（前台 7 + 共用 1 + 後台 4，約 12 份；後台無 POC 依據屬我方提案）
- [ ] 決定是否把 `tai-builder-prd` 工具包提供給產品規劃師作為雙方會議的共同格式（可用 Web 版 prompt；後台可能之後用 TAI-BUILDER 開發）

## Layer 1：基礎建設與資料層

> 細項待 Layer 開始前依 TASK.md 展開。

## Layer 2：身分與帳號

## Layer 3：情境包與 Digital Twin 串接

## Layer 4：Agent、完成判定與學習紀錄

## Layer 5：學員練習 Web（P1–P7）

## Layer 6：安全、營運與用量

## Layer 7：Scenario Studio（MVP2，待確認）

## Layer 8：端對端整合測試
