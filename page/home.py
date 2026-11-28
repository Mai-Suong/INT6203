import streamlit as st

from core.catalog import ALGORITHMS
from core.data import load_dataset
from core.pipeline import run_experiment
from core.plotting import plot_embedding


def _flow_card(icon, title, sub, bg):
    return (f"<div class='algo-card' style='text-align:center;background:{bg};min-height:150px'>"
            f"<div style='font-size:28px'>{icon}</div><b style='color:#001C44'>{title}</b>"
            f"<p style='color:#0C5776;margin-top:6px'>{sub}</p></div>")


def render():
    left, right = st.columns([1.2, 1], vertical_alignment="center", gap="large")
    with left:
        st.markdown("""<section class='hero'><div style='color:#2563eb;font-weight:700;font-size:13px;letter-spacing:1px'>DIMENSIONALITY REDUCTION LAB</div>
        <h1>Khám phá dữ liệu đa chiều bằng trực quan hóa</h1>
        <p style='font-size:16px;color:#52627a;max-width:700px'>DimViz hỗ trợ thực nghiệm và so sánh 9 thuật toán giảm chiều dữ liệu thông qua biểu đồ tương tác 1D, 2D và 3D.</p></section>""",
                    unsafe_allow_html=True)
        a, b = st.columns(2)
        with a:
            if st.button("🚀 Bắt đầu thực nghiệm", type="primary", width="stretch"):
                st.session_state.selected_algorithm = "PCA"
                st.switch_page("page/algorithm.py")
        with b:
            if st.button("Khám phá thuật toán →", width="stretch"):
                st.switch_page("page/explore.py")
    with right:
        # Kết quả thật: PCA (Z-score) trên bộ Iris, có cache nên không tốn thời gian ở các lần sau
        df, label = load_dataset("Iris")
        res = run_experiment("PCA", df.drop(columns=[label]), df[label], 2, True)
        fig = plot_embedding(res["Z"], res["labels"], 2, "Iris: 4 chiều → 2 chiều (PCA, Z-score)", "Loài")
        fig.update_layout(height=320)
        st.plotly_chart(fig, width="stretch", theme=None)

    st.markdown("### Từ dữ liệu nhiều chiều đến không gian dễ quan sát")
    flow = st.columns([1, .25, 1, .25, 1], vertical_alignment="center")
    arrow = "<div style='text-align:center;color:#2563eb;font-size:28px'>→</div>"
    flow[0].markdown(_flow_card("▦", "High-dimensional data", "Nhiều đặc trưng", "#BCFEFE"), unsafe_allow_html=True)
    flow[1].markdown(arrow, unsafe_allow_html=True)
    flow[2].markdown(_flow_card("✦", "Dimensionality reduction", "Biến đổi dữ liệu", "#F8DAD0"), unsafe_allow_html=True)
    flow[3].markdown(arrow, unsafe_allow_html=True)
    flow[4].markdown(_flow_card("◉", "1D / 2D / 3D space", "Trực quan hóa", "#BCFEFE"), unsafe_allow_html=True)

    st.markdown("### Các chức năng chính")
    cols = st.columns(4)
    items = [("🗃️", "Quản lý dữ liệu", "Chọn dataset mẫu hoặc tải tệp CSV.", "page/data_page.py"),
             ("🧩", "Khám phá thuật toán", "Tìm hiểu nhanh 9 phương pháp giảm chiều.", "page/explore.py"),
             ("📊", "Trực quan hóa", "Chạy thuật toán, chỉnh tham số, xem biểu đồ 1D/2D/3D.", "page/algorithm.py"),
             ("⚖️", "So sánh", "Đối chiếu nhiều thuật toán, có chỉ số chất lượng.", "page/comparison.py")]
    for i, (col, (ico, title, desc, target)) in enumerate(zip(cols, items)):
        with col:
            # Cả thẻ bấm được: st.page_link chuyển trang giống thanh menu (CSS ở core/ui.py, lớp st-key-feat_*)
            with st.container(key=f"feat_{i}"):
                st.page_link(target, label=title, icon=ico)
                st.markdown(desc)

    st.markdown("### 9 thuật toán được hỗ trợ")
    cols = st.columns(3)
    for i, (key, info) in enumerate(ALGORITHMS.items()):
        with cols[i % 3]:
            st.markdown(f"<div class='algo-card'><div class='algo-code'>{key}</div><div class='algo-full'>{info['full']}</div>"
                        f"<div class='algo-desc'>{info['desc']}</div></div>", unsafe_allow_html=True)
            if st.button(f"Trực quan hóa {key} →", key=f"home_{key}", width="stretch"):
                st.session_state.selected_algorithm = key
                st.switch_page("page/algorithm.py")


render()
