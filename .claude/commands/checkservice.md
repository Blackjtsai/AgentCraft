# /checkservice

檢查本專案所有服務的目前狀況，輸出狀態表。

## 服務清單

| 服務 | 類型 | 預期位置 |
| ---- | ---- | -------- |
| PostgreSQL | DB | `localhost:5432`，資料庫 `db_act_dev`、`db_act_test` |
| Redis | Cache / Queue | `localhost:6379` |
| api | FastAPI | `http://localhost:8000/healthz` |
| web | Next.js | `http://localhost:3000` |
| job | 背景 worker | 程序存在（以 Redis 佇列心跳判斷，待 Layer 1 定案） |

> 尚未建立的服務（api / web / job 在 Layer 1 前不存在）狀態標「未建立」，不算失敗。

## 執行步驟

```bash
pg_isready -h localhost -p 5432
psql -lqt | cut -d '|' -f1 | grep -E 'db_act_(dev|test)'
redis-cli ping
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/healthz
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
pgrep -fl "job" || echo "job 未執行"
```

## 輸出格式

```
=== AgentCraft 服務狀態 ===

服務             狀態    備註
──────────────── ─────── ────────────────────────────
PostgreSQL       ✅/❌   localhost:5432
Redis            ✅/❌   localhost:6379
api              ✅/❌/— http://localhost:8000
web              ✅/❌/— http://localhost:3000
job              ✅/❌/— worker

最後檢查時間：YYYY-MM-DD HH:MM
```

## 詢問開關

輸出狀態表後，問一次：
「需要對服務執行什麼操作？（開啟 / 關閉 / 略過）」
