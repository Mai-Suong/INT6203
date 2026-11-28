"""Giao diện dùng chung: CSS (nhúng bằng Python), thanh đầu trang, footer và ô nhập tham số thuật toán."""
import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Barlow+Condensed:wght@700;800&display=swap');

:root{
  --navy:#001C44; --teal:#2D99AE; --teal-dark:#0C5776; --peach:#F8DAD0;
  --bg:#f3f5f9; --line:#e3e7ee; --text:#172033; --muted:#64748b;
}

/* ---------- Nền & phông chữ ---------- */
.stApp{background:var(--bg); color:var(--text); font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;}
header[data-testid="stHeader"], [data-testid="stDecoration"], [data-testid="stToolbar"],
[data-testid="stStatusWidget"], footer{display:none !important;}

/* ---------- Bố cục: thanh/footer rộng 100%, nội dung 80% ---------- */
[data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"]{
  max-width:100% !important; width:100% !important; padding:0 !important; min-height:100vh;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"],
[data-testid="stAppViewBlockContainer"] > [data-testid="stVerticalBlock"]{
  gap:0 !important; min-height:100vh; display:flex; flex-direction:column;
}
.st-key-page_content{padding:2rem 10% 3rem; flex:1 0 auto;}
div:has(> .st-key-page_content){flex:1 0 auto;}
div:has(> .st-key-site_footer){margin-top:auto;}
@media (max-width:900px){
  .st-key-page_content{padding:1.2rem 1rem 2rem;}
  .st-key-topbar, .st-key-navbar, .st-key-site_footer{padding-left:1rem !important; padding-right:1rem !important;}
}

/* ---------- Thanh trên cùng: chỉ có DimViz và nút Đăng nhập ---------- */
.st-key-topbar{background:var(--navy); padding:.65rem 10%;}
.st-key-topbar [data-testid="stVerticalBlock"]{gap:0;}
.st-key-topbar a, .st-key-topbar a:hover{text-decoration:none !important;}
.st-key-topbar a p{color:#fff !important; margin:0;}
.st-key-brand_link a{display:inline-flex; align-items:center; gap:.6rem; padding:0 !important; background:transparent !important;}
.st-key-brand_link a::before{
  content:"D"; display:inline-flex; align-items:center; justify-content:center; width:2.15rem; height:2.15rem;
  border-radius:50%; background:var(--teal); color:#fff; font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:1.35rem;
}
.st-key-brand_link a p{font-family:'Barlow Condensed','Impact',sans-serif; font-weight:800; font-size:1.65rem; letter-spacing:.4px; text-transform:uppercase;}
.st-key-login_link a{border:1px solid rgba(255,255,255,.85); border-radius:6px; padding:.42rem .95rem !important; background:transparent !important; transition:background .15s;}
.st-key-login_link a:hover{background:rgba(255,255,255,.14) !important;}
.st-key-login_link a p{font-weight:600; font-size:.92rem;}
.st-key-login_link [data-testid="stIconMaterial"]{color:#fff !important;}

/* ---------- Thanh menu trắng ---------- */
.st-key-navbar{background:#fff; border-bottom:1px solid var(--line); padding:0 10%;}
.st-key-navbar [data-testid="stVerticalBlock"], .st-key-navbar [data-testid="stHorizontalBlock"]{gap:.25rem;}
.st-key-navbar a{border-radius:0 !important; border-bottom:3px solid transparent; padding:.95rem .8rem !important; background:transparent !important; text-decoration:none !important;}
.st-key-navbar a p{color:#334155 !important; font-weight:600; font-size:.93rem; margin:0;}
.st-key-navbar a:hover{border-bottom-color:var(--peach);}
.st-key-navbar a:hover p{color:var(--navy) !important;}
[class*="st-key-nav_active"] a{border-bottom-color:var(--teal-dark) !important;}
[class*="st-key-nav_active"] a p{color:var(--teal-dark) !important;}

/* ---------- Footer ---------- */
.st-key-site_footer{background:var(--navy); padding:1.15rem 10%; color:#c9d4e6; font-size:.88rem;}
.st-key-site_footer p{color:#c9d4e6 !important; margin:0;}
.st-key-site_footer b{color:#fff;}

/* ---------- Tiêu đề & chữ ---------- */
.stApp h1, .stApp h2, .stApp h3{color:var(--navy); letter-spacing:-.3px;}
.muted{color:var(--muted);}

/* ---------- Nút ---------- */
[data-testid="stBaseButton-secondary"], [data-testid="stDownloadButton"] button, [data-testid="stBaseButton-secondaryFormSubmit"]{
  background:#fff !important; color:var(--navy) !important; border:1px solid var(--navy) !important;
  border-radius:10px !important; font-weight:600 !important; transition:all .2s ease-in-out !important;
}
[data-testid="stBaseButton-secondary"] p, [data-testid="stDownloadButton"] button p{color:var(--navy) !important;}
[data-testid="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover{
  background:var(--peach) !important; transform:translateY(-1px); box-shadow:0 3px 8px rgba(0,28,68,.12) !important;
}
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"]{
  background:var(--navy) !important; color:#fff !important; border:1px solid var(--navy) !important;
  border-radius:10px !important; font-weight:700 !important; transition:all .2s ease-in-out !important;
}
[data-testid="stBaseButton-primary"] p, [data-testid="stBaseButton-primaryFormSubmit"] p{color:#fff !important;}
[data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover{
  background:var(--teal-dark) !important; border-color:var(--teal-dark) !important; transform:translateY(-1px);
}
[data-testid="stBaseButton-primary"]:disabled{opacity:.45;}

/* ---------- Thẻ ---------- */
.hero{padding:2.2rem 2.4rem; border-radius:18px; background:linear-gradient(120deg,#eaf2ff 0%,#f7fbff 65%,#eff6ff 100%); border:1px solid #dbeafe;}
.hero h1{font-size:2.35rem; line-height:1.18; color:#102a56; margin-bottom:.7rem;}
.algo-card{background:#fff; border:1px solid var(--navy); border-radius:16px; padding:18px; min-height:205px; box-sizing:border-box; display:flex; flex-direction:column;}
.algo-code{font-size:28px; font-weight:800; color:var(--teal-dark); margin-bottom:3px;}
.algo-full{font-size:17px; color:#475569; font-weight:650; min-height:44px;}
.algo-desc{font-size:15px; color:var(--muted); line-height:1.5; margin-top:8px;}
.feature-card{background:var(--teal); border:1px solid var(--navy); border-radius:16px; padding:18px; min-height:175px; box-sizing:border-box; color:var(--navy);}
.feature-card .muted{color:#000 !important; font-weight:400;}
.tag{display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:700; margin-top:auto; align-self:flex-start;}
div[data-testid="stMetric"]{background:#fff; border:1px solid var(--line); padding:12px 14px; border-radius:12px;}

/* ---------- Trang đăng nhập ---------- */
.st-key-login_card{max-width:400px; margin:2rem auto 1rem; background:#fff; border:1px solid var(--line); border-radius:10px; padding:1.3rem 1.5rem 1.6rem; box-shadow:0 1px 3px rgba(16,24,40,.06);}
.login-title{display:flex; align-items:center; justify-content:center; gap:.55rem; margin:.2rem 0 1.1rem;
  font-family:'Barlow Condensed','Impact',sans-serif; font-weight:800; font-size:2.35rem; letter-spacing:.5px; text-transform:uppercase; color:#1b2230; line-height:1;}
.login-title svg{width:2.1rem; height:2.1rem;}
.st-key-login_card [data-testid="stForm"]{border:0 !important; padding:0 !important;}
.st-key-login_card [data-testid="stBaseButton-primaryFormSubmit"]{width:100%; padding:.6rem 0;}
/* viền xanh khi focus */
div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within{
  border-color:#86b7fe !important; box-shadow:0 0 0 .22rem rgba(13,110,253,.22) !important;}
"""


def inject_css():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def render_header(home_page, nav_pages, login_page, logged_in=False, current_page=None):
    """Hàng 1 (nền xanh đậm): logo DimViz + nút Đăng nhập. Hàng 2 (nền trắng): menu chính."""
    with st.container(key="topbar"):
        with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center", key="topbar_row"):
            with st.container(key="brand_link", width="content"):
                st.page_link(home_page, label="DimViz")
            with st.container(key="login_link", width="content"):
                st.page_link(login_page, label="Quản trị" if logged_in else "Đăng nhập", icon=":material/person:")
    with st.container(key="navbar"):
        with st.container(horizontal=True, key="navbar_row"):
            for i, (label, page) in enumerate(nav_pages.items()):
                active = current_page is not None and page.url_path == current_page.url_path
                with st.container(key=f"nav_{'active' if active else 'item'}_{i}", width="content"):
                    st.page_link(page, label=label)


def render_footer():
    with st.container(key="site_footer"):
        with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
            st.markdown("**DimViz** · Sầm Thị Mai Sương · Đồ án Cơ sở ngành")
            st.markdown("Python · Streamlit · scikit-learn · Plotly")


def render_param_inputs(algo, specs, prefix):
    """Vẽ các ô nhập tham số của thuật toán; trả về dict tham số để truyền vào run_algorithm."""
    params = {}
    for spec in specs:
        key = f"{prefix}_{algo}_{spec['key']}"
        if spec["kind"] == "int":
            params[spec["key"]] = st.slider(spec["label"], spec["min"], spec["max"], spec["default"], 1, help=spec["help"], key=key)
        elif spec["kind"] == "float":
            params[spec["key"]] = st.slider(spec["label"], float(spec["min"]), float(spec["max"]), float(spec["default"]),
                                            float(spec.get("step", 0.1)), help=spec["help"], key=key)
        elif spec["kind"] == "select":
            params[spec["key"]] = st.selectbox(spec["label"], spec["options"], index=spec["options"].index(spec["default"]),
                                               help=spec["help"], key=key)
        elif spec["kind"] == "gamma":
            if params.get("kernel", "rbf") in ("rbf", "poly", "sigmoid"):
                auto = st.checkbox(f"gamma tự động (= 1/số đặc trưng ≈ {spec['default']:.4f})", value=True, key=key + "_auto")
                if auto:
                    params["gamma"] = None
                else:
                    params["gamma"] = st.number_input(spec["label"], min_value=1e-6, max_value=1000.0, value=float(spec["default"]),
                                                      format="%.5f", step=0.01, help=spec["help"], key=key)
    return params
