# ADR-005：Agent 對話上下文由自建紀錄表組裝

> 狀態：草稿（方向已與使用者對齊，細節待 Layer 4 實作時以真實 API 驗證）
> 日期：2026-10-25
> 決策者：BlackJ-Tsai

## 背景

LLM 使用 Gemini API。標準 `generateContent` 無狀態，每次請求只看當次送入的內容；SDK 的 chat 輔助只把歷史存在程式記憶體，job 重啟、多副本或學員斷線重連即遺失。專案另有需求：學習紀錄與完成判定需可追溯、學員間狀態隔離、情境包版本固定、AI Gateway 是否採用尚未決定。

## 選項

| 選項 | 優點 | 缺點 |
| ---- | ---- | ---- |
| A 用 SDK chat（記憶體） | 最省事 | 重啟 / 多副本 / 重連即失憶，無紀錄 |
| B 依賴供應商端保存對話狀態 | 少送資料 | 歷史在外部，無法自行隔離、審計、換供應商；功能細節未查證 |
| **C 自建紀錄表，每次組裝後送出（採用）** | 紀錄即上下文來源；可重連、可審計、不綁供應商 | 需自行處理組裝、冪等、並行與長度 |

## 決策

採用 C。以下為**建議，待實作時確認**：

### 資料表

- `act_agent_request`：一次 LLM 呼叫一列，會更新狀態，帶標準 8 欄。
  欄位：`request_id`（PK，UUID，由前端 / API 在送出時產生）、`case_id`、`status`（`running` / `done` / `failed`）、`model`、`input_token_count`、`cached_token_count`、`output_token_count`、`latency_ms`、`provider_response_id`（僅供除錯）、`error_code`（我們自己的錯誤碼，不存英文原文）。
- `act_agent_turn`：歷史的一則內容一列，寫入後不修改，純 log 表只帶 `create_*` 四欄。
  欄位：`turn_id`（PK）、`case_id`、`seq`（`(case_id, seq)` 唯一）、`request_id`、`role`（`user` / `model` / `tool`）、`kind`（`message` / `summary`）、`parts`（jsonb，**存 Gemini 原始 parts**，含工具呼叫與思考簽章，需原樣送回）、`covers_to_seq`（僅 summary）、`token_count`。
- `case_id` 對應的案件表名稱待 Layer 1 實體清單確認。
- 索引：`act_agent_turn(case_id, seq)` 唯一；`act_agent_request(case_id, create_date)`；`act_agent_request(case_id) WHERE status='running'` 部分唯一。

### 行為規則

1. **接續對話靠 `case_id` 查歷史組裝，不靠任何請求代號。** Gemini 的 response id 只存來除錯。
2. **冪等**：`request_id` 唯一；重送回傳第一次結果，不重複呼叫、不重複計費。
3. **同案件同時只允許一個進行中呼叫**（部分唯一索引），避免 `seq` 錯亂。
4. **失敗的呼叫**標 `failed`，不寫入 `model` turn。
5. **組裝順序**：固定前綴（system prompt、情境包定版、Skill）在前，其後為摘要與最近歷史，最後是本次輸入。目的是讓 Gemini 隱式快取命中；以回應的 cached token 數驗證。
6. **MVP1 全量重播歷史**，只截斷過長的工具結果。超過 token 門檻（暫定預算的 60%）才由 job 產生摘要：**新增一列 `kind='summary'`，不刪舊列**；組裝時取最新摘要加其後的原文。摘要機制是否排入 MVP1，待用 POC 紀錄估算對話長度後決定。
7. 明確快取（context caching）MVP1 不做，待有用量數據再評估；是否經 AI Gateway 決定前，不假設快取參數可透傳。
8. 上下文只影響 Agent 回答；**完成判定仍看 Twin 實際結果**。

## 後果

- Layer 4 新增 2 表與組裝模組；用量欄位可供 Layer 6 用量上限使用。
- 不引入向量庫等新元件，符合「基礎元件僅七項」。
- Redis 最多作熱快取，PostgreSQL 為唯一來源。
- 對話逐字稿屬個資範疇，後台 A3 不顯示逐字稿（已於 TASK.md Layer 6 規定）；個資刪除為下一階段，表設計需能依 `case_id` 整批處理。

## 待確認

- Gemini 多輪 function calling 的思考簽章處理方式（Layer 4 以實際 API 驗證）。
- 單次練習的對話輪數與工具結果大小（決定摘要是否進 MVP1）。
- AI Gateway 是否採用，及其對快取與串流的影響。
