import streamlit as st

LOGO = """<div class='brand-mark'>DimViz</div>"""

def inject_css():
    st.markdown("""<style>
    .stApp {background: white; color:#172033 width:80%}
    header[data-testid="stHeader"] {background: transparent !important;}
    .block-container, [data-testid="stMainBlockContainer"] {padding-top: 4.2rem !important; padding-bottom: 2rem !important; max-width:1280px}
    .main .block-container > div[data-testid="stVerticalBlock"] {
    min-height: calc(100vh - 100px);
    display: flex;
    flex-direction: column;} 
    .brand-mark{width:36px;height:36px;border-radius:11px;background:#001C44;color:white;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:21px}
    .brand-name{font-size:22px;font-weight:800;letter-spacing:-.6px;color:#101828}
    .hero{padding:2.2rem 2.4rem;border-radius:22px;background:linear-gradient(120deg,#eaf2ff 0%,#f7fbff 65%,#eff6ff 100%);border:1px solid #dbeafe}
    .hero h1{font-size:2.45rem;line-height:1.18;color:#102a56;margin-bottom:.7rem}
    .muted{color:#64748b}
    .algo-card{background:white; border:1px solid #001C44; border-radius:16px; padding:18px;height:205px;box-sizing:border-box;display:flex;flex-direction:column;}
    
    
    /* Các khung chức năng chính có kích thước bằng nhau */
    .feature-card {
    background: #2D99AE;
    border: 1px solid #001C44;
    border-radius: 16px;
    padding: 18px;
    height: 175px;
    box-sizing: border-box;
    overflow: hidden;
    color: #001C44;
    }
    .feature-card .muted {
        color: black !important;
        font-weight: 350 !important;
    }

    /* Giữ màu chữ trắng khi hover */
    [class*="st-key-nav_logo_home"] button:hover p {
        color: white !important;
    }

    [class*="st-key-nav_"] button:hover {
        background-color: #F8DAD0 !important;
        border-color: #0C5776 !important;
        color: #001C44 !important;
    }
    [class*="st-key-nav_"] button:hover p {
        color: #001C44 !important;
    }

    .algo-code{font-size:30px;font-weight:800;color:#0C5776;margin-bottom:3px}
    .algo-full{font-size:20px;color:#475569;font-weight:650;min-height:40px}
    .algo-desc{font-size:17px;color:#64748b;line-height:1.5;min-height:58px;margin-top:10px}
    div[data-testid='stMetric']{background:white;border:1px solid #e5eaf2;padding:12px;border-radius:12px}
    button[kind='primary']{background:#2563eb;border-color:#2563eb}
    /* Vùng nội dung chính của Streamlit */
    div[data-testid="stMainBlockContainer"] {
        min-height: calc(100vh - 80px);
        display: flex;
        flex-direction: column;
    }
    
    /* Khối nội dung bên trong */
    div[data-testid="stMainBlockContainer"] > div[data-testid="stVerticalBlock"] {
        flex: 1;
    }
    
    /* Đẩy khối chứa footer xuống cuối */
    div[data-testid="stVerticalBlock"] > div:has(.footer) {
        margin-top: auto;
    }
    
    /* Giao diện footer */
    .footer {
        width: 100%;
        box-sizing: border-box;
        margin-top: auto !important;
        padding: 18px 12px;
        color: #FFFFFF !important;
        background: #001C44 !important;
        font-size: 16px !important;
        font-weight: 500;
        border-radius: 8px;
    }

    /* Trạng thái mặc định */
    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        background-color: #FFFFFF !important;
        color: #001C44 !important;
        border: 1px solid #001C44 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Chữ bên trong nút */
    div[data-testid="stButton"] button p,
    div[data-testid="stDownloadButton"] button p,
    div[data-testid="stFormSubmitButton"] button p {
        color: #001C44 !important;
    }

    /* Khi rê chuột */
    div[data-testid="stButton"] button:hover,
    div[data-testid="stDownloadButton"] button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #F8DAD0 !important;
        border: 1px solid #001C44 !important;
        color: #001C44 !important;
        transform: translateY(-2px);
        box-shadow: 0 3px 8px rgba(0, 28, 68, 0.12) !important;
    }

    /* Chữ khi rê chuột */
    div[data-testid="stButton"] button:hover p,
    div[data-testid="stDownloadButton"] button:hover p,
    div[data-testid="stFormSubmitButton"] button:hover p {
        color: #001C44 !important;
    }

    /* Nút logo quay về Trang chủ */
    [class*="st-key-nav_logo_home"] button {
        background-color: #001C44 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 8px 14px !important;
        border-radius: 12px !important;
        transition: background-color 0.2s ease !important;
    }

    /* Chữ DimViz */
    [class*="st-key-nav_logo_home"] button p {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: white !important;
        white-space: nowrap !important;
    }

    /* Khi rê chuột */
    [class*="st-key-nav_logo_home"] button:hover {
        background-color: #F8DAD0 !important;
    }

    </style>""", unsafe_allow_html=True)



def render_header(pages, current_page=None):
    # Chia không gian cho logo và thanh menu
    c1, c2 = st.columns([1.7, 8.3], vertical_alignment="center")

    with c1:
        home_page = pages.get("Trang chủ") if isinstance(pages, dict) else None
        if st.button("DimViz", key="nav_logo_home", type="tertiary"):
            if home_page is not None:
                st.switch_page(home_page)

    with c2:
        weights = [1.0, 0.8, 1.5, 0.9, 0.9, 0.7]
        cols = st.columns(weights, gap="small")

        for col, (label, page) in zip(cols, pages.items()):
            with col:
                if st.button(
                    label,
                    key=f"nav_{label}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.switch_page(page)

    st.markdown(
        "<hr style='border:0;border-top:1px solid #e5eaf2;"
        "margin:.8rem 0 1.5rem'>",
        unsafe_allow_html=True
    )

def render_footer():
    st.markdown("<div class='footer'>Sầm Thị Mai Sương · Đồ án Cơ sở ngành</div>", unsafe_allow_html=True)
