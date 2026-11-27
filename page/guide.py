import streamlit as st


def render():
    st.title("Hướng dẫn sử dụng DimViz")
    st.markdown("""
### Quy trình thực nghiệm
1. Mở **Khám phá thuật toán** (hoặc **Trực quan hóa**) và chọn một thuật toán.
2. Chọn dataset mẫu hoặc tải tệp CSV. Dữ liệu chọn ở trang **Dữ liệu** sẽ được dùng sẵn ở các trang khác.
3. Chọn **Label column** nếu muốn tô màu theo lớp; riêng LDA bắt buộc phải có nhãn phân loại.
4. Chọn **Feature columns**. Cột nhãn tự động không nằm trong danh sách đặc trưng.
5. Chọn số chiều đầu ra: 1D, 2D hoặc 3D, và chạy dữ liệu gốc, dữ liệu Z-score hoặc so sánh cả hai.
6. Chỉnh **tham số** của thuật toán nếu có (perplexity, n_neighbors, gamma...).
7. Nhấn nút **Run** để xem biểu đồ, thời gian chạy và các chỉ số chất lượng; có thể tải embedding về dạng CSV.

### Z-score Standardization
Z-score đưa mỗi đặc trưng về trung bình 0 và độ lệch chuẩn 1. Khi các cột có đơn vị hoặc độ lớn rất khác nhau
(ví dụ cột *proline* ≈ 1000 so với cột khác ≈ 1 trong bộ Wine), dữ liệu gốc sẽ bị cột lớn chi phối. Hãy dùng chế độ
**So sánh cả hai** để thấy sự khác biệt. LDA gần như không bị ảnh hưởng vì nó bất biến với việc co giãn từng đặc trưng.

### Cách đọc biểu đồ
- Trục mới (Dim 1, Dim 2, Dim 3) **không** mang ý nghĩa trực tiếp như các cột ban đầu.
- Với **t-SNE** và **UMAP**, khoảng cách giữa các cụm và kích thước cụm không đáng tin; chỉ nên đọc việc điểm nào đứng gần nhau.
- Thuật toán ngẫu nhiên (t-SNE, UMAP, MDS) dùng hạt giống cố định nên kết quả lặp lại được, nhưng vẫn phụ thuộc tham số.
- **Trustworthiness** (0–1): láng giềng trên biểu đồ có thật sự là láng giềng ở dữ liệu gốc không.
- **Silhouette** (−1…1): các lớp có tách nhau trên biểu đồ không (cần nhãn phân loại).
- **Scree plot** (PCA/SVD): phương sai của từng thành phần; chọn số chiều ở chỗ đường cong bắt đầu phẳng.

### Lưu ý về dữ liệu
- CSV nên có hàng đầu tiên là tên cột. Hỗ trợ dấu phân cách `,` và `;`, mã hóa UTF-8 hoặc Excel tiếng Việt.
- Các Feature columns cần là dữ liệu số. Giá trị thiếu có thể được thay bằng trung vị hoặc loại khỏi quá trình chạy.
- Cột nhãn dạng số có nhiều giá trị khác nhau (hơn 20, như nhãn của Swiss Roll) được coi là **nhãn liên tục** và tô bằng thang màu. LDA không dùng được với loại nhãn này.
- Một số thuật toán chậm với dữ liệu lớn (MDS, t-SNE, Isomap, Kernel PCA) sẽ tự động lấy mẫu ngẫu nhiên và có thông báo.
- Kết quả 1D/2D/3D là embedding để trực quan hóa, không phải dữ liệu để thay thế dữ liệu gốc khi phân tích số liệu.
""")


render()
