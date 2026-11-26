# DimViz — Dimensionality Reduction Visualization

Ứng dụng học tập và trực quan hóa các thuật toán giảm chiều dữ liệu, xây dựng bằng Python và Streamlit.

## Tính năng trong bản khởi tạo
- Trang chủ và trang khám phá 9 thuật toán.
- Trang thực nghiệm riêng theo thuật toán: PCA, LDA, SVD, MDS, t-SNE, UMAP, Isomap, LLE, Kernel PCA.
- Dataset mẫu: Iris, Wine, Breast Cancer, Digits, Swiss Roll.
- Tải dữ liệu CSV, chọn Feature columns và Label column.
- Trực quan hóa 1D, 2D, 3D.
- So sánh dữ liệu gốc và dữ liệu chuẩn hóa Z-score.
- Trang so sánh nhiều thuật toán trên cùng dữ liệu.

## Cài đặt
Khuyến nghị Python 3.10–3.12.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Cài thư viện và chạy ứng dụng:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cấu hình Admin
Tạo file `.streamlit/secrets.toml`:
```toml
admin_password = "your-strong-password"
```
Không đưa file secrets lên GitHub.

## Lưu ý
- UMAP cần gói `umap-learn`.
- LDA cần cột nhãn và số chiều tối đa phụ thuộc số lớp.
- MDS và một số thuật toán manifold có thể chạy chậm với dataset lớn.
- Đây là bản nền để tiếp tục hoàn thiện; chức năng CRUD Admin, xuất kết quả và kiểm thử toàn diện chưa được triển khai.
