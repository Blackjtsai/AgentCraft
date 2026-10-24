# ============================================================
# 檔案名稱：test_llm_stream_template.py
# 中文名稱：LLM 串流測試樣板
# 功能說明：經 AI Gateway 的 LLM 串流測試起點；涵蓋三條必測路徑
# 所屬模組：tests/_templates/
# 建立日期：2026-10-24
# 修改日期：2026-10-24
# 開發者　：BlackJ-Tsai
# ============================================================
#
# 使用方式：
#   cp tests/_templates/test_llm_stream_template.py tests/test_<feature>_stream.py
#   （本檔含 <佔位符>，僅供複製後修改，不可直接執行；5xx 與外洩測試依實際串流介面改用 async generator 或 AsyncMock）
#
# 必測路徑（缺一要補）：
#   ✅ 逾時：超過閾值，回傳中文錯誤訊息，不拋 exception
#   ✅ 中途斷線：串流進行中上游中斷，graceful 結束不拋
#   ✅ 上游 5xx：LLM API 回 500/503，不重試，回傳友善錯誤
#   ✅ 使用者可見文字不含英文錯誤（OV-01；POC 曾直接外洩 ModelHTTPError）

import re

import pytest
from unittest.mock import AsyncMock

CJK = re.compile(r"[\u4e00-\u9fff]")


def assert_zh_message(result) -> None:
    """使用者可見訊息必須含繁體中文，且不得夾帶上游英文錯誤字串（OV-01）。"""
    text = str(result)
    assert CJK.search(text), f"訊息缺少中文：{text!r}"
    for leak in ("ModelHTTPError", "status_code", "Traceback"):
        assert leak not in text, f"外洩上游英文錯誤：{leak}"


@pytest.mark.asyncio
async def test_stream_timeout(monkeypatch):
    """逾時：超過閾值時，應回傳中文錯誤訊息，不拋 exception。"""
    async def fake_stream(*args, **kwargs):
        raise TimeoutError("LLM timeout")
        yield  # 讓 Python 認識為 async generator

    monkeypatch.setattr("<llm_client_stream>", fake_stream)
    result = await stream_handler(<VALID_PARAMS>)
    assert_zh_message(result)


@pytest.mark.asyncio
async def test_stream_disconnect(monkeypatch):
    """中途斷線：串流中上游中斷，應 graceful 結束，不拋 exception。"""
    async def fake_stream(*args, **kwargs):
        yield "部分內容"
        raise ConnectionResetError("disconnected")

    monkeypatch.setattr("<llm_client_stream>", fake_stream)
    result = await stream_handler(<VALID_PARAMS>)
    assert "部分內容" in str(result)  # 已收到的內容要保留
    assert_zh_message(result)


@pytest.mark.asyncio
async def test_stream_upstream_5xx(monkeypatch):
    """上游 5xx：不重試，回傳友善錯誤。"""
    monkeypatch.setattr(
        "<llm_client_stream>",
        AsyncMock(side_effect=Exception("upstream 500")),
    )
    result = await stream_handler(<VALID_PARAMS>)
    assert_zh_message(result)


@pytest.mark.asyncio
async def test_stream_error_not_leaked_in_english(monkeypatch):
    """使用者可見訊息不得含上游英文錯誤字串。"""
    monkeypatch.setattr(
        "<llm_client_stream>",
        AsyncMock(side_effect=Exception("ModelHTTPError: status_code: 503")),
    )
    result = await stream_handler(<VALID_PARAMS>)
    assert_zh_message(result)
