import json

import numpy as np
import pandas as pd
import streamlit as st

from core.algorithms import variance_curve
from core.catalog import ALGORITHMS, param_specs
from core.data import FEATURE_EXCLUDE, NO_LABEL, clean_feature_frame, is_continuous_label, prepare_data, scale_imbalance
from core.datasource import dataset_picker
from core.pipeline import run_experiment
from core.plotting import plot_embedding, plot_scree
from core.ui import render_param_inputs

SCALE_SENSITIVE_NOTE = {
    "Kernel PCA": "Với Kernel PCA (rbf), dữ liệu chưa chuẩn hóa thường làm kernel gần như ma trận đơn vị, kết quả mất cấu trúc.",
}


def render():
    names = list(ALGORITHMS)
    current = st.session_state.get("selected_algorithm", "PCA")
    if current not in ALGORITHMS:
        current = "PCA"
    algo = st.selectbox("Thuật toán", names, index=names.index(current),
                        format_func=lambda a: f"{a} · {ALGORITHMS[a]['vi']}")
    st.session_state.selected_algorithm = algo
    info = ALGORITHMS[algo]

    st.markdown(f"# {algo} Visualization")

    with st.expander(f"📘 Lý thuyết nhanh: {algo}"):
        st.markdown(info["idea"])
        st.code(info["formula"], language=None)
        a, b = st.columns(2)
        a.markdown("**Ưu điểm**\n" + "\n".join(f"- {t}" for t in info["pros"]))
        b.markdown("**Hạn chế**\n" + "\n".join(f"- {t}" for t in info["cons"]))
        st.info(f"💡 {info['tip']}")

    # ---------------- 01 · Dữ liệu ----------------
    st.markdown("### 01 · Chọn dữ liệu")
    src = dataset_picker("viz")
    if src is None:
        return
    df, name = src["df"], str(src["name"])
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.error("Dataset cần có ít nhất một cột dữ liệu dạng số để giảm chiều.")
        return
    st.caption(f"Dữ liệu hiện có **{len(df):,} mẫu** và **{len(df.columns)} cột**.")
    with st.expander("Xem trước dữ liệu", expanded=False):
        st.dataframe(df.head(8), width="stretch")

    # ---------------- 02 · Cấu hình dữ liệu ----------------
    st.markdown("### 02 · Cấu hình dữ liệu")
    label_options = [NO_LABEL] + list(df.columns)
    default_label = src["label"] if src["label"] in df.columns else NO_LABEL
    label_col = st.selectbox("Label column · Cột nhãn (tùy chọn)", label_options, index=label_options.index(default_label),
                             key=f"viz_label_{name}")
    feature_options = [c for c in numeric_cols if c != label_col and str(c).lower() not in FEATURE_EXCLUDE] or \
                      [c for c in numeric_cols if c != label_col] or numeric_cols
    feature_cols = st.multiselect("Feature columns · Các cột đặc trưng", feature_options, default=feature_options,
                                  key=f"viz_feat_{name}_{label_col}")
    fill_missing = st.checkbox("Thay giá trị thiếu bằng trung vị của từng cột (bỏ chọn: loại các dòng thiếu)", value=True, key="viz_fill")

    label_continuous = label_col != NO_LABEL and is_continuous_label(df[label_col])
    if label_continuous:
        st.caption(f"Cột nhãn **{label_col}** là số liên tục nên biểu đồ được tô bằng thang màu (không chia thành các lớp).")

    # ---------------- 03 · Cấu hình trực quan hóa ----------------
    st.markdown("### 03 · Cấu hình trực quan hóa")
    c1, c2 = st.columns(2)
    with c1:
        dim_label = st.radio("Số chiều đầu ra", ["1D", "2D", "3D"], index=1, horizontal=True, key=f"dim_{algo}")
        n_components = int(dim_label[0])
    with c2:
        compare_mode = st.radio("Chuẩn hóa Z-score", ["So sánh cả hai", "Chỉ dữ liệu gốc", "Chỉ dữ liệu Z-score"],
                                index=0, key=f"scale_{algo}")

    specs = param_specs(algo, len(df), max(1, len(feature_cols)), n_components)
    params = {}
    if specs:
        with st.expander(f"⚙️ Tham số của {algo}", expanded=True):
            params = render_param_inputs(algo, specs, f"viz_{name}_{len(df)}_{n_components}")
    else:
        st.caption(f"{algo} không có tham số điều chỉnh. Kết quả là xác định cho cùng dữ liệu và cấu hình.")

    if feature_cols and compare_mode != "Chỉ dữ liệu Z-score" and algo != "LDA":
        imb = scale_imbalance(clean_feature_frame(df, feature_cols))
        if imb and imb[1] > 10:
            extra = SCALE_SENSITIVE_NOTE.get(algo, "")
            st.info(f"Các đặc trưng có thang đo chênh lệch ≈ {imb[1]:,.0f} lần (cột **{imb[0]}** lớn nhất), "
                    f"nên dữ liệu gốc có thể bị cột này chi phối. {extra} Hãy so sánh với Z-score.")
    if algo == "LDA" and label_col == NO_LABEL:
        st.warning("LDA là thuật toán có giám sát. Bạn cần chọn Label column để chạy LDA.")
    if algo == "LDA" and label_continuous:
        st.warning("LDA cần nhãn phân loại; cột nhãn đang chọn là số liên tục nên LDA không chạy được.")
    if not feature_cols:
        st.warning("Hãy chọn ít nhất một Feature column.")

    config_signature = (algo, name, tuple(feature_cols), label_col, dim_label, compare_mode, fill_missing,
                        json.dumps(params, sort_keys=True, default=str))
    blocked = (not feature_cols) or (algo == "LDA" and (label_col == NO_LABEL or label_continuous))
    if st.button(f"🚀 Run {algo}", type="primary", disabled=blocked, width="stretch"):
        X_df, labels, prep = prepare_data(df, feature_cols, label_col, fill_missing)
        if len(X_df) < 3:
            st.error("Cần ít nhất 3 dòng dữ liệu hợp lệ.")
            return
        variants = []
        if compare_mode in ("So sánh cả hai", "Chỉ dữ liệu gốc"):
            variants.append(("Raw Data", False))
        if compare_mode in ("So sánh cả hai", "Chỉ dữ liệu Z-score"):
            variants.append(("Z-score Standardization", True))
        st.session_state.pop(f"result_{algo}", None)
        results = []
        try:
            with st.spinner(f"Đang chạy {algo}..."):
                for title, standardized in variants:
                    res = run_experiment(algo, X_df, labels, n_components, standardized, params)
                    res["title"] = title
                    if algo in ("PCA", "SVD"):
                        res["scree"] = variance_curve(algo, X_df.to_numpy(), standardized)
                    results.append(res)
        except Exception as exc:
            st.error(f"Không thể chạy thuật toán: {exc}")
            return
        st.session_state[f"result_{algo}"] = results
        st.session_state[f"signature_{algo}"] = config_signature
        st.session_state[f"meta_{algo}"] = {"requested": n_components, "features": len(feature_cols), "dropped": prep["dropped"],
                                            "label": label_col, "dataset": name}

    # ---------------- 04 · Kết quả ----------------
    results = st.session_state.get(f"result_{algo}")
    if st.session_state.get(f"signature_{algo}") != config_signature:
        results = None
    if not results:
        return
    meta = st.session_state[f"meta_{algo}"]
    st.markdown("---")
    st.markdown("### 04 · Kết quả trực quan hóa")
    if any(r["k"] != meta["requested"] for r in results):
        st.info(f"Số chiều đầu ra được giới hạn theo đặc điểm thuật toán/dữ liệu. Kết quả hiện có {results[0]['k']} chiều.")
    if meta["dropped"]:
        st.caption(f"Đã loại {meta['dropped']:,} dòng có giá trị thiếu/không hợp lệ.")
    seen = set()
    for r in results:
        for note in r["notes"]:
            if note not in seen:
                seen.add(note)
                st.warning(note)

    m1, m2, m3 = st.columns(3)
    m1.metric("Số mẫu sử dụng", f"{results[0]['n_rows']:,}")
    m2.metric("Số chiều đầu vào", meta["features"])
    m3.metric("Số chiều đầu ra", results[0]["k"])

    plot_cols = st.columns(len(results))
    for i, (col, r) in enumerate(zip(plot_cols, results)):
        with col:
            st.markdown(f"**{r['title']}**")
            st.plotly_chart(plot_embedding(r["Z"], r["labels"], r["k"], f"{algo} · {r['title']}",
                                           label_name=str(meta["label"]) if meta["label"] != NO_LABEL else "Nhãn"),
                            width="stretch", theme=None, key=f"plot_{algo}_{i}")
            lines = [f"⏱ Thời gian: {r['elapsed']:.1f} ms"]
            if r["trust"] is not None:
                lines.append(f"Trustworthiness: {r['trust']:.3f}")
            if r["silhouette"] is not None:
                lines.append(f"Silhouette (theo nhãn): {r['silhouette']:.3f}")
            if r["variance"] is not None:
                lines.append(f"Phương sai giữ lại: {r['variance'].sum():.2f}%")
            st.caption(" · ".join(lines))

    with st.expander("Cách đọc các chỉ số"):
        st.markdown(
            "- **Trustworthiness (0–1)**: các láng giềng gần trong biểu đồ có thật sự gần nhau ở dữ liệu gốc không. Càng gần 1 càng đáng tin. Chỉ số đo trong không gian dữ liệu mà thuật toán nhìn thấy (gốc hoặc Z-score), nên đừng so sánh trực tiếp giữa Raw và Z-score.\n"
            "- **Silhouette (−1…1)**: các lớp có tách khỏi nhau trên biểu đồ không. Chỉ có khi chọn nhãn phân loại; "
            "với LDA chỉ số này hiển nhiên cao vì LDA học trực tiếp từ nhãn.\n"
            "- **Phương sai giữ lại**: chỉ PCA/SVD có; các thuật toán phi tuyến không có chỉ số tương đương.")

    if algo in ("PCA", "SVD"):
        with st.expander("📉 Scree plot · phương sai của từng thành phần", expanded=True):
            sc = st.columns(len(results))
            for i, (col, r) in enumerate(zip(sc, results)):
                with col:
                    st.plotly_chart(plot_scree(r["scree"], f"{algo} · {r['title']}"), width="stretch", theme=None, key=f"scree_{algo}_{i}")
        if algo == "SVD":
            st.caption("TruncatedSVD không trừ trung bình cột, nên 'phương sai giữ lại' của SVD thường thấp hơn PCA trên dữ liệu chưa chuẩn hóa. Với dữ liệu đã Z-score hai kết quả gần như trùng nhau.")
    elif algo == "LDA":
        st.caption("LDA sử dụng nhãn lớp trong quá trình học. Việc co giãn từng đặc trưng gần như không đổi không gian phân biệt, nên Raw và Z-score thường cho bố cục rất giống nhau.")
    elif info["supervised"] is False:
        st.caption("Thuật toán không giám sát: nhãn chỉ dùng để tô màu biểu đồ, không tham gia vào quá trình học.")

    export = pd.DataFrame({"Mẫu": np.arange(results[0]["n_rows"])})
    if results[0]["labels"] is not None:
        export["Nhãn"] = np.asarray(results[0]["labels"])
    for r in results:
        tag = "raw" if r["title"] == "Raw Data" else "zscore"
        for d in range(r["Z"].shape[1]):
            export[f"{tag}_dim{d + 1}"] = r["Z"][:, d]
    st.download_button("⬇️ Tải embedding (CSV)", export.to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"{algo.replace(' ', '_')}_embedding.csv", mime="text/csv")


render()
