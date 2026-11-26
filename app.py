import streamlit as st
from core.ui import inject_css, render_header, render_footer

st.set_page_config(page_title="DimViz", page_icon="📊", layout="wide")
inject_css()

PAGES = {
    "Trang chủ": "home",
    "Dữ liệu": "data",
    "Khám phá thuật toán": "explore",
    "So sánh": "comparison",
    "Hướng dẫn": "guide",
    "Đăng nhập": "admin",
}

# Mỗi thuật toán dùng chung một trang thực nghiệm, nội dung thay đổi theo lựa chọn của người dùng.
p_home = st.Page("page/home.py", title="Trang chủ", url_path="home", default=True)
p_data = st.Page("page/data_page.py", title="Dữ liệu", url_path="data")
p_explore = st.Page("page/explore.py", title="Khám phá thuật toán", url_path="algorithms")
p_algorithm = st.Page("page/algorithm.py", title="Trực quan hóa thuật toán", url_path="visualize")
p_comparison = st.Page("page/comparison.py", title="So sánh", url_path="comparison")
p_guide = st.Page("page/guide.py", title="Hướng dẫn", url_path="guide")
p_admin = st.Page("page/admin.py", title="Đăng nhập", url_path="admin")

pg = st.navigation([p_home, p_data, p_explore, p_algorithm, p_comparison, p_guide, p_admin], position="hidden")
render_header({"Trang chủ": p_home, "Dữ liệu": p_data, "Khám phá thuật toán": p_explore,
               "So sánh": p_comparison, "Hướng dẫn": p_guide, "Đăng nhập": p_admin}, pg)
pg.run()
render_footer()
