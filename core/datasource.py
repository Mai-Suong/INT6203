"""Bộ chọn nguồn dữ liệu dùng chung cho trang Trực quan hóa và So sánh."""
import streamlit as st

from core.data import guess_label_col, list_datasets, load_dataset, read_csv_bytes

SHARED = "Dữ liệu đã chọn ở trang Dữ liệu"
BUILTIN = "Dataset có sẵn"
UPLOAD = "Tải CSV lên"


def dataset_picker(prefix):
    """Trả về dict {name, df, label, source} hoặc None nếu chưa có dữ liệu."""
    shared = st.session_state.get("dataset_df")
    options = ([SHARED] if shared is not None else []) + [BUILTIN, UPLOAD]
    source = st.radio("Nguồn dữ liệu", options, horizontal=True, key=f"{prefix}_source")

    if source == SHARED:
        name = st.session_state.get("dataset_name", "(không tên)")
        st.caption(f"Đang dùng dữ liệu bạn đã chọn ở trang **Dữ liệu**: {name}")
        return {"name": name, "df": shared.copy(), "label": st.session_state.get("dataset_label"), "source": source}

    if source == BUILTIN:
        names = list_datasets()
        current = st.session_state.get("dataset_name")
        name = st.selectbox("Dataset", names, index=names.index(current) if current in names else 0, key=f"{prefix}_sample")
        df, label = load_dataset(name)
        return {"name": name, "df": df, "label": label, "source": source}

    uploaded = st.file_uploader("Tải tệp dữ liệu CSV", type=["csv"], key=f"{prefix}_upload")
    if uploaded is None:
        st.info("Vui lòng tải lên tệp CSV để tiếp tục.")
        return None
    try:
        df = read_csv_bytes(uploaded.getvalue())
    except Exception as exc:
        st.error(f"Không thể đọc tệp CSV: {exc}")
        return None
    return {"name": uploaded.name, "df": df, "label": guess_label_col(df), "source": source}
