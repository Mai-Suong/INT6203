import streamlit as st

def render():
    st.title("Admin")
    st.caption("Khu vực quản trị dành cho người quản lý nội dung và dữ liệu mẫu.")
    try:
        password = st.secrets.get("admin_password", None)
    except Exception:
        password = None
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    if not st.session_state.admin_authenticated:
        st.info("Khách có thể sử dụng các chức năng trực quan hóa mà không cần đăng nhập. Chỉ khu vực Admin yêu cầu xác thực.")
        with st.form("admin_login"):
            entered = st.text_input("Mật khẩu quản trị", type="password")
            submitted = st.form_submit_button("Đăng nhập", type="primary")
        if submitted:
            if password and entered == password:
                st.session_state.admin_authenticated = True
                st.rerun()
            elif not password:
                st.error("Chưa cấu hình mật khẩu. Hãy tạo .streamlit/secrets.toml với admin_password = \"your-password\".")
            else:
                st.error("Mật khẩu không chính xác.")
        return
    st.success("Đã đăng nhập Admin.")
    st.warning("Bản khởi tạo hiện cung cấp khung xác thực. Chức năng CRUD quản lý dataset/nội dung sẽ được triển khai ở bước tiếp theo.")
    if st.button("Đăng xuất"):
        st.session_state.admin_authenticated = False
        st.rerun()

render()
