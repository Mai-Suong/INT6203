"""Nạp dữ liệu: dataset mẫu của scikit-learn, dataset do Admin quản lý (core/store.py) và CSV người dùng tải lên."""
import io

import numpy as np
import pandas as pd
import streamlit as st
from sklearn import datasets

from core import store

SAMPLE_DATASETS = ["Iris", "Wine", "Breast Cancer", "Digits", "Swiss Roll"]
NO_LABEL = "Không sử dụng nhãn"
LABEL_HINTS = ("label", "target", "class", "species", "nhan", "nhãn")
FEATURE_EXCLUDE = ("label", "target", "class")  # tên cột không tự đưa vào danh sách đặc trưng
CONTINUOUS_THRESHOLD = 20  # cột nhãn dạng số có nhiều hơn ngần này giá trị khác nhau → coi là nhãn liên tục


def list_datasets():
    """Dataset mẫu + dataset do Admin thêm."""
    return SAMPLE_DATASETS + store.custom_names()


def guess_label_col(df: pd.DataFrame):
    """Đoán cột nhãn theo tên cột thường gặp; không thấy thì trả về None."""
    for col in df.columns:
        if str(col).strip().lower() in LABEL_HINTS:
            return col
    return None


def is_continuous_label(labels) -> bool:
    """Nhãn dạng số thực có quá nhiều giá trị (vd. Swiss Roll) → không phải nhãn phân loại."""
    s = pd.Series(labels)
    if pd.api.types.is_bool_dtype(s) or not pd.api.types.is_numeric_dtype(s):
        return False
    return s.nunique(dropna=True) > CONTINUOUS_THRESHOLD


def read_csv_bytes(raw: bytes) -> pd.DataFrame:
    """Đọc CSV từ bytes, tự thử vài bảng mã (UTF-8, Excel tiếng Việt cp1258) và tự nhận dấu phân cách."""
    last_exc = None
    for enc in ("utf-8-sig", "cp1258", "latin-1"):
        try:
            return pd.read_csv(io.BytesIO(raw), encoding=enc, sep=None, engine="python")
        except UnicodeDecodeError as exc:
            last_exc = exc
    raise last_exc


@st.cache_data(show_spinner=False)
def _load_builtin(name: str):
    if name == "Iris":
        bunch = datasets.load_iris(as_frame=True)
        df, labels = bunch.data.copy(), pd.Series(bunch.target_names[bunch.target], name="label")
    elif name == "Wine":
        bunch = datasets.load_wine(as_frame=True)
        df, labels = bunch.data.copy(), pd.Series(bunch.target_names[bunch.target], name="label")
    elif name == "Breast Cancer":
        bunch = datasets.load_breast_cancer(as_frame=True)
        df, labels = bunch.data.copy(), pd.Series(bunch.target_names[bunch.target], name="label")
    elif name == "Digits":
        bunch = datasets.load_digits()
        df = pd.DataFrame(bunch.data, columns=[f"pixel_{i}" for i in range(bunch.data.shape[1])])
        labels = pd.Series(bunch.target.astype(str), name="label")
    else:  # Swiss Roll: nhãn là vị trí dọc theo mặt cuộn (số thực liên tục)
        X, color = datasets.make_swiss_roll(n_samples=900, noise=0.08, random_state=42)
        df = pd.DataFrame(X, columns=["x", "y", "z"])
        labels = pd.Series(color, name="label")
    df = df.reset_index(drop=True)
    df["label"] = labels.reset_index(drop=True)
    return df


@st.cache_data(show_spinner=False)
def _load_custom(name: str, file_key: str):
    # file_key (tên tệp) nằm trong khóa cache để dataset được sửa/xóa/thêm lại sẽ không bị dùng bản cũ
    return store.load_custom(name)


def load_dataset(name: str):
    """Trả về (DataFrame, tên cột nhãn mặc định hoặc None)."""
    custom = store.list_custom()
    if name in custom:
        meta = custom[name]
        df = _load_custom(name, meta["file"])
        label = meta.get("label")
        return df.copy(), (label if label in df.columns else guess_label_col(df))
    return _load_builtin(name).copy(), "label"


def clean_feature_frame(df: pd.DataFrame, feature_cols):
    X = df.loc[:, list(feature_cols)].apply(pd.to_numeric, errors="coerce")
    return X.replace([np.inf, -np.inf], np.nan)


def prepare_data(df: pd.DataFrame, feature_cols, label_col, fill_missing: bool):
    """Làm sạch đặc trưng và khớp nhãn theo từng dòng.

    Trả về (X_df, labels | None, thông tin). labels là pandas Series cùng thứ tự dòng với X_df.
    """
    X = clean_feature_frame(df, feature_cols)
    n_all = len(X)
    if fill_missing:
        X = X.fillna(X.median(numeric_only=True))
    valid = X.notna().all(axis=1)
    X = X.loc[valid]
    labels = None
    if label_col and label_col != NO_LABEL:
        labels = df.loc[X.index, label_col]
        if not is_continuous_label(labels):
            labels = labels.astype("string").fillna("(thiếu)").astype(str)
        labels = labels.reset_index(drop=True)
    X = X.reset_index(drop=True)
    return X, labels, {"dropped": int(n_all - len(X)), "total": n_all}


def scale_imbalance(X_df: pd.DataFrame):
    """Cột có độ lệch chuẩn lớn nhất và tỉ lệ so với cột nhỏ nhất (bỏ cột hằng). Dùng để cảnh báo khi chưa chuẩn hóa."""
    std = X_df.std(numeric_only=True)
    std = std[std > 0]
    if len(std) < 2:
        return None
    return std.idxmax(), float(std.max() / std.min())
