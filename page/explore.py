import streamlit as st

from core.catalog import ALGORITHMS

TAGS = {"Linear": ("#eaf2ff", "#1d4ed8"), "Nonlinear": ("#f1eafe", "#7c3aed")}


def render():
    st.title("Khám phá thuật toán")
    c1, c2 = st.columns([3, 1.4])
    query = c1.text_input("Tìm kiếm thuật toán", placeholder="Nhập PCA, t-SNE hoặc tên đầy đủ...").strip().lower()
    group = c2.radio("Nhóm", ["Tất cả", "Linear", "Nonlinear"], horizontal=True)
    filtered = [(k, v) for k, v in ALGORITHMS.items()
                if (group == "Tất cả" or v["group"] == group)
                and (query in k.lower() or query in v["full"].lower() or query in v["vi"].lower())]
    if not filtered:
        st.info("Không tìm thấy thuật toán phù hợp.")
        return
    cols = st.columns(3)
    for i, (key, info) in enumerate(filtered):
        bg, fg = TAGS[info["group"]]
        sup = "<span class='tag' style='background:#fef3c7;color:#b45309;margin-left:6px'>Có giám sát</span>" if info["supervised"] else ""
        with cols[i % 3]:
            st.markdown(f"<div class='algo-card'><div class='algo-code'>{key}</div><div class='algo-full'>{info['full']}</div>"
                        f"<div class='algo-desc'>{info['desc']}</div>"
                        f"<div style='margin-top:auto'><span class='tag' style='background:{bg};color:{fg}'>{info['group']}</span>{sup}</div></div>",
                        unsafe_allow_html=True)
            if st.button(f"Mở trực quan hóa {key} →", key=f"open_{key}", type="primary", width="stretch"):
                st.session_state.selected_algorithm = key
                st.switch_page("page/algorithm.py")


render()
