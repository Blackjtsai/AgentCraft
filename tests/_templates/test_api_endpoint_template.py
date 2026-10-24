# ============================================================
# 檔案名稱：test_api_endpoint_template.py
# 中文名稱：REST API 端點測試樣板
# 功能說明：新 API 端點測試的優先參考起點；涵蓋四條必測路徑
# 所屬模組：tests/_templates/
# 建立日期：2026-10-24
# 修改日期：2026-10-24
# 開發者　：BlackJ-Tsai
# ============================================================
#
# 使用方式：
#   cp tests/_templates/test_api_endpoint_template.py tests/test_<feature>.py
#   將 <ENDPOINT>、<EXPECTED_FIELD> 替換為實際值，並把 VALID_BODY 改成該端點的合法請求
#   （本檔含佔位符，僅供複製後修改，不可直接執行）
#
# 必測路徑（缺一要補）：
#   ✅ 200  成功路徑
#   ✅ 401  未提供 token
#   ✅ 403  有 token 但無權限
#   ✅ 422  格式錯誤（欄位缺漏 / 型別不符）
#   ➕ 本專案加測：學員 A 不得讀寫學員 B 的資源（隔離）

import pytest
from httpx import AsyncClient

VALID_BODY: dict = {}  # 改成合法請求內容；403 與 200 測試都用它，才會真的走到權限檢查
INVALID_BODY: dict = {}  # 改成缺必填欄位的請求，專供 422 測試


@pytest.mark.asyncio
async def test_feature_success(client: AsyncClient, auth_headers: dict):
    """成功路徑：回傳 200 與預期資料。"""
    response = await client.post("/<ENDPOINT>", json=VALID_BODY, headers=auth_headers)
    assert response.status_code == 200
    assert "<EXPECTED_FIELD>" in response.json()


@pytest.mark.asyncio
async def test_feature_unauthorized(client: AsyncClient):
    """401：未提供 token，應立即拒絕，不重試。"""
    response = await client.post("/<ENDPOINT>", json=VALID_BODY)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_feature_forbidden(client: AsyncClient, other_user_headers: dict):
    """403：token 有效但無此資源存取權（學員隔離）。"""
    response = await client.post("/<ENDPOINT>", json=VALID_BODY, headers=other_user_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_feature_validation_error(client: AsyncClient, auth_headers: dict):
    """422：必填欄位缺漏，應回傳驗證錯誤，不拋 exception。"""
    response = await client.post("/<ENDPOINT>", json=INVALID_BODY, headers=auth_headers)
    assert response.status_code == 422
