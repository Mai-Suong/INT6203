"""Quy trình chạy thí nghiệm dùng chung cho trang Trực quan hóa và So sánh."""
import json

import numpy as np
import streamlit as st

from core.algorithms import label_separation, run_algorithm
from core.data import is_continuous_label

# Một số thuật toán quá chậm/tốn RAM với dữ liệu lớn → tự lấy mẫu ngẫu nhiên (có thông báo).
MAX_ROWS = {"MDS": 600, "t-SNE": 5000, "Isomap": 5000, "LLE": 8000, "Kernel PCA": 5000, "UMAP": 30000}


@st.cache_data(show_spinner=False, max_entries=64)
def _cached_run(algo, X, n_components, y, standardize, params_json):
    return run_algorithm(algo, X, n_components, y=y, standardize=standardize, params=json.loads(params_json))


def run_experiment(algo, X_df, labels, n_components, standardize, params=None):
    """Chạy 1 thuật toán. Trả về dict kết quả kèm nhãn (đã khớp với các dòng được dùng)."""
    n = len(X_df)
    notes = []
    idx = np.arange(n)
    cap = MAX_ROWS.get(algo)
    if cap and n > cap:
        idx = np.sort(np.random.default_rng(42).choice(n, cap, replace=False))
        notes.append(f"{algo} chậm với dữ liệu lớn nên đã lấy ngẫu nhiên {cap:,}/{n:,} mẫu.")
    X = X_df.to_numpy(dtype=float)[idx]
    lab = labels.iloc[idx].reset_index(drop=True) if labels is not None else None

    y = None
    if algo == "LDA":
        if lab is None:
            raise ValueError("LDA cần cột nhãn. Hãy chọn Label column.")
        if is_continuous_label(lab):
            raise ValueError("LDA cần nhãn phân loại; cột nhãn đang chọn là số liên tục (nhiều giá trị khác nhau).")
        y = lab.astype(str).to_numpy()

    res = dict(_cached_run(algo, X, int(n_components), y, bool(standardize), json.dumps(params or {}, sort_keys=True)))
    res["labels"] = lab
    res["silhouette"] = label_separation(res["Z"], lab)
    res["n_rows"] = len(idx)
    res["notes"] = notes + list(res["notes"])
    return res
