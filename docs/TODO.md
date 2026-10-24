# TODO — AgentCraft（代理工坊）

> 進度唯一來源。每次對話查進度從此檔讀取，不從記憶體查。
> 任務說明請查 `docs/design/TASK.md`；UC 清單請查 `docs/design/SDD.md`；架構請查 `docs/design/ARCHITECTURE.md`。
> 格式：`[ ]` 待辦 / `[x]` 完成 / `[-]` 進行中
> 任務項目請附 UC 編號，例：`[ ] UC-ACT 3.1.1.1 K8s 環境與 CI/CD`

---

## 啟動前待辦（初始化遺留）

- [ ] 確認團隊人數與可投入人天（TASK.md 估算 L1–L6 約 80 人天，SSO 已移 MVP2，11 月底前需並行）
- [ ] 向產品規劃團隊（Scottie）確認：回應時間目標、第 5 個產業、Orbit 非醫療業交付時程
- [ ] 向 Orbit 團隊取得 Digital Twin 介面資訊（MCP 端點、認證、sandbox 隔離與重設能力）
- [ ] 確認 Agent 執行位置（api 內嵌 vs Agent 平台團隊的 Pod）→ 寫成 ADR-001
- [ ] 確認 Layer 7（Studio）是否排 MVP2
- [ ] 向產品規劃團隊確認「人次」定義（每次登入 / 每個情境練習 / 每次 Agent 對話？）與預期同時並行數，作為 Layer 6、8 壓測目標
- [x] 登入 POC 並截圖（2026-10-24，存於 `docs/design/poc-screenshots/`，索引與觀察見該資料夾 README）
- [ ] 取得 P6（Skill 編輯、換案驗證）與 P7 有成果狀態的截圖：需在 POC demo 帳號完成第一關，會改變帳號資料，待使用者同意
- [ ] 回應時間目標：POC 實測 Agent 出方案超過 10 分鐘，需向產品規劃團隊定義目標並確認是否為 POC 限制
- [ ] 後台規劃納入 TASK.md / SDD.md UC（依 `docs/specs/SITEMAP.md` §3，待確認 MVP2 範圍）
- [ ] Layer 1 Schema 預留：org_id、Seat / 角色、LLM 呼叫 token 計量、稽核 log 表、情境版本（見 SITEMAP §3.7）
- [ ] 確認 MVP1 登入 token 細節：連結或驗證碼、有效期、一次性、邀請碼是否每次登入都要、寄信服務選型；SSO 後移是否確認（TASK Layer 2 可減約 3.5 天）
- [ ] 確認 TASK.md 工時是否以「人工開發」或「AI 輔助開發」為基準，並於 Layer 1 驗收後用實際值校準
- [x] 建立第一個本地 commit（2026-10-24 checkpoint）
- [ ] push 到 `https://github.com/Blackjtsai/AgentCraft.git`（待使用者核准；需 GitHub 認證）

## Layer 1：基礎建設與資料層

> 細項待 Layer 開始前依 TASK.md 展開。

## Layer 2：身分與帳號

## Layer 3：情境包與 Digital Twin 串接

## Layer 4：Agent、完成判定與學習紀錄

## Layer 5：學員練習 Web（P1–P7）

## Layer 6：安全、營運與用量

## Layer 7：Scenario Studio（MVP2，待確認）

## Layer 8：端對端整合測試
