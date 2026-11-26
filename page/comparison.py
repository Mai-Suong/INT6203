import streamlit as st
import pandas as pd
import numpy as np
from core.catalog import ALGORITHMS
from core.data import SAMPLE_DATASETS, load_sample, clean_feature_frame
from core.algorithms import run_algorithm
from core.plotting import plot_embedding

def render():
    st.title("So sánh thuật toán")
    st.caption("Chạy nhiều thuật toán trên cùng một bộ dữ liệu và cùng cấu hình để quan sát sự khác biệt.")
    source = st.radio("Nguồn dữ liệu", ["Dataset có sẵn", "Tải CSV lên"], horizontal=True, key="cmp_source")
    if source == "Dataset có sẵn":
        name = st.selectbox("Dataset", SAMPLE_DATASETS, key="cmp_dataset")
        df, labels = load_sample(name)
        df = df.copy(); df["label"] = labels
        default_label = "label"
    else:
        file = st.file_uploader("Tải CSV", type=["csv"], key="cmp_upload")
        if file is None:
            st.info("Tải CSV để bắt đầu so sánh."); return
        try:
            df = pd.read_csv(file); default_label = None
        except Exception as exc:
            st.error(f"Không đọc được CSV: {exc}"); return
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    feature_options = [c for c in numeric_cols if c.lower() not in ["label", "target", "class"]]
    if not feature_options:
        feature_options = numeric_cols
    features = st.multiselect("Feature columns", feature_options, default=feature_options, key="cmp_features")
    label_options = ["Không sử dụng nhãn"] + list(df.columns)
    default = default_label if default_label in df.columns else "Không sử dụng nhãn"
    label_col = st.selectbox("Label column (tùy chọn)", label_options, index=label_options.index(default), key="cmp_label")
    algorithms = st.multiselect("Chọn thuật toán cần so sánh", list(ALGORITHMS), default=["PCA", "t-SNE"], key="cmp_algorithms")
    c1, c2 = st.columns(2)
    with c1:
        dim = st.radio("Số chiều đầu ra", ["1D", "2D", "3D"], index=1, horizontal=True, key="cmp_dim")
    with c2:
        scale = st.radio("Chuẩn hóa", ["Z-score", "Không chuẩn hóa"], horizontal=True, key="cmp_scale")
    fill = st.checkbox("Thay giá trị thiếu bằng trung vị", value=True, key="cmp_fill")
    if st.button("⚖️ Chạy so sánh", type="primary", disabled=(not features or not algorithms), use_container_width=True):
        X = clean_feature_frame(df, features)
        if "MDS" in algorithms and len(X) > 600:
            st.error("MDS trên bộ dữ liệu lớn có thể mất rất nhiều thời gian. Hãy chọn dataset nhỏ hơn hoặc giảm số dòng CSV xuống tối đa 600.")
            return
        if fill: X = X.fillna(X.median(numeric_only=True))
        valid = X.notna().all(axis=1); X = X.loc[valid]
        y = df.loc[valid, label_col].astype(str).to_numpy() if label_col != "Không sử dụng nhãn" else None
        if len(X) < 3:
            st.error("Cần ít nhất 3 dòng dữ liệu hợp lệ."); return
        output = []
        progress = st.progress(0)
        for i, algo in enumerate(algorithms):
            try:
                Z, actual_k, variance, elapsed = run_algorithm(algo, X.to_numpy(), int(dim[0]), y=y, standardize=(scale == "Z-score"))
                output.append((algo, Z, actual_k, elapsed, variance, None))
            except Exception as exc:
                output.append((algo, None, None, None, None, str(exc)))
            progress.progress((i + 1) / len(algorithms))
        st.session_state.comparison_output = output
        st.session_state.comparison_labels = y
    if "comparison_output" in st.session_state:
        st.markdown("---")
        st.markdown("### Kết quả so sánh")
        y = st.session_state.get("comparison_labels")
        output = st.session_state.comparison_output
        cols = st.columns(2)
        for i, (algo, Z, k, elapsed, variance, error) in enumerate(output):
            with cols[i % 2]:
                st.markdown(f"**{algo}**")
                if error:
                    st.warning(f"{algo}: {error}")
                else:
                    st.plotly_chart(plot_embedding(Z, y, k, f"{algo} · {k}D"), use_container_width=True)
                    st.caption(f"Thời gian: {elapsed:.2f} ms" + (f" · Phương sai giữ lại: {variance.sum():.2f}%" if variance is not None else ""))

render()
