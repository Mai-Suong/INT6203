"""Danh mục 9 thuật toán: mô tả ngắn (thẻ), lý thuyết (trang trực quan hóa) và tham số điều chỉnh được."""

ALGORITHMS = {
    "PCA": {
        "full": "Principal Component Analysis", "vi": "Phân tích thành phần chính", "group": "Linear", "supervised": False,
        "desc": "Tìm các hướng chiếu giữ lại lượng phương sai lớn nhất của dữ liệu.",
        "idea": "Trừ trung bình từng cột, rồi tìm các trục trực giao theo hướng dữ liệu biến thiên nhiều nhất. Các trục chính là vectơ riêng của ma trận hiệp phương sai; chiếu dữ liệu lên k vectơ riêng lớn nhất cho embedding k chiều.",
        "formula": "C = XᵀX / (n−1),  C·w = λ·w,  Z = X·W_k",
        "pros": ["Nhanh, xác định (không ngẫu nhiên)", "Đo được lượng thông tin giữ lại (phương sai)", "Trục có thể diễn giải qua loadings"],
        "cons": ["Chỉ bắt được cấu trúc tuyến tính", "Rất nhạy với thang đo → nên chuẩn hóa Z-score"],
        "tip": "Xem scree plot để chọn số thành phần: dừng ở chỗ đường cong bắt đầu phẳng.",
    },
    "LDA": {
        "full": "Linear Discriminant Analysis", "vi": "Phân tích biệt thức tuyến tính", "group": "Linear", "supervised": True,
        "desc": "Tìm các hướng chiếu giúp phân biệt các lớp dữ liệu; cần cột nhãn.",
        "idea": "Có giám sát: tìm các hướng làm khoảng cách giữa tâm các lớp (S_B) lớn nhất trong khi độ phân tán trong từng lớp (S_W) nhỏ nhất. Số chiều tối đa là min(số đặc trưng, số lớp − 1).",
        "formula": "max_w  (wᵀ S_B w) / (wᵀ S_W w)",
        "pros": ["Tách lớp rất tốt khi các lớp gần Gaussian", "Nhanh, xác định"],
        "cons": ["Bắt buộc có nhãn phân loại", "Số chiều tối đa = số lớp − 1", "Chỉ tuyến tính, giả định các lớp có hiệp phương sai giống nhau"],
        "tip": "Vì dùng nhãn khi học, biểu đồ LDA luôn 'đẹp' hơn các phương pháp không giám sát; đừng kết luận dữ liệu tách lớp chỉ từ LDA.",
    },
    "SVD": {
        "full": "Singular Value Decomposition", "vi": "Phân rã giá trị suy biến", "group": "Linear", "supervised": False,
        "desc": "Phân rã ma trận thành các thành phần để biểu diễn dữ liệu bằng số chiều thấp hơn.",
        "idea": "Phân rã X = UΣVᵀ và giữ k giá trị suy biến lớn nhất. Khác PCA ở chỗ TruncatedSVD KHÔNG trừ trung bình cột, nên thành phần đầu thường chỉ mô tả 'độ lớn trung bình' của dữ liệu.",
        "formula": "X ≈ U_k Σ_k V_kᵀ,  Z = U_k Σ_k",
        "pros": ["Làm được với ma trận thưa (vd. văn bản, LSA)", "Rất nhanh"],
        "cons": ["Không căn giữa dữ liệu nên 'phương sai giữ lại' không bằng PCA", "Chỉ tuyến tính"],
        "tip": "So sánh SVD với PCA trên cùng dữ liệu: nếu dữ liệu đã căn giữa (hoặc dùng Z-score) hai kết quả gần như trùng nhau.",
    },
    "MDS": {
        "full": "Multidimensional Scaling", "vi": "Định tỷ lệ đa chiều", "group": "Linear", "supervised": False,
        "desc": "Tạo biểu diễn ít chiều sao cho khoảng cách giữa các điểm gần với dữ liệu gốc.",
        "idea": "Đặt các điểm vào không gian ít chiều sao cho khoảng cách mới xấp xỉ khoảng cách gốc, bằng cách cực tiểu hóa 'stress' (thuật toán lặp SMACOF). Bản cổ điển trên khoảng cách Euclid cho kết quả tương đương PCA.",
        "formula": "min Σᵢ<ⱼ ( dᵢⱼ − ‖zᵢ − zⱼ‖ )²",
        "pros": ["Bảo toàn khoảng cách toàn cục", "Dùng được khi chỉ có ma trận khoảng cách"],
        "cons": ["Chậm: O(n²) bộ nhớ và thời gian", "Có thể kẹt cực tiểu cục bộ (nên thử nhiều lần khởi tạo)"],
        "tip": "Tăng 'Số lần khởi tạo' và 'Số vòng lặp tối đa' nếu bố cục thay đổi nhiều giữa các lần chạy.",
    },
    "t-SNE": {
        "full": "t-distributed Stochastic Neighbor Embedding", "vi": "Nhúng lân cận ngẫu nhiên phân phối t", "group": "Nonlinear", "supervised": False,
        "desc": "Tập trung bảo toàn quan hệ lân cận, thường dùng để quan sát cụm dữ liệu.",
        "idea": "Biến khoảng cách thành xác suất 'là láng giềng' (Gaussian ở không gian gốc, phân phối t ở không gian mới) rồi cực tiểu hóa độ lệch KL giữa hai phân phối bằng gradient descent. Perplexity quyết định 'bao nhiêu láng giềng' được xét.",
        "formula": "min KL(P ‖ Q) = Σ pᵢⱼ log(pᵢⱼ / qᵢⱼ)",
        "pros": ["Tách cụm rất rõ, giữ cấu trúc cục bộ"],
        "cons": ["Khoảng cách giữa các cụm và kích thước cụm KHÔNG đáng tin", "Ngẫu nhiên, chậm với dữ liệu lớn", "Nhạy với perplexity"],
        "tip": "Thử perplexity từ 5 đến 50. Giá trị nhỏ cho nhiều cụm vụn, giá trị lớn gộp cụm lại.",
    },
    "UMAP": {
        "full": "Uniform Manifold Approximation and Projection", "vi": "Xấp xỉ và chiếu đa tạp đồng nhất", "group": "Nonlinear", "supervised": False,
        "desc": "Xây dựng đồ thị lân cận để biểu diễn cấu trúc dữ liệu trong không gian thấp chiều.",
        "idea": "Dựng đồ thị láng giềng gần có trọng số (tập đơn hình mờ) trong không gian gốc, rồi tối ưu bố cục ít chiều sao cho đồ thị tương ứng giống nhất theo cross-entropy.",
        "formula": "min Σ [ μᵢⱼ log(μᵢⱼ/νᵢⱼ) + (1−μᵢⱼ) log((1−μᵢⱼ)/(1−νᵢⱼ)) ]",
        "pros": ["Nhanh hơn t-SNE", "Giữ cấu trúc toàn cục tốt hơn t-SNE", "Có thể dùng cho dữ liệu mới"],
        "cons": ["Phụ thuộc n_neighbors và min_dist", "Ngẫu nhiên; khoảng cách vẫn chỉ mang tính tương đối"],
        "tip": "n_neighbors nhỏ → nhấn cấu trúc cục bộ; lớn → nhấn cấu trúc toàn cục. min_dist nhỏ → các điểm đứng sát nhau hơn.",
    },
    "Isomap": {
        "full": "Isometric Mapping", "vi": "Ánh xạ đẳng cự", "group": "Nonlinear", "supervised": False,
        "desc": "Ước lượng khoảng cách trắc địa trên đồ thị lân cận và bảo toàn chúng khi chiếu.",
        "idea": "Dựng đồ thị k-láng giềng, tính khoảng cách trắc địa (đường ngắn nhất dọc đồ thị) giữa mọi cặp điểm, rồi áp dụng MDS cổ điển lên ma trận đó để 'trải phẳng' đa tạp.",
        "formula": "D_geo = đường đi ngắn nhất trên đồ thị kNN → MDS cổ điển",
        "pros": ["Mở phẳng tốt đa tạp cuộn như Swiss Roll", "Xác định"],
        "cons": ["Rất nhạy với n_neighbors (quá lớn gây 'đoản mạch', quá nhỏ làm đồ thị đứt)", "Nhạy với nhiễu", "Chậm với n lớn"],
        "tip": "Thử Swiss Roll với n_neighbors = 5 rồi 15 để thấy hiện tượng 'đoản mạch' làm hỏng việc trải phẳng.",
    },
    "LLE": {
        "full": "Locally Linear Embedding", "vi": "Nhúng tuyến tính cục bộ", "group": "Nonlinear", "supervised": False,
        "desc": "Giữ lại quan hệ tái tạo tuyến tính giữa mỗi điểm và các láng giềng gần nhất.",
        "idea": "Biểu diễn mỗi điểm bằng tổ hợp tuyến tính của các láng giềng (tìm trọng số W), rồi tìm tọa độ ít chiều giữ nguyên các trọng số đó (vectơ riêng nhỏ nhất của (I−W)ᵀ(I−W)).",
        "formula": "min ‖xᵢ − Σⱼ wᵢⱼ xⱼ‖²  (Σⱼ wᵢⱼ = 1)  →  min ‖zᵢ − Σⱼ wᵢⱼ zⱼ‖²",
        "pros": ["Không cần tối ưu lặp phức tạp", "Giữ cấu trúc cục bộ"],
        "cons": ["Rất nhạy với n_neighbors và nhiễu", "Dễ co cụm lại, tạo biểu đồ méo"],
        "tip": "n_neighbors nên lớn hơn số chiều đầu ra. Nếu biểu đồ co thành vài điểm, hãy tăng n_neighbors.",
    },
    "Kernel PCA": {
        "full": "Kernel Principal Component Analysis", "vi": "Phân tích thành phần chính hạt nhân", "group": "Nonlinear", "supervised": False,
        "desc": "Dùng hàm kernel để mô hình hóa cấu trúc phi tuyến mà PCA thông thường khó nắm bắt.",
        "idea": "Làm PCA trong một không gian đặc trưng (rất nhiều chiều) mà không cần tính tường minh, nhờ hàm kernel K(x, y). Với kernel RBF, tham số gamma quyết định 'tầm nhìn' của kernel.",
        "formula": "K(x,y) = exp(−γ‖x−y‖²);  giải K̃·α = λ·α  (K̃ là kernel đã căn giữa)",
        "pros": ["Bắt được cấu trúc phi tuyến (vòng tròn, hai mặt trăng)", "Chọn được nhiều loại kernel"],
        "cons": ["Rất nhạy với gamma và thang đo", "O(n³), nặng với dữ liệu lớn", "Khó diễn giải trục"],
        "tip": "Với RBF, dữ liệu chưa chuẩn hóa thường làm kernel gần như ma trận đơn vị (mọi điểm 'xa' nhau) → hãy dùng Z-score hoặc chỉnh gamma.",
    },
}

# Tham số điều chỉnh được. kind: int | float | select | gamma. Giá trị min/max/default phụ thuộc dữ liệu → xem param_specs().
KERNELS = ["rbf", "poly", "sigmoid", "cosine", "linear"]


def param_specs(algo, n_samples, n_features, k):
    """Danh sách tham số của thuật toán, đã giới hạn theo kích thước dữ liệu hiện tại."""
    top = max(3, n_samples - 1)
    if algo == "t-SNE":
        hi = float(min(100, top))
        default = float(min(max(round(min(30.0, (n_samples - 1) / 3.0)), 2), hi))
        return [dict(key="perplexity", label="Perplexity", kind="float", min=2.0, max=hi, default=default, step=1.0,
                     help="Số láng giềng 'hiệu dụng' của mỗi điểm. Nhỏ → nhiều cụm vụn; lớn → gộp cụm.")]
    if algo == "UMAP":
        hi = int(min(100, top))
        return [dict(key="n_neighbors", label="n_neighbors", kind="int", min=2, max=hi, default=int(min(15, hi)),
                     help="Số láng giềng dùng dựng đồ thị. Nhỏ → cấu trúc cục bộ; lớn → cấu trúc toàn cục."),
                dict(key="min_dist", label="min_dist", kind="float", min=0.0, max=0.99, default=0.1, step=0.05,
                     help="Khoảng cách tối thiểu giữa các điểm trong biểu đồ. Nhỏ → điểm đứng sát nhau.")]
    if algo == "Isomap":
        hi = int(min(50, top))
        return [dict(key="n_neighbors", label="n_neighbors", kind="int", min=2, max=hi, default=int(min(5, hi)),
                     help="Số láng giềng dựng đồ thị trắc địa. Quá lớn gây 'đoản mạch', quá nhỏ làm đồ thị đứt.")]
    if algo == "LLE":
        lo = int(k) + 1
        hi = int(max(lo + 1, min(50, top)))
        return [dict(key="n_neighbors", label="n_neighbors", kind="int", min=lo, max=hi, default=int(min(max(5, lo), hi)),
                     help="Số láng giềng dùng tái tạo mỗi điểm. Nên lớn hơn số chiều đầu ra.")]
    if algo == "Kernel PCA":
        return [dict(key="kernel", label="Kernel", kind="select", options=KERNELS, default="rbf",
                     help="Hàm kernel. 'rbf' là lựa chọn phổ biến nhất."),
                dict(key="gamma", label="gamma", kind="gamma", default=1.0 / max(1, n_features),
                     help="Độ hẹp của kernel (rbf/poly/sigmoid). Tự động = 1 / số đặc trưng.")]
    if algo == "MDS":
        return [dict(key="max_iter", label="Số vòng lặp tối đa", kind="int", min=50, max=1000, default=300,
                     help="MDS chưa hội tụ nếu đạt đúng mức tối đa này."),
                dict(key="n_init", label="Số lần khởi tạo", kind="int", min=1, max=8, default=2,
                     help="Chạy nhiều lần từ các điểm khởi đầu ngẫu nhiên và giữ kết quả stress thấp nhất.")]
    return []
