import numpy as np
import pandas as pd
import streamlit as st

from core.catalog import ALGORITHMS
from core.data import FEATURE_EXCLUDE, NO_LABEL, is_continuous_label, prepare_data
from core.datasource import dataset_picker
from core.pipeline import run_experiment
from core.plotting import plot_embedding


def render():
    st.title("So sánh thuật toán")

    src = dataset_picker("cmp")
    if src is None:
        return
    df, name = src["df"], str(src["name"])
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.error("Dataset cần có ít nhất một cột dữ liệu dạng số.")
        return

    label_options = [NO_LABEL] + list(df.columns)
    default = src["label"] if src["label"] in df.columns else NO_LABEL
    label_col = st.selectbox("Label column (tùy chọn)", label_options, index=label_options.index(default), key=f"cmp_label_{name}")
    feature_options = [c for c in numeric_cols if c != label_col and str(c).lower() not in FEATURE_EXCLUDE] or \
                      [c for c in numeric_cols if c != label_col] or numeric_cols
    features = st.multiselect("Feature columns", feature_options, default=feature_options, key=f"cmp_features_{name}_{label_col}")
    algorithms = st.multiselect("Chọn thuật toán cần so sánh", list(ALGORITHMS), default=["PCA", "t-SNE"], key="cmp_algorithms")
    c1, c2 = st.columns(2)
    dim = c1.radio("Số chiều đầu ra", ["1D", "2D", "3D"], index=1, horizontal=True, key="cmp_dim")
    scale = c2.radio("Chuẩn hóa", ["Z-score", "Không chuẩn hóa"], horizontal=True, key="cmp_scale")
    fill = st.checkbox("Thay giá trị thiếu bằng trung vị", value=True, key="cmp_fill")

    if "LDA" in algorithms and (label_col == NO_LABEL or is_continuous_label(df[label_col])):
        st.warning("LDA cần cột nhãn phân loại. Nếu giữ LDA trong danh sách, nó sẽ báo lỗi riêng và các thuật toán khác vẫn chạy bình thường.")

    if st.button("⚖️ Chạy so sánh", type="primary", disabled=(not features or not algorithms), width="stretch"):
        X, labels, prep = prepare_data(df, features, label_col, fill)
        if len(X) < 3:
            st.error("Cần ít nhất 3 dòng dữ liệu hợp lệ.")
            return
        output = []
        progress = st.progress(0.0, text="Đang chạy...")
        for i, algo in enumerate(algorithms):
            progress.progress(i / len(algorithms), text=f"Đang chạy {algo}...")
            try:
                res = run_experiment(algo, X, labels, int(dim[0]), scale == "Z-score")
                res["algo"], res["error"] = algo, None
            except Exception as exc:
                res = {"algo": algo, "error": str(exc)}
            output.append(res)
        progress.empty()
        st.session_state.comparison_output = output
        st.session_state.comparison_meta = {"dataset": name, "label": label_col, "scale": scale, "dim": dim}

    output = st.session_state.get("comparison_output")
    if not output:
        return
    meta = st.session_state.get("comparison_meta", {})
    st.markdown("---")
    st.markdown("### Kết quả so sánh")
    st.caption(f"Dataset: **{meta.get('dataset')}** · {meta.get('dim')} · {meta.get('scale')}")

    rows = []
    for r in output:
        if r["error"]:
            rows.append({"Thuật toán": r["algo"], "Trạng thái": "Lỗi", "Thời gian (ms)": None, "Trustworthiness": None,
                         "Silhouette": None, "Số mẫu": None})
        else:
            rows.append({"Thuật toán": r["algo"], "Trạng thái": "OK", "Thời gian (ms)": round(r["elapsed"], 1),
                         "Trustworthiness": None if r["trust"] is None else round(r["trust"], 3),
                         "Silhouette": None if r["silhouette"] is None else round(r["silhouette"], 3),
                         "Số mẫu": r["n_rows"]})
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    st.caption("Trustworthiness càng gần 1 thì cấu trúc láng giềng được giữ càng tốt. Silhouette đo độ tách giữa các lớp theo nhãn "
               "(LDA học trực tiếp từ nhãn nên chỉ số này hiển nhiên cao).")

    cols = st.columns(2)
    for i, r in enumerate(output):
        with cols[i % 2]:
            st.markdown(f"**{r['algo']}**")
            if r["error"]:
                st.warning(f"{r['algo']}: {r['error']}")
                continue
            for note in r["notes"]:
                st.caption(f"⚠️ {note}")
            st.plotly_chart(plot_embedding(r["Z"], r["labels"], r["k"], f"{r['algo']} · {r['k']}D"),
                            width="stretch", theme=None, key=f"cmp_plot_{i}")
            extra = f" · Phương sai giữ lại: {r['variance'].sum():.2f}%" if r["variance"] is not None else ""
            st.caption(f"Thời gian: {r['elapsed']:.1f} ms" + extra)


render()
