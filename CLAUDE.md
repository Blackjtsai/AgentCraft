# AgentCraft（代理工坊）— 專案規範 (CLAUDE.md)

---

# 一、通用規範

## Claude 行為規範（Karpathy Coding Guidelines）

- **Think Before Coding**：有假設或模糊地帶，先說出來對齊，不要默默實作
- **Simplicity First**：只寫解決當前問題最少的程式碼，不預留「未來可能用到」的抽象
- **Surgical Changes**：只動必要的地方，不順手重構周邊不相關的程式碼
- **Goal-Driven Execution**：每個任務完成前，先定義可驗證的成功標準，達到才繼續

> 已有個人全域規範者以全域版為準，內容一致。

## 不問已知規範

有合理預設答案時直接執行，不問。只有在真正有歧義且無法從上下文推斷時才提問。

## 文件資料夾管理規範

- `docs/design/` — 設計類（需求、SDD、架構等規劃文件）
- `docs/specs/` — 規格類（API 規格、服務說明書、流程圖等衍生文件）
- `需求/` — 需求來源（原始需求文件、簡報、POC 原始碼壓縮檔）。**此專案沿用 `需求/` 而非 `docs/requirements/`**，不自行搬動
- **滾動式調整**：資料夾結構不清楚時，自動提醒使用者討論調整，不自行亂動

### 為什麼不用單一 CONTEXT.md

「專案 context」刻意依讀者情境拆分到不同文件（`ARCHITECTURE.md` 現況、ADR 決策原因、`TODO.md` 進度、`TASK.md` 驗收條件、`CHANGELOG.md` 歷史軌跡），而非集中成一份 CONTEXT.md——好處是各司其職、邊界清楚，代價是抓全貌要讀多份，靠下方「專案開場問候規範」的固定組裝順序補回。此為 **BlackJ-Tsai 工作流** 的核心精神。

## 檔案異動盤查規範

資料夾或檔案位置變動時，主動盤查：Import 路徑、設定檔引用、CLAUDE.md 目錄結構區塊、測試路徑。
異動影響超過 1 個檔案時，先列受影響清單讓使用者確認，再動手。

## 自動記憶規範

- **錯誤經驗**：對話中發生錯誤或誤判，立即寫入專案 memory 目錄，類型 `feedback`
- **系統藍圖**：實作新模組前，必須先產出或更新 `docs/design/ARCHITECTURE.md` 的 Mermaid 架構圖
- **經驗性討論**：對話中出現架構取捨、設計決策分析類的討論（不論當下是否已有明確結論），該段落告一段落時主動詢問是否保存。屬於既有決策的延伸理由，優先補寫進對應的 ADR / 設計文件；屬於新的討論脈絡，寫入專案 memory
- **通用規範升級**：若某項設計決策判斷不限於本專案、具通用性，主動詢問是否同步更新到全域規範

## Todo 管理規範

- **唯一來源**：進度以 `docs/TODO.md` 為準，不以記憶體或 TodoWrite 工具為準
- 每個 Layer 開始前，先在 `docs/design/TASK.md` 列出驗收條件與工時估算，再在 `docs/TODO.md` 展開細項，再動手
- **TASK.md gate**：`docs/TODO.md` 出現新 Layer，但 `docs/design/TASK.md` 無對應條目或無工時估算 → 停下來，先依 `docs/design/ESTIMATION-TEMPLATE.md` 的複雜度分級補寫，使用者確認後才繼續
- 每完成一項，立即更新 `docs/TODO.md`（`[ ]` → `[x]`），不批次更新
- 上一 Layer 所有項目 `[x]` 才能開新 Layer
- TodoWrite 工具只用於當前對話同步顯示，以 `docs/TODO.md` 為準

## 專案開場問候規範

使用者輸入 `hi` / `Hi` / `HI` 時，依序執行：

0. **環境檢查** — 讀取 `docs/SETUP.md`，逐項列出就緒 ✅ / 未完成 ❌
1. **打招呼** — 問候使用者，開頭加一行標籤：「（本專案採用 BlackJ-Tsai 工作流）」
2. **專案任務說明** — 一段話說明此專案的目的與階段
3. **Claude 技能清單** — 列出目前可執行的任務，固定包含：
   - `/checkpoint` — 每次對話結束前執行（commit + push + 累積開發經驗）
   - `/checkservice` — 確認服務就緒
4. **目前進度** — 讀取 `docs/TODO.md`，對照 `docs/design/ARCHITECTURE.md` 的 Layer 驗收表
5. **可對外服務** — 說明哪些端點 / 功能目前已可使用

## 程式碼註解規範

每支程式碼檔案（空白佔位檔除外）都必須包含以下兩層：

**1. 檔案 header（最頂端）**

```
# ============================================================
# 檔案名稱：xxx.py（或對應副檔名）
# 中文名稱：（繁體中文說明）
# 功能說明：（一行說清楚此檔的職責）
# 所屬模組：（對應的模組或資料夾）
# 建立日期：YYYY-MM-DD
# 修改日期：YYYY-MM-DD
# 開發者　：（開發者名稱）
# ============================================================
```

**2. 每個函式 / 方法的 docstring / 說明**

- 一行說明「做什麼、回傳什麼、特殊條件」
- 測試函式說明測試情境與預期結果
- 新增檔案時 header 與 docstring 同步建立；修改函式時同步更新 docstring 與 header 修改日期

## 測試規範（Error Path）

測試必須覆蓋「正確失敗」，不只「能動」。以下三條適用所有專案：

1. **驗收條件必須列 error path 預期行為**（成功 → 200；逾時 → 指定訊息不拋 exception；401/403 → 立即放棄不重試）
2. **每個 `except XxxError`，加一個 sibling exception 測試** — sibling 是同層而非父子，不測它會穿透
3. **monkeypatch 前自問「我是在測這個值，還是繞過它？」** — 若繞過，另加不 patch 的 case

## 資料表設計規範

### 命名規則

**資料表命名**：格式為 `{系統代號小寫}_{業務實體名稱}`（全小寫、底線分隔）
- 本專案系統代號：`ACT`，資料表前綴 `act_`
- 範例：`act_user`、`act_scenario`、`act_case`

**PK / FK 欄位命名**：去掉系統代號前綴，取業務實體名稱加欄位用途後綴
- PK（單一識別）：`{業務實體名稱}_id`
- FK（參照其他表）：`{被參照表業務實體名稱}_id`
- 代碼識別欄位：`{業務實體名稱}_code`

| 系統代號 | 資料表 | PK 欄位 |
| -------- | ------ | ------- |
| `ACT` | `act_user` | `user_id` |
| `ACT` | `act_scenario` | `scenario_code`（情境包代號，如 `med-01`） |

> 完整實體清單於 Layer 1（資料層）確認後補入。

### 標準 8 欄

每張主要業務資料表必須在業務欄位之後加入：

| 欄位 | 型別 | 預設 | 說明 |
| ---- | ---- | ---- | ---- |
| `note` | TEXT | — | 備註 |
| `is_delete` | CHAR(1) | `'N'` | 軟刪除，加 `CHECK (is_delete IN ('Y','N'))` |
| `create_user` | VARCHAR(100) | — | 建立人員 |
| `create_date` | TIMESTAMP | `NOW()` | 建立時間 |
| `create_ip` | VARCHAR(50) | — | 新增 IP |
| `update_user` | VARCHAR(100) | — | 更新人員 |
| `update_date` | TIMESTAMP | — | 異動時間 |
| `update_ip` | VARCHAR(50) | — | 異動 IP |

純 log 表：僅加 `create_*` 四欄。單純關聯表：可視情況省略。
命名慣例：`create_date` / `update_date`，不用 `created_at` / `updated_at`。

---

# 二、業務邏輯規範

## 專案快照

**AgentCraft（代理工坊，代號 ACT）**
人才培育網站：學員在模擬企業情境中指揮 AI Agent 解題，親手把解法打磨成可重複使用的 **Skill**，再用新案例驗證。我方團隊為**前台平台團隊**，負責 product 層級系統（對應 `需求/17.png` 的第 2 棒：Citizen Portal、SSO、Agent/MCP 選擇與設定、使用者 Workspace、UI/UX）。

里程碑：
- **MVP1**：2026/11 底，目標 300 人
- **MVP2**：2027/03 底，帶入其他功能
- **MVP3**：2027/05 正式版上線，到 2027/12 底累計 10 萬人次（非 10 萬同時在線；同時並行數待與產品規劃團隊確認）

參考文件：
- `需求/文檔.md` — 專案背景與團隊角色（**內含 POC 帳密，不得複製進任何 git 追蹤的檔案**）
- `docs/design/POC-ANALYSIS.md` — POC 內容盤點（產品規劃團隊的 AIP_Education）
- `docs/design/SDD.md` — 系統設計說明書與 UC 清單
- `docs/design/TASK.md` — 各 Layer 驗收條件與工時
- `docs/decisions/` — ADR

## 技術棧

| 層 | 技術 |
| -- | ---- |
| Web | Next.js + TypeScript（繁體中文單語系，桌機 / 平板直橫 / 手機四種尺寸） |
| API | Python 3.12 + FastAPI（uv 管理） |
| Backend | Python 領域服務（情境包、Agent 執行、完成判定）與平台工程師 CLI |
| Job | Python 背景 worker（以 Redis 為佇列；套件於 Layer 1 以 ADR 確認） |
| DB | PostgreSQL 16（DEV：`db_act_dev`） |
| Cache / Queue | Redis |
| 部署 | Kubernetes（雲端） |
| 外部 | Orbit Digital Twin（MCP）、AI Gateway（LLM）、Google / Microsoft SSO、Email |

## 必備技能

- `/checkpoint` — **必備**，每次對話結束前執行（commit + push + 累積開發經驗）
- `/checkservice` — 確認 web / api / job / PostgreSQL / Redis 就緒

## 實作順序（嚴格遵守，未驗收不動下一層）

| Layer | 名稱 | 里程碑 |
| ----- | ---- | ------ |
| 1 | 基礎建設與資料層 | MVP1 |
| 2 | 身分與帳號 | MVP1 |
| 3 | 情境包與 Digital Twin 串接 | MVP1 |
| 4 | Agent、完成判定與學習紀錄 | MVP1 |
| 5 | 學員練習 Web（P1–P7） | MVP1 |
| 6 | 安全、營運與用量 | MVP1 |
| 7 | Scenario Studio | MVP2（待確認） |
| 8 | 端對端整合測試 | MVP1 先跑 300 人，之後逐步擴大 |

## 開發慣例

### UC 編號規範

格式：`UC-ACT {大類}.{子層}.{子子層}`

| 大類 | 類別 |
| ---- | ---- |
| 3.1 | 基礎建設（必含） |
| 3.2 | WEB |
| 3.3 | API |
| 3.4 | Backend |
| 3.5 | JOB |
| 4.x | 異質系統（每個外部系統獨占一個 4.x） |
| 5.x | 其他 |

- UC 清單完整定義在 `docs/design/SDD.md` 的「UC 清單」章節
- commit message 格式：`feat: UC-ACT {大類}.x.x [功能名稱]`
- 跨 UC 引用格式：`呼叫 [UC-ACT {大類}.x.x]`

### 其他命名慣例

- 每個 workload 一個資料夾：`web/`、`api/`、`backend/`、`job/`、`external/`，各有 `blueprint.md`
- 情境包代號沿用 POC 慣例：`{產業縮寫}-{序號}-{slug}`，如 `med-01-outpatient-change`
- 介面文字一律繁體中文，不做多語系；外部服務的英文錯誤不得直接顯示給使用者

## 關鍵業務約束

- **Digital Twin 由 Orbit 團隊提供**，我們只串接、不自建模擬系統；介面不是我們能換的
- **完成判定看模擬系統的實際結果**，不看 Agent 嘴上說完成
- **資料要歸屬組織**：所有帳號與衍生資料都帶預設組織（OV-04），不得留空
- **Playground、Level 2、後台管理、個資刪除是下一階段**，只預留不實作
- 帳號以 **email** 為唯一識別，同 email 跨登入方式視為同一帳號
- **MVP1 登入**：邀請碼 + email 驗證後，寄 token 到信箱登入；SSO 後移 MVP2
- **未決事項不自己定，先問**（回應時間目標、第 5 個產業、Orbit 非醫療業交付時程）
- LLM 一律經 AI Gateway，不直連模型供應商

## 測試規範（專案特有）

繼承通用測試規範（上方第一部分）。本專案補充：
- Error path 驗收必列：Twin 斷線 / 逾時、LLM 逾時 / 5xx、用量上限、邀請碼無效、SSO 失敗、同 email 跨方式登入
- **DB 禁止 mock**：測試用真實 PostgreSQL（`db_act_test`）
- 非預期的 sibling exception 必測（例如 `ConnectError` 與 `TimeoutException`）
- 學員間狀態隔離必測：A 的操作不得出現在 B 的案件
- 四種尺寸 e2e（桌機 1440×900、平板 820×1180 / 1180×820、手機 390×844）

## 專案目錄結構

```
AgentCraft/
├── CLAUDE.md
├── .gitignore
├── .pre-commit-config.yaml
├── 需求/                         # 需求來源（簡報、圖、POC 壓縮檔）
├── docs/
│   ├── INTRO.md
│   ├── INDEX.md
│   ├── TODO.md
│   ├── SETUP.md
│   ├── design/                   # ARCHITECTURE / TASK / SDD / ESTIMATION-TEMPLATE / POC-ANALYSIS
│   ├── decisions/                # ADR
│   └── specs/
├── web/ api/ backend/ job/ external/   # 各 workload，內含 blueprint.md
├── scripts/check_conventions.py
├── tests/_templates/
└── .claude/commands/             # checkpoint / checkservice
```
