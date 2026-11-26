import streamlit as st
from core.catalog import ALGORITHMS

def render():
    st.title("Khám phá thuật toán")
    st.caption("Chọn một trong 9 thuật toán để mở trang thực nghiệm riêng. Trang chi tiết tập trung vào thao tác và biểu đồ, không lặp lại phần lý thuyết dài.")
    query = st.text_input("Tìm kiếm thuật toán", placeholder="Nhập PCA, t-SNE hoặc tên đầy đủ...")
    filtered = [(k, v) for k, v in ALGORITHMS.items() if query.lower() in k.lower() or query.lower() in v['full'].lower() or query.lower() in v['vi'].lower()]
    if not filtered:
        st.info("Không tìm thấy thuật toán phù hợp.")
        return
    cols = st.columns(3)
    for i, (key, info) in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(f"<div class='algo-card'><div class='algo-code'>{key}</div><div class='algo-full'>{info['full']}</div><div class='algo-desc'>{info['desc']}</div><span style='display:inline-block;background:{'#eaf2ff' if info['group']=='Linear' else '#f1eafe'};color:{'#1d4ed8' if info['group']=='Linear' else '#7c3aed'};padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700'>{info['group']}</span></div>", unsafe_allow_html=True)
            if st.button(f"Mở trực quan hóa {key} →", key=f"open_{key}", type="primary", use_container_width=True):
                st.session_state.selected_algorithm = key
                st.switch_page("page/algorithm.py")

render()
