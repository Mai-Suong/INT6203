import streamlit as st
import pandas as pd
from core.data import SAMPLE_DATASETS, load_sample

def render():
    st.title("Quản lý dữ liệu")
    st.caption("Chọn dữ liệu mẫu hoặc tải CSV. Dữ liệu đã xác nhận sẽ được lưu trong phiên làm việc để dùng ở trang trực quan hóa.")
    mode = st.radio("Nguồn dữ liệu", ["Dataset có sẵn", "Tải CSV lên"], horizontal=True)
    if mode == "Dataset có sẵn":
        name = st.selectbox("Chọn dataset", SAMPLE_DATASETS)
        df, labels = load_sample(name)
        label_name = "label"
        df = df.copy(); df[label_name] = labels
        st.session_state.dataset_name = name
        st.session_state.dataset_df = df
        st.session_state.label_column = label_name
    else:
        uploaded = st.file_uploader("Chọn tệp CSV", type=["csv"])
        if uploaded is None:
            st.info("Tải lên một tệp CSV để xem trước dữ liệu.")
            return
        try:
            df = pd.read_csv(uploaded)
        except Exception as exc:
            st.error(f"Không đọc được CSV: {exc}")
            return
        st.session_state.dataset_name = uploaded.name
        st.session_state.dataset_df = df
    df = st.session_state.dataset_df
    st.markdown("### Xem trước dữ liệu")
    m1, m2, m3 = st.columns(3)
    m1.metric("Số mẫu", len(df)); m2.metric("Số cột", len(df.columns)); m3.metric("Giá trị thiếu", int(df.isna().sum().sum()))
    st.dataframe(df.head(10), use_container_width=True)
    st.success(f"Đã chọn dữ liệu: {st.session_state.dataset_name}. Có thể dùng dataset này trong trang Trực quan hóa.")

render()
