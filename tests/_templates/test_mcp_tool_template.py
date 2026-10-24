# ============================================================
# 檔案名稱：test_mcp_tool_template.py
# 中文名稱：MCP Tool 處理器測試樣板
# 功能說明：呼叫 Orbit Digital Twin 等 MCP 上游的測試起點；涵蓋四條必測路徑
# 所屬模組：tests/_templates/
# 建立日期：2026-10-24
# 修改日期：2026-10-24
# 開發者　：BlackJ-Tsai
# ============================================================
#
# 使用方式：
#   cp tests/_templates/test_mcp_tool_template.py tests/test_<tool>.py
#   （本檔含 <佔位符>，僅供複製後修改，不可直接執行）
#
# 必測路徑（缺一要補）：
#   ✅ 成功路徑
#   ✅ 參數錯誤（缺欄位 / 型別錯）
#   ✅ 上游不可達（ConnectError）
#   ✅ sibling exception：TimeoutException 與 ConnectError 同層，確認也被攔住
#   ✅ 認證失敗（401/403）：立即放棄，不重試
#   ✅ 錯誤訊息為繁體中文，不外洩上游英文錯誤（OV-01）

import re

import httpx
import pytest
from httpx import ConnectError, TimeoutException
from unittest.mock import AsyncMock, patch

CJK = re.compile(r"[\u4e00-\u9fff]")


def assert_zh_error(result) -> None:
    """錯誤結果必須含繁體中文訊息，且不得夾帶上游英文錯誤字串（OV-01）。"""
    message = str(result.get("error", ""))
    assert CJK.search(message), f"錯誤訊息缺少中文：{message!r}"
    assert "status_code" not in message and "Error:" not in message


@pytest.mark.asyncio
async def test_tool_success():
    """成功路徑：上游正常回應，回傳預期結果。"""
    with patch("<upstream_call>", new_callable=AsyncMock) as mock:
        mock.return_value = "<EXPECTED_RESPONSE>"
        result = await tool_handler(<VALID_PARAMS>)
    assert result["status"] == "ok"


@pytest.mark.asyncio
async def test_tool_missing_params():
    """參數缺漏：應回傳明確錯誤訊息，不拋 exception。"""
    result = await tool_handler({})
    assert_zh_error(result)


@pytest.mark.asyncio
async def test_tool_upstream_unreachable(monkeypatch):
    """上游不可達（ConnectError）：應被攔住，回傳繁中友善錯誤，不拋。"""
    monkeypatch.setattr("<upstream_call>", AsyncMock(side_effect=ConnectError("unreachable")))
    result = await tool_handler(<VALID_PARAMS>)
    assert_zh_error(result)


@pytest.mark.asyncio
async def test_tool_upstream_timeout(monkeypatch):
    """sibling exception：TimeoutException 與 ConnectError 同層，確認也被攔住。"""
    monkeypatch.setattr("<upstream_call>", AsyncMock(side_effect=TimeoutException("timeout")))
    result = await tool_handler(<VALID_PARAMS>)
    assert_zh_error(result)


@pytest.mark.asyncio
async def test_tool_auth_failure_no_retry(monkeypatch):
    """401/403：立即放棄，不重試（呼叫次數必須為 1）。"""
    response = httpx.Response(401, request=httpx.Request("POST", "http://twin.test"))
    mock = AsyncMock(side_effect=httpx.HTTPStatusError("401", request=response.request, response=response))
    monkeypatch.setattr("<upstream_call>", mock)
    result = await tool_handler(<VALID_PARAMS>)
    assert_zh_error(result)
    assert mock.call_count == 1


@pytest.mark.asyncio
async def test_tool_unexpected_exception_does_not_leak(monkeypatch):
    """非預期的 sibling（例如 RuntimeError）：不得原樣穿透給呼叫端，回傳繁中錯誤。"""
    monkeypatch.setattr("<upstream_call>", AsyncMock(side_effect=RuntimeError("boom")))
    result = await tool_handler(<VALID_PARAMS>)
    assert_zh_error(result)
