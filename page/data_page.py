import pandas as pd
import streamlit as st

from core import store
from core.data import guess_label_col, list_datasets, load_dataset, read_csv_bytes


def render():
    st.title("Quản lý dữ liệu")
    mode = st.radio("Nguồn dữ liệu", ["Dataset có sẵn", "Tải CSV lên"], horizontal=True)

    if mode == "Dataset có sẵn":
        names = list_datasets()
        current = st.session_state.get("dataset_name")
        name = st.selectbox("Chọn dataset", names, index=names.index(current) if current in names else 0)
        df, label = load_dataset(name)
        desc = store.list_custom().get(name, {}).get("desc")
        if desc:
            st.caption(desc)
    else:
        uploaded = st.file_uploader("Chọn tệp CSV", type=["csv"])
        if uploaded is None:
            st.info("Tải lên một tệp CSV để xem trước dữ liệu.")
            return
        try:
            df = read_csv_bytes(uploaded.getvalue())
        except Exception as exc:
            st.error(f"Không đọc được CSV: {exc}")
            return
        name, label = uploaded.name, guess_label_col(df)

    st.session_state.dataset_name = name
    st.session_state.dataset_df = df
    st.session_state.dataset_label = label

    st.markdown("### Tổng quan")
    n_numeric = len(df.select_dtypes("number").columns)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Số mẫu", f"{len(df):,}")
    m2.metric("Số cột", len(df.columns))
    m3.metric("Cột dạng số", n_numeric)
    m4.metric("Giá trị thiếu", f"{int(df.isna().sum().sum()):,}")
    if label:
        st.caption(f"Cột nhãn được nhận diện: **{label}**")
    st.markdown("### Xem trước dữ liệu")
    st.dataframe(df.head(10), width="stretch")
    with st.expander("Thống kê mô tả và giá trị thiếu theo cột"):
        st.dataframe(df.describe(include="all").T, width="stretch")
        missing = df.isna().sum()
        st.dataframe(pd.DataFrame({"Giá trị thiếu": missing, "Tỉ lệ (%)": (missing / max(len(df), 1) * 100).round(2)}), width="stretch")
    st.success(f"Đã chọn dữ liệu: **{name}**. Mở trang **Trực quan hóa** hoặc **So sánh** để dùng dataset này.")


render()
