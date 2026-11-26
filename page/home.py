import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.datasets import make_blobs
from core.catalog import ALGORITHMS

def render():
    left, right = st.columns([1.2, 1], vertical_alignment="center")
    with left:
        st.markdown("""<section class='hero'><div style='color:#2563eb;font-weight:700;font-size:13px;letter-spacing:1px'>DIMENSIONALITY REDUCTION LAB</div>
        <h1>Khám phá dữ liệu đa chiều bằng trực quan hóa</h1>
        <p style='font-size:16px;color:#52627a;max-width:700px'>DimViz hỗ trợ thực nghiệm và so sánh các thuật toán giảm chiều dữ liệu thông qua biểu đồ tương tác 1D, 2D và 3D.</p></section>""", unsafe_allow_html=True)
        st.write("")
        a, b = st.columns(2)
        with a:
            if st.button("🚀 Bắt đầu thực nghiệm", type="primary", use_container_width=True):
                st.session_state.selected_algorithm = "PCA"
                st.switch_page("page/algorithm.py")
        with b:
            if st.button("Khám phá thuật toán →", use_container_width=True):
                st.switch_page("page/explore.py")
    with right:
        X, labels = make_blobs(n_samples=100, centers=3, n_features=2, cluster_std=1.15, random_state=12)
        chart_df = pd.DataFrame(X, columns=["Dim 1", "Dim 2"])
        chart_df["Nhóm"] = labels.astype(str)
        fig = px.scatter(chart_df, x="Dim 1", y="Dim 2", color="Nhóm", title="Minh họa dữ liệu sau giảm chiều")
        fig.update_traces(marker=dict(size=8, opacity=.8))
        fig.update_layout(height=300, margin=dict(l=8, r=8, t=48, b=8), legend_title_text="Nhóm")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Biểu đồ minh họa bố cục, không phải kết quả chạy thuật toán thực tế.")

    st.markdown("### Từ dữ liệu nhiều chiều đến không gian dễ quan sát")
    flow = st.columns([1, .3, 1, .3, 1])
    with flow[0]:
        st.markdown("<div class='algo-card' style='text-align:center;background:#BCFEFE;border:1px solid #001C44;color:#001C44'><div style='font-size:28px'>▦</div><b>High-dimensional data</b><p style='color:#0C5776;margin-top:6px'>Nhiều đặc trưng</p></div>", unsafe_allow_html=True)
    with flow[1]:
        st.markdown("<div style='text-align:center;padding-top:30px;color:#2563eb;font-size:24px'>→</div>", unsafe_allow_html=True)
    with flow[2]:
        st.markdown("<div class='algo-card' style='text-align:center;background:#F8DAD0;border:1px solid #0C5776;color:#001C44'><div style='font-size:28px'>✦</div><b>Dimensionality reduction</b><p style='color:#0C5776;margin-top:6px'>Biến đổi dữ liệu</p></div>", unsafe_allow_html=True)
    with flow[3]:
        st.markdown("<div style='text-align:center;padding-top:30px;color:#2563eb;font-size:24px'>→</div>", unsafe_allow_html=True)
    with flow[4]:
        st.markdown("<div class='algo-card' style='text-align:center;background:#BCFEFE;border:1px solid #001C44;color:#001C44'><div style='font-size:28px'>◉</div><b>2D / 3D space</b><p style='color:#0C5776;margin-top:6px'>Trực quan hóa</p></div>", unsafe_allow_html=True)

    st.markdown("### Các chức năng chính")
    cols = st.columns(4)
    items = [("🗃️", "Quản lý dữ liệu", "Chọn dataset mẫu hoặc tải tệp CSV."), ("🧩", "Khám phá thuật toán", "Tìm hiểu nhanh 9 phương pháp giảm chiều."), ("📊", "Trực quan hóa", "Chạy thuật toán và xem biểu đồ 1D/2D/3D."), ("⚖️", "So sánh", "Đối chiếu kết quả trước và sau chuẩn hóa.")]
    for col, (ico, title, desc) in zip(cols, items):
        with col:
            st.markdown(
                f"""
                <div class='feature-card'>
                    <div style='font-size:25px'>{ico}</div>
                    <b style='font-size:23px'>{title}</b>
                    <p class='muted' style='font-size:17px'>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### 9 thuật toán được hỗ trợ")
    cols = st.columns(3)
    for i, (key, info) in enumerate(ALGORITHMS.items()):
        with cols[i % 3]:
            st.markdown(f"<div class='algo-card'><div class='algo-code'>{key}</div><div class='algo-full'>{info['full']}</div><div class='algo-desc'>{info['desc']}</div></div>", unsafe_allow_html=True)
            if st.button(f"Trực quan hóa {key} →", key=f"home_{key}", use_container_width=True):
                st.session_state.selected_algorithm = key
                st.switch_page("page/algorithm.py")

render()