"""Kho dataset do Admin quản lý (lưu trên đĩa: data_store/)."""
import json
import os
import uuid
from pathlib import Path

import pandas as pd

STORE_DIR = Path(__file__).resolve().parent.parent / "data_store"
INDEX_FILE = STORE_DIR / "index.json"
MAX_NAME_LEN = 60


def _read_index() -> dict:
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_index(index: dict):
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = INDEX_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, INDEX_FILE)


def list_custom() -> dict:
    """{tên: {"file":..., "label":..., "desc":...}} – chỉ gồm dataset còn tệp trên đĩa."""
    return {n: m for n, m in _read_index().items() if (STORE_DIR / m["file"]).exists()}


def custom_names() -> list:
    return sorted(list_custom())


def load_custom(name: str) -> pd.DataFrame:
    return pd.read_csv(STORE_DIR / list_custom()[name]["file"])


def validate_name(name: str, builtin_names, current=None):
    name = (name or "").strip()
    if not name:
        return "Tên dataset không được để trống."
    if len(name) > MAX_NAME_LEN:
        return f"Tên dataset tối đa {MAX_NAME_LEN} ký tự."
    taken = set(builtin_names) | set(_read_index())
    if current:
        taken.discard(current)
    if name in taken:
        return "Tên dataset đã tồn tại."
    return None


def add_dataset(name: str, df: pd.DataFrame, label_col, desc: str = ""):
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.csv"          # tên tệp sinh ngẫu nhiên → không bị path traversal
    df.to_csv(STORE_DIR / filename, index=False, encoding="utf-8")
    index = _read_index()
    index[name.strip()] = {"file": filename, "label": label_col, "desc": desc.strip()}
    _write_index(index)


def update_dataset(name: str, new_name: str, label_col, desc: str):
    index = _read_index()
    meta = index.pop(name)
    meta.update(label=label_col, desc=desc.strip())
    index[new_name.strip()] = meta
    _write_index(index)


def delete_dataset(name: str):
    index = _read_index()
    meta = index.pop(name, None)
    if meta:
        try:
            (STORE_DIR / meta["file"]).unlink()
        except FileNotFoundError:
            pass
    _write_index(index)
