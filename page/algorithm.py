import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from core.catalog import ALGORITHMS
from core.data import SAMPLE_DATASETS, load_sample, clean_feature_frame
from core.algorithms import run_algorithm
from core.plotting import plot_embedding


def render():
    algo = st.session_state.get("selected_algorithm", "PCA")
    if algo not in ALGORITHMS:
        algo = "PCA"
    info = ALGORITHMS[algo]
    st.markdown(f"# {algo} Visualization")
    st.caption(f"{info['full']} · {info['vi']} · {info['group']}")
    st.markdown("---")

    st.markdown("### 01 · Chọn dữ liệu")
    source = st.radio("Nguồn dữ liệu", ["Dataset có sẵn", "Tải CSV lên"], horizontal=True, key=f"source_{algo}")
    df = None
    data_identifier = ""
    if source == "Dataset có sẵn":
        current = st.session_state.get("dataset_name", "Iris")
        default_index = SAMPLE_DATASETS.index(current) if current in SAMPLE_DATASETS else 0
        dataset_name = st.selectbox("Dataset", SAMPLE_DATASETS, index=default_index, key=f"sample_{algo}")
        data_identifier = dataset_name
        df, default_labels = load_sample(dataset_name)
        df = df.copy()
        df["label"] = default_labels
        default_label_col = "label"
    else:
        uploaded = st.file_uploader("Tải tệp dữ liệu CSV", type=["csv"], key=f"upload_{algo}")
        if uploaded is not None:
            data_identifier = uploaded.name
            try:
                df = pd.read_csv(uploaded)
                default_label_col = None
            except Exception as exc:
                st.error(f"Không thể đọc tệp CSV: {exc}")
                return
        else:
            st.info("Vui lòng tải lên tệp CSV để tiếp tục.")
            return

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.error("Dataset cần có ít nhất một cột dữ liệu dạng số để giảm chiều.")
        return
    st.caption(f"Dữ liệu hiện có **{len(df):,} mẫu** và **{len(df.columns)} cột**.")
    with st.expander("Xem trước dữ liệu", expanded=False):
        st.dataframe(df.head(8), use_container_width=True)

    st.markdown("### 02 · Cấu hình dữ liệu")
    feature_options = [c for c in numeric_cols if c.lower() not in ["label", "target", "class"]]
    if not feature_options:
        feature_options = numeric_cols
    feature_cols = st.multiselect("Feature columns · Các cột đặc trưng", feature_options, default=feature_options, key=f"features_{algo}")
    label_options = ["Không sử dụng nhãn"] + list(df.columns)
    default_label = default_label_col if default_label_col in df.columns else "Không sử dụng nhãn"
    label_col = st.selectbox("Label column · Cột nhãn (tùy chọn)", label_options, index=label_options.index(default_label), key=f"label_{algo}")
    fill_missing = st.checkbox("Thay giá trị thiếu bằng trung vị của từng cột", value=True, key=f"missing_{algo}")

    st.markdown("### 03 · Cấu hình trực quan hóa")
    c1, c2 = st.columns(2)
    with c1:
        dim_label = st.radio("Số chiều đầu ra", ["1D", "2D", "3D"], index=1, horizontal=True, key=f"dim_{algo}")
        n_components = int(dim_label[0])
    with c2:
        compare_mode = st.radio("Chuẩn hóa Z-score", ["So sánh cả hai", "Chỉ dữ liệu gốc", "Chỉ dữ liệu Z-score"], index=0, key=f"scale_{algo}")

    if algo == "LDA" and label_col == "Không sử dụng nhãn":
        st.warning("LDA là thuật toán có giám sát. Bà cần chọn Label column để chạy LDA.")
    if not feature_cols:
        st.warning("Hãy chọn ít nhất một Feature column.")
    config_signature = (algo, source, data_identifier, tuple(feature_cols), label_col, dim_label, compare_mode, fill_missing)
    if st.button(f"🚀 Run {algo}", type="primary", disabled=(not feature_cols or (algo == "LDA" and label_col == "Không sử dụng nhãn")), use_container_width=True):
        X_df = clean_feature_frame(df, feature_cols)
        if algo == "MDS" and len(X_df) > 600:
            st.error("MDS trên bộ dữ liệu lớn có thể mất rất nhiều thời gian. Hãy chọn dataset nhỏ hơn hoặc giảm số dòng CSV xuống tối đa 600.")
            return
        if fill_missing:
            X_df = X_df.fillna(X_df.median(numeric_only=True))
        valid_rows = X_df.notna().all(axis=1)
        X_df = X_df.loc[valid_rows]
        y = df.loc[valid_rows, label_col].astype(str).to_numpy() if label_col != "Không sử dụng nhãn" else None
        if len(X_df) < 3:
            st.error("Cần ít nhất 3 dòng dữ liệu hợp lệ.")
            return
        if X_df.shape[1] < 1:
            st.error("Không có cột đặc trưng hợp lệ.")
            return
        variants = []
        if compare_mode in ["So sánh cả hai", "Chỉ dữ liệu gốc"]:
            variants.append(("Raw Data", False))
        if compare_mode in ["So sánh cả hai", "Chỉ dữ liệu Z-score"]:
            variants.append(("Z-score Standardization", True))
        results = []
        st.session_state.pop(f"result_{algo}", None)
        try:
            with st.spinner(f"Đang chạy {algo}..."):
                for title, standardized in variants:
                    Z, actual_k, variance, elapsed = run_algorithm(algo, X_df.to_numpy(), n_components, y=y, standardize=standardized)
                    results.append({"title": title, "Z": Z, "k": actual_k, "variance": variance, "elapsed": elapsed})
            st.session_state[f"result_{algo}"] = results
            st.session_state[f"labels_{algo}"] = y
            st.session_state[f"signature_{algo}"] = config_signature
            st.session_state[f"result_meta_{algo}"] = {"requested": n_components, "rows": len(X_df), "features": len(feature_cols), "label": label_col}
        except Exception as exc:
            st.error(f"Không thể chạy thuật toán: {exc}")
            return

    results = st.session_state.get(f"result_{algo}")
    if st.session_state.get(f"signature_{algo}") != config_signature:
        results = None
    if results:
        meta = st.session_state.get(f"result_meta_{algo}", {})
        st.markdown("---")
        st.markdown("### 04 · Kết quả trực quan hóa")
        if any(r["k"] != meta.get("requested") for r in results):
            st.info(f"Số chiều đầu ra được giới hạn theo đặc điểm thuật toán/dữ liệu. Kết quả hiện có {results[0]['k']} chiều.")
        m1, m2, m3 = st.columns(3)
        m1.metric("Số mẫu sử dụng", f"{meta.get('rows', 0):,}")
        m2.metric("Số chiều đầu vào", meta.get("features", 0))
        m3.metric("Số chiều đầu ra", results[0]["k"])
        plot_cols = st.columns(len(results))
        y_plot = st.session_state.get(f"labels_{algo}")
        for col, result in zip(plot_cols, results):
            with col:
                st.markdown(f"**{result['title']}**")
                fig = plot_embedding(result["Z"], y_plot, result["k"], f"{algo} · {result['title']}")
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Thời gian thực thi: {result['elapsed']:.2f} ms")
                if result["variance"] is not None:
                    st.caption(f"Phương sai giữ lại (cộng dồn): {result['variance'].sum():.2f}%")
        if algo == "LDA":
            st.caption("LDA sử dụng nhãn lớp trong quá trình học. Với thuật toán không giám sát, nhãn chỉ được dùng để tô màu biểu đồ nếu người dùng chọn.")
        elif algo in ["PCA", "SVD"]:
            st.caption("Phương sai giữ lại là chỉ số đặc thù của PCA/SVD; các thuật toán khác không nhất thiết có chỉ số tương đương.")

render()
