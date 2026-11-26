ALGORITHMS = {
    "PCA": {"full": "Principal Component Analysis", "vi": "Phân tích thành phần chính", "group": "Linear", "desc": "Tìm các hướng chiếu giữ lại lượng phương sai lớn nhất của dữ liệu.", "supervised": False},
    "LDA": {"full": "Linear Discriminant Analysis", "vi": "Phân tích biệt thức tuyến tính", "group": "Linear", "desc": "Tìm các hướng chiếu giúp phân biệt các lớp dữ liệu; cần cột nhãn.", "supervised": True},
    "SVD": {"full": "Singular Value Decomposition", "vi": "Phân rã giá trị suy biến", "group": "Linear", "desc": "Phân rã ma trận thành các thành phần để biểu diễn dữ liệu bằng số chiều thấp hơn.", "supervised": False},
    "MDS": {"full": "Multidimensional Scaling", "vi": "Định tỷ lệ đa chiều", "group": "Linear", "desc": "Tạo biểu diễn ít chiều sao cho khoảng cách giữa các điểm gần với dữ liệu gốc.", "supervised": False},
    "t-SNE": {"full": "t-distributed Stochastic Neighbor Embedding", "vi": "Nhúng lân cận ngẫu nhiên phân phối t", "group": "Nonlinear", "desc": "Tập trung bảo toàn quan hệ lân cận, thường dùng để quan sát cụm dữ liệu.", "supervised": False},
    "UMAP": {"full": "Uniform Manifold Approximation and Projection", "vi": "Xấp xỉ và chiếu đa tạp đồng nhất", "group": "Nonlinear", "desc": "Xây dựng đồ thị lân cận để biểu diễn cấu trúc dữ liệu trong không gian thấp chiều.", "supervised": False},
    "Isomap": {"full": "Isometric Mapping", "vi": "Ánh xạ đẳng cự", "group": "Nonlinear", "desc": "Ước lượng khoảng cách trắc địa trên đồ thị lân cận và bảo toàn chúng khi chiếu.", "supervised": False},
    "LLE": {"full": "Locally Linear Embedding", "vi": "Nhúng tuyến tính cục bộ", "group": "Nonlinear", "desc": "Giữ lại quan hệ tái tạo tuyến tính giữa mỗi điểm và các láng giềng gần nhất.", "supervised": False},
    "Kernel PCA": {"full": "Kernel Principal Component Analysis", "vi": "Phân tích thành phần chính hạt nhân", "group": "Nonlinear", "desc": "Dùng hàm kernel để mô hình hóa cấu trúc phi tuyến mà PCA thông thường khó nắm bắt.", "supervised": False},
}
