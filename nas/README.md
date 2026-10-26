# nas/ — 情境素材儲存區（NAS 工作目錄）

> 版本：v0.1 ／ 2026-10-24
> 對應 UC-ACT 3.4.2.4（情境視覺素材）與 `docs/specs/UX-GUIDELINES.md` U-11。
> **初期在本機執行**（使用者 2026-10-24）：這個資料夾就是本機實際使用的素材儲存區，程式以設定檔指定根目錄（預設指向本資料夾）。上雲後改由 K8s 掛載 NAS（掛載路徑、協定待確認，見 `docs/TODO.md`），目錄規約不變。
> **圖片檔不進版控**（見根目錄 `.gitignore`）；只有本說明與空資料夾結構進版控。

## 目錄規約

```
nas/
├── README.md
├── _defaults/
│   └── industry/{medical,manufacturing,finance,retail,common}/   # 產業預設圖（沒上傳素材時的後備）
│       ├── cover.webp        # 情境卡封面預設
│       └── banner.webp       # 工作台橫幅預設
└── scenarios/
    └── {scenario_code}/      # 如 med-01-outpatient-change；代號定了不改
        └── v{version}/       # 素材跟著情境版本；更新情境 = 新資料夾，舊版不覆蓋
            ├── cover.{jpg|png|webp}      # 情境卡封面（P3 / P4）
            ├── banner.{jpg|png|webp}     # 工作台橫幅或底圖（P5）
            ├── scene-*.{jpg|png|webp}    # 人物與場景插圖（M2）
            └── icon-{system}.{png|webp}  # 模擬系統圖示（M2）
```

## 規則

| 項目 | 規定 |
| ---- | ---- |
| 格式 | JPG / PNG / WebP。**不收 SVG**（避免腳本注入）、不收 GIF 動畫（MVP1） |
| 大小 | 單檔上限暫訂 2 MB；尺寸上限與建議比例待 Design System 定案 |
| 檔名 | 小寫英數與連字號；位置名稱固定（cover / banner / scene-* / icon-*），不接受使用者自訂路徑 |
| 資料庫 | 只存**相對路徑**與替代文字，不存絕對路徑；每張圖必填替代文字 |
| 版本 | 路徑含 `v{version}`；已發布版本的素材**不可覆蓋**，要改就發新版本 |
| 存取 | 前台**只經 api 的受控端點讀取**（白名單位置名稱＋情境代號驗證），不直接暴露 NAS 路徑；防止路徑穿越（`..`、絕對路徑、符號連結） |
| 預設圖 | 找不到素材時回該產業的 `_defaults`；預設圖也不存在時回通用占位圖，不回錯誤頁 |
| 備份 | 由基礎設施團隊的 NAS 備份機制負責（待確認）；素材可由情境來源重新上傳，不是唯一副本 |

## K8s 注意事項（待確認）

- 多個 api 副本同時讀取：NAS 需以 **ReadWriteMany**（如 NFS）方式掛載。
- 上傳只由後台寫入；前台 Pod 以**唯讀**掛載。
- 若 NAS 不可用：前台顯示預設圖，後台上傳回明確錯誤，不影響學員練習。
