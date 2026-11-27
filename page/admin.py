import hmac
import os
import time

import numpy as np
import streamlit as st

from core import store
from core.data import NO_LABEL, SAMPLE_DATASETS, guess_label_col, read_csv_bytes

USER_ICON = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='currentColor'>"
             "<path d='M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0'/>"
             "<path fill-rule='evenodd' d='M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1'/></svg>")


def _credentials():
    """Lấy tài khoản quản trị từ .streamlit/secrets.toml hoặc biến môi trường. Trả về (user, password) hoặc (None, None)."""
    try:
        user, password = st.secrets.get("admin_username"), st.secrets.get("admin_password")
    except Exception:
        user = password = None
    user = user or os.environ.get("DIMVIZ_ADMIN_USER") or "admin"
    password = password or os.environ.get("DIMVIZ_ADMIN_PASSWORD")
    return (user, password) if password else (None, None)


def _same(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def _login():
    user, password = _credentials()
    with st.container(key="login_card"):
        st.markdown(f"<div class='login-title'>{USER_ICON}<span>Đăng nhập</span></div>", unsafe_allow_html=True)
        with st.form("admin_login", border=False):
            entered_user = st.text_input("Tên đăng nhập")
            entered_pass = st.text_input("Mật khẩu", type="password")  # có sẵn biểu tượng con mắt để hiện/ẩn mật khẩu
            submitted = st.form_submit_button("Đăng nhập", type="primary", width="stretch")
        if submitted:
            if password is None:
                st.error("Chưa cấu hình tài khoản. Hãy tạo .streamlit/secrets.toml (xem secrets.toml.example).")
            elif _same(entered_user.strip(), user) and _same(entered_pass, password):
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                time.sleep(1)  # làm chậm việc dò mật khẩu
                st.error("Tên đăng nhập hoặc mật khẩu không chính xác.")
    st.markdown("<p class='muted' style='text-align:center;font-size:.85rem'>Khách có thể dùng mọi chức năng trực quan hóa mà không cần đăng nhập. Chỉ khu vực quản trị dataset cần xác thực.</p>", unsafe_allow_html=True)


def _add_form():
    st.markdown("#### Thêm dataset mới")
    uploaded = st.file_uploader("Tệp CSV", type=["csv"], key="admin_new_file")
    if uploaded is None:
        st.caption("Chọn một tệp CSV để thêm vào danh sách dataset có sẵn của mọi người dùng.")
        return
    try:
        df = read_csv_bytes(uploaded.getvalue())
    except Exception as exc:
        st.error(f"Không đọc được CSV: {exc}")
        return
    st.dataframe(df.head(5), width="stretch")
    options = [NO_LABEL] + list(df.columns)
    guess = guess_label_col(df)
    with st.form("admin_add_dataset", clear_on_submit=True):
        name = st.text_input("Tên dataset", value=uploaded.name.rsplit(".", 1)[0])
        label = st.selectbox("Cột nhãn mặc định", options, index=options.index(guess) if guess in options else 0)
        desc = st.text_area("Mô tả (tùy chọn)", max_chars=300)
        ok = st.form_submit_button("Thêm dataset", type="primary")
    if ok:
        err = store.validate_name(name, SAMPLE_DATASETS)
        if err:
            st.error(err)
        elif len(df) < 3 or not len(df.select_dtypes(include=np.number).columns):
            st.error("Dataset cần có ít nhất 3 dòng và 1 cột dạng số.")
        else:
            store.add_dataset(name, df, None if label == NO_LABEL else label, desc)
            st.session_state.pop("admin_new_file", None)
            st.success(f"Đã thêm dataset “{name.strip()}”.")
            st.rerun()


def _manage_list():
    st.markdown("#### Dataset đã thêm")
    custom = store.list_custom()
    if not custom:
        st.info("Chưa có dataset nào do Admin thêm.")
        return
    for i, (name, meta) in enumerate(sorted(custom.items())):
        df = store.load_custom(name)
        with st.expander(f"{name} · {len(df):,} dòng × {len(df.columns)} cột"):
            with st.form(f"admin_edit_{i}"):
                new_name = st.text_input("Tên dataset", value=name)
                options = [NO_LABEL] + list(df.columns)
                cur = meta.get("label") if meta.get("label") in df.columns else NO_LABEL
                label = st.selectbox("Cột nhãn mặc định", options, index=options.index(cur))
                desc = st.text_area("Mô tả", value=meta.get("desc", ""), max_chars=300)
                save = st.form_submit_button("Lưu thay đổi")
            if save:
                err = store.validate_name(new_name, SAMPLE_DATASETS, current=name)
                if err:
                    st.error(err)
                else:
                    store.update_dataset(name, new_name, None if label == NO_LABEL else label, desc)
                    st.rerun()
            confirm = st.checkbox("Tôi chắc chắn muốn xóa dataset này", key=f"admin_confirm_{i}")
            if st.button("🗑️ Xóa dataset", key=f"admin_delete_{i}", disabled=not confirm):
                store.delete_dataset(name)
                st.rerun()


def render():
    if not st.session_state.get("admin_authenticated"):
        _login()
        return
    st.title("Quản trị")
    st.caption("Quản lý các dataset mẫu bổ sung. Dataset thêm ở đây sẽ xuất hiện trong danh sách “Dataset có sẵn” của mọi người dùng.")
    _add_form()
    st.markdown("---")
    _manage_list()
    st.markdown("---")
    if st.button("Đăng xuất"):
        st.session_state.admin_authenticated = False
        st.rerun()


render()
