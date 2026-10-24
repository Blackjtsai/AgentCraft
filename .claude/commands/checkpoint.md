# /checkpoint

執行對話檢查點。整理重點、記錄經驗、同步文件、commit 所有變動。

> **規範原則**：「執行步驟的判斷條件」必須寫在此檔案的步驟說明裡，不能只存 memory。
> Memory 是提示，規範才是約束。發現判斷條件有缺漏時，同步更新此檔，不只記 feedback。

---

## 步驟

### 1. 對話重點摘要 → docs/CHANGELOG.md

先讀取 `docs/CHANGELOG.md` 最後一筆的時間戳（`## YYYY-MM-DD` 或 `## YYYY-MM-DD 標題`）。
只摘要**該時間戳之後**發生的事項，append 一筆新紀錄：

```
## YYYY-MM-DD 標題

- 做了什麼（決策、實作、修改）
- 遇到什麼問題或誤判
- 確認了什麼規範或方向
```

> 若本次對話是首次執行 checkpoint，摘要整段對話。檔案不存在則建立。

---

### 2. 經驗記錄 → Memory

檢查本次對話（上一筆 checkpoint 之後）是否有值得記錄的經驗：

- 錯誤或誤判 → `feedback` memory
- 使用者偏好或習慣 → `user` memory
- 專案決策或背景 → `project` memory
- 架構取捨 / 設計決策分析類討論（不論當下有無明確結論）且對話中尚未問過是否保存 → 主動詢問；屬既有決策延伸理由優先補進對應 ADR / 設計文件，屬新脈絡則寫入 memory
- 其中若有決策判斷不限於本專案、具通用性 → 額外詢問是否同步更新到全域規範
- 無新資訊 → 明確說明「本次無新增 memory」

**Memory 淘汰檢查（Layer 完成時觸發）**：

讀取 `docs/TODO.md`，判斷本次對話是否有某個 Layer 的所有項目從未完成變為全部 `[x]`：

- **有 Layer 剛完成** → 掃描專案 memory 目錄中所有 `project_*.md`，逐一判斷：
  - 描述的狀態已落地進程式碼或文件 → 提議刪除，列出檔名與理由，等使用者確認後才刪
  - 仍是活的決策背景 → 保留，說明原因
- **無 Layer 剛完成** → 說明「本次無 Layer 完成，略過 memory 淘汰檢查」

---

### 3. 檢查 CLAUDE.md 與 .claude/commands/

**`docs/design/SDD.md`**：
本次對話若有 Layer 驗收完成，或涉及新模組、新 API 端點、Schema 異動 → 對應章節同步更新，並在版本記錄新增一筆；無結構性變動 → 說明原因。

**根目錄 `CLAUDE.md`**：有新規範補入、有舊規範推翻則修正；無變動說明原因。

**子目錄 CLAUDE.md**：
讀取根目錄 `CLAUDE.md` 的「專案目錄結構」區塊，找出所有有獨立 CLAUDE.md 的子目錄，逐一確認：

| 判斷條件 | 動作 |
| -------- | ---- |
| 本次對話有新增 / 刪除該目錄下的檔案 | 更新對應子目錄 CLAUDE.md |
| 該目錄的核心邏輯規則有變動 | 更新對應子目錄 CLAUDE.md |
| 有新增函式或測試案例 | 更新對應子目錄 CLAUDE.md 的涵蓋範圍描述 |
| 以上皆無 | 說明「無需更動」 |

**`.claude/commands/*.md`**：
對照 CLAUDE.md 中列出的核心模組（API 端點、管理 CLI 等），確認 skill 描述與清單是否仍正確。

**`docs/INTRO.md`**：
- REST API 端點有新增 / 刪除 → 同步更新對應段落
- 目錄結構有新增資料夾或搬移 → 同步更新目錄結構區塊
- 系統元數據有變更（系統代號、資料庫名稱、相依系統等）→ 同步更新頂部資訊表，並更新 `最後更新` 日期
- 以上皆無 → 說明原因

**`docs/decisions/`**：
若本次對話有重大架構決策（技術選型、廢棄原有方案、引入新外部依賴、安全策略變更等）→ 新增一筆 `ADR-{N:03d}-{slug}.md`，N 為下一個流水號；無決策 → 說明「本次無新增 ADR」。

各項結論必須明確回覆「需要更新 → 已更新」或「無需更動 → 原因」。

---

### 4. 檢查 docs/design/ARCHITECTURE.md

- 有新模組或服務 → 更新 Mermaid 圖
- 有 Layer 驗收完成 → 更新 Layer 狀態表
- 無需更動 → 說明原因

---

### 5. 檢查 docs/SETUP.md

若本次對話確認或新增了環境工具、套件、設定、外部資源（OAuth client、K8s namespace 等），同步更新狀態欄。

---

### 6. 檢查 docs/design/TASK.md

列出 `docs/TODO.md` 中所有 `## Layer` 標題，對照 `docs/design/TASK.md` 是否都有對應條目：
- 有缺漏 → 補寫缺漏的 Layer 條目，完成後才繼續
- 任務說明、驗收條件、依賴關係有調整 → 同步更新
- 有條目但缺「工時估算」小節或缺「評估依據」→ 依 `docs/design/ESTIMATION-TEMPLATE.md` 補上，完成後才繼續
- 有 Layer 剛驗收完成 → 回填該 Layer 估算的「預估 vs 實際」到 `ESTIMATION-TEMPLATE.md` 的校準範例表
- 無缺漏且無調整 → 說明「TASK.md 無需更動」

---

### 7. 更新有異動的 Workload Blueprint.md

掃描本次對話中有檔案異動的 workload 目錄（`web/`、`api/`、`backend/`、`job/`、`external/`），逐一確認：

| 判斷條件 | 動作 |
| -------- | ---- |
| 該 workload 目錄下有新增 / 修改 / 刪除檔案 | 更新 `{workload}/blueprint.md` |
| 新增 API endpoint 或元件 | 更新「對外介面」區塊 |
| Layer 驗收完成 | 更新「當前 Layer 狀態」表，狀態標記 ✅ |
| 技術棧或目錄結構有變動 | 更新對應區塊 |
| 以上皆無 | 說明「{workload}/blueprint.md 無需更動」 |

同步更新 blueprint.md 頂部的 `最後更新` 日期，並 bump minor 版本號。

---

### 8. 檢核並更新 docs/INDEX.md

```bash
find docs/ -type f ! -name ".DS_Store" | sort
```

對照 `docs/INDEX.md`：有新增補入、有刪除或搬移則修正；無變動說明「INDEX.md 無需更動」。

---

### 9. Code Review

先看本次變動的檔案清單，自動選擇等級：

**`high`**（任一條件符合）：
- 身份驗證、權限判斷、Token / Session 驗證、OAuth、邀請碼邏輯有異動
- DB Schema 變動（DDL、ALTER TABLE）
- 用量限制與 sandbox 隔離邏輯有異動（學員間資料隔離）
- 新增模組或大規模重構（超過 3 個核心檔案同時異動）

**`medium`**（其餘情況）：
- UI template、前端 JS、文件、設定檔、一般 CRUD 端點

執行 `/code-review <選定等級>`，並說明選擇原因：

- 有 CONFIRMED / PLAUSIBLE findings → 修完再繼續
- 全部 REFUTED 或無 findings → 說明「code review 無問題」，繼續

---

### 10. 更新 docs/TODO.md

- 已完成項目標記 `[x]`
- 新增本次發現的待辦項目

---

### 11. Lint 檢查

```bash
uv run ruff check . --fix && uv run ruff format .
# 若 web/ 已建立：
cd web && npm run lint
```

- 全通過 → 繼續（自動修的異動會在 Step 13 一起 commit）
- 有修不了的錯誤 → 列出問題，手動修完才繼續

---

### 12. 執行測試

**確認服務就緒**：執行 `/checkservice`（PostgreSQL、Redis 必須就緒）。

**執行測試**：

```bash
uv run pytest          # api / backend / job
cd web && npm test     # 若 web/ 已建立
```

- 全過 → 繼續
- 有失敗 → 修到全過才繼續，不帶紅燈 commit

若專案尚未建立測試，說明「目前無測試」並繼續。

---

### 13. Git Commit + Push

```bash
git add <changed files>
git commit -m "checkpoint: <一句話描述本次主要變動>"
git push
```

直接 commit 並 push，不需等使用者確認。
**commit 前確認 `git status` 沒有 `.env`、`需求/文檔.md`（含 POC 帳密）、`*.pptx`、`*.zip` 被加入。**
