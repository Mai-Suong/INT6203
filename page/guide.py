import streamlit as st

def render():
    st.title("Hướng dẫn sử dụng DimViz")
    st.markdown("""
### Quy trình thực nghiệm
1. Mở **Khám phá thuật toán** và chọn một thuật toán.
2. Trong trang trực quan hóa, chọn dataset mẫu hoặc tải tệp CSV.
3. Chọn các cột đặc trưng (Feature columns). Không đưa cột nhãn vào Feature columns.
4. Chọn Label column nếu muốn tô màu theo lớp; riêng LDA bắt buộc phải có nhãn.
5. Chọn số chiều đầu ra: 1D, 2D hoặc 3D.
6. Chọn chạy dữ liệu gốc, dữ liệu Z-score hoặc so sánh cả hai.
7. Nhấn **Run Algorithm** để xem biểu đồ và thông tin kết quả.

### Z-score Standardization
Z-score đưa mỗi đặc trưng về thang đo dựa trên trung bình và độ lệch chuẩn. Việc chuẩn hóa có thể ảnh hưởng đáng kể đến kết quả của một số thuật toán, đặc biệt khi các cột có đơn vị hoặc độ lớn khác nhau.

### Lưu ý về dữ liệu
- CSV nên có hàng đầu tiên là tên cột.
- Các Feature columns cần là dữ liệu số.
- Dữ liệu thiếu có thể được thay bằng trung vị hoặc loại khỏi quá trình chạy.
- Với LDA, cần chọn cột nhãn có ít nhất hai lớp.
- Kết quả 1D/2D/3D là embedding để trực quan hóa; trục mới không nhất thiết mang ý nghĩa trực tiếp như các cột ban đầu.
""")

render()
