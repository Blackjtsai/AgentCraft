#!/usr/bin/env python3
# ============================================================
# 檔案名稱：check_conventions.py
# 中文名稱：專案規範檢查器
# 功能說明：pre-commit hook，檢查命名規範、檔案 header、DB 稽核欄（限制：只認 __tablename__ 字面值宣告）
# 所屬模組：scripts/
# 建立日期：2026-10-24
# 修改日期：2026-10-24
# 開發者　：BlackJ-Tsai
# ============================================================

import re
import subprocess
import sys
from pathlib import Path

SYSTEM_CODE = "act"  # new-project-init 生成時填入實際值

HEADER_FIELDS = [
    "# 檔案名稱：",
    "# 中文名稱：",
    "# 功能說明：",
    "# 所屬模組：",
    "# 建立日期：",
    "# 修改日期：",
    "# 開發者　：",
]

AUDIT_COLUMNS = [
    "is_delete", "create_user", "create_date", "create_ip",
    "update_user", "update_date", "update_ip",
]

SKIP_DIRS = {"__pycache__", ".venv", "node_modules", ".git", "migrations", "_templates"}
SKIP_FILES = {"__init__.py", "conftest.py"}
SKIP_TABLE_WORDS = {"log", "junction", "assoc"}


def get_staged_py_files() -> list[str]:
    """取得本次 staged 的 .py 檔案清單。"""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True,
    )
    return [f for f in result.stdout.splitlines() if f.endswith(".py")]


def read_staged(file_str: str) -> str:
    """讀取 staged 版本內容（而非工作目錄），避免未 staged 的修改掩蓋違規。"""
    result = subprocess.run(
        ["git", "show", f":{file_str}"], capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else Path(file_str).read_text(encoding="utf-8")


def check_header(content: str) -> list[str]:
    """回傳 header 問題：只檢查檔案前 20 行，且每個欄位必須有填值。"""
    head = content.splitlines()[:20]
    errors = []
    for field in HEADER_FIELDS:
        line = next((ln for ln in head if ln.startswith(field)), None)
        if line is None:
            errors.append(f"缺少 header 欄位（須在檔案前 20 行）：{field.strip()}")
        elif not line[len(field):].strip():
            errors.append(f"header 欄位沒有填值：{field.strip()}")
    return errors


def split_tables(content: str) -> list[tuple[str, str]]:
    """依 __tablename__ 切出各資料表的程式碼區段，回傳 (表名, 區段內容)。"""
    matches = list(re.finditer(r'__tablename__\s*=\s*["\']([^"\']+)["\']', content))
    tables = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        tables.append((m.group(1), content[m.start():end]))
    return tables


def check_table_naming(content: str) -> list[str]:
    """回傳命名不符規範的資料表清單。"""
    return [
        f"資料表命名錯誤：{name!r} 應以 {SYSTEM_CODE}_ 開頭"
        for name, _ in split_tables(content)
        if not name.startswith(f"{SYSTEM_CODE}_")
    ]


def check_audit_columns(path: Path, content: str) -> list[str]:
    """逐表檢查標準稽核欄；表名含 log / junction / assoc 的字詞（以 _ 分隔）視為純 log 或關聯表而略過。"""
    errors = []
    for name, body in split_tables(content):
        if SKIP_TABLE_WORDS & set(name.split("_")):
            continue
        missing = [col for col in AUDIT_COLUMNS if col not in body]
        if missing:
            errors.append(f"資料表 {name} 缺少標準稽核欄：{', '.join(missing)}")
    return errors


def main() -> None:
    """掃描 staged .py 檔案（讀 staged 版本），有違規則印出錯誤並以 exit(1) 中止 commit。"""
    errors_by_file: dict[str, list[str]] = {}

    for file_str in get_staged_py_files():
        path = Path(file_str)
        if any(part in SKIP_DIRS for part in path.parts) or path.name in SKIP_FILES:
            continue

        content = read_staged(file_str)
        if not content.strip():
            continue
        errs = (
            check_header(content)
            + check_table_naming(content)
            + check_audit_columns(path, content)
        )
        if errs:
            errors_by_file[file_str] = errs

    if errors_by_file:
        print("❌ 規範檢查失敗：")
        for file_str, errs in errors_by_file.items():
            print(f"\n{file_str}")
            for e in errs:
                print(f"  {e}")
        print("\n修正後重新 git add 並 commit。")
        sys.exit(1)

    print("✅ 規範檢查通過")


if __name__ == "__main__":
    main()
