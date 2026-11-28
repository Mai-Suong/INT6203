"""Lõi thuật toán giảm chiều (scikit-learn + umap-learn). Không phụ thuộc Streamlit để dễ kiểm thử."""
import time
import warnings

import numpy as np
from sklearn.decomposition import PCA, KernelPCA, TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import MDS, TSNE, Isomap, LocallyLinearEmbedding, trustworthiness
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

MAX_TRUST_ROWS = 3000  # trustworthiness cần ma trận khoảng cách n×n → bỏ qua khi n quá lớn
SCREE_COMPONENTS = 15


def _fit_transform(name, X, n_components, y=None, params=None):
    p = params or {}
    n_samples, n_features = X.shape
    notes = []
    k = min(int(n_components), n_samples, n_features)

    if name == "LDA":
        if y is None:
            raise ValueError("LDA cần cột nhãn (Label column). Hãy chọn cột nhãn trước khi chạy.")
        n_classes = len(np.unique(y))
        if n_classes >= n_samples:
            raise ValueError("LDA cần số mẫu nhiều hơn số lớp. Cột nhãn đang chọn có quá nhiều giá trị khác nhau.")
        max_k = min(n_features, n_classes - 1)
        if max_k < 1:
            raise ValueError("LDA cần ít nhất 2 lớp dữ liệu.")
        k = min(k, max_k)
        model = LinearDiscriminantAnalysis(n_components=k)
        return model.fit_transform(X, y), k, None, notes

    if name == "PCA":
        model = PCA(n_components=k, random_state=42)
        Z = model.fit_transform(X)
        return Z, k, model.explained_variance_ratio_ * 100, notes

    if name == "SVD":
        model = TruncatedSVD(n_components=k, random_state=42)
        Z = model.fit_transform(X)
        return Z, k, model.explained_variance_ratio_ * 100, notes

    if name == "MDS":
        model = MDS(n_components=k, random_state=42, init="random",
                    n_init=int(p.get("n_init", 2)), max_iter=int(p.get("max_iter", 300)))
        Z = model.fit_transform(X)
        if model.n_iter_ >= int(p.get("max_iter", 300)):
            notes.append("MDS chưa hội tụ trong số vòng lặp cho phép. Hãy tăng 'Số vòng lặp tối đa' để bố cục ổn định hơn.")
        return Z, k, None, notes

    if name == "t-SNE":
        if n_samples < 4:
            raise ValueError("t-SNE cần ít nhất 4 mẫu dữ liệu.")
        auto = min(30.0, max(2.0, (n_samples - 1) / 3.0))
        perplexity = min(float(p.get("perplexity", auto)), n_samples - 1.0)
        model = TSNE(n_components=k, perplexity=perplexity, init="pca", learning_rate="auto", random_state=42)
        return model.fit_transform(X), k, None, notes

    if name == "UMAP":
        try:
            from umap import UMAP
        except ImportError as exc:
            raise ImportError("Chưa cài UMAP. Mở terminal và chạy: pip install umap-learn") from exc
        n_neighbors = max(2, min(int(p.get("n_neighbors", 15)), n_samples - 1))
        model = UMAP(n_components=k, n_neighbors=n_neighbors, min_dist=float(p.get("min_dist", 0.1)), random_state=42)
        return model.fit_transform(X), k, None, notes

    if name == "Isomap":
        n_neighbors = max(2, min(int(p.get("n_neighbors", 5)), n_samples - 1))
        model = Isomap(n_components=k, n_neighbors=n_neighbors)
        return model.fit_transform(X), k, None, notes

    if name == "LLE":
        n_neighbors = min(max(int(p.get("n_neighbors", max(5, k + 1))), k + 1), n_samples - 1)
        model = LocallyLinearEmbedding(n_components=k, n_neighbors=n_neighbors, random_state=42)
        return model.fit_transform(X), k, None, notes

    if name == "Kernel PCA":
        k = min(k, n_samples - 1)
        kernel = p.get("kernel", "rbf")
        gamma = p.get("gamma")  # None → scikit-learn dùng 1 / số đặc trưng
        model = KernelPCA(n_components=k, kernel=kernel, gamma=gamma, eigen_solver="arpack", random_state=42)
        return model.fit_transform(X), k, None, notes

    raise ValueError(f"Chưa hỗ trợ thuật toán {name}.")


def _safe_trustworthiness(X, Z):
    """Độ tin cậy lân cận (0–1): tỉ lệ láng giềng trong bản đồ mới thực sự là láng giềng ở không gian gốc."""
    n = len(X)
    nn = min(10, (n - 1) // 2)
    if nn < 1 or n > MAX_TRUST_ROWS:
        return None
    try:
        return float(trustworthiness(X, Z, n_neighbors=nn))
    except Exception:
        return None


def run_algorithm(name, X, n_components, y=None, standardize=False, params=None):
    """Chạy một thuật toán. Trả về dict: Z, k, variance (%, từng thành phần) hoặc None, elapsed (ms), trust, notes."""
    X_input = np.asarray(X, dtype=float)
    if standardize:
        X_input = StandardScaler().fit_transform(X_input)
    start = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        Z, actual_k, variance, notes = _fit_transform(name, X_input, n_components, y, params)
    elapsed_ms = (time.perf_counter() - start) * 1000
    notes = list(notes)
    if any("connected components" in str(w.message) for w in caught):
        notes.append("Đồ thị láng giềng không liên thông. scikit-learn đã tự nối các thành phần, nhưng kết quả kém tin cậy. Hãy tăng n_neighbors.")
    if name == "UMAP" and elapsed_ms > 5000:
        notes.append("Lần chạy UMAP đầu tiên gồm cả thời gian biên dịch (numba), nên thời gian hiển thị cao hơn các lần sau.")
    return {"Z": Z, "k": actual_k, "variance": variance, "elapsed": elapsed_ms,
            "trust": _safe_trustworthiness(X_input, Z), "notes": notes}


def variance_curve(name, X, standardize=False):
    """Phương sai (%) của từng thành phần, tối đa SCREE_COMPONENTS thành phần đầu, để vẽ scree plot (chỉ PCA/SVD)."""
    X_input = np.asarray(X, dtype=float)
    if standardize:
        X_input = StandardScaler().fit_transform(X_input)
    m = min(SCREE_COMPONENTS, X_input.shape[0], X_input.shape[1])
    model = PCA(n_components=m, random_state=42) if name == "PCA" else TruncatedSVD(n_components=m, random_state=42)
    model.fit(X_input)
    return model.explained_variance_ratio_ * 100


def label_separation(Z, labels):
    """Hệ số silhouette của các lớp trên embedding (−1…1). None nếu không có nhãn phân loại phù hợp."""
    if labels is None or len(labels) != len(Z):
        return None
    y = np.asarray(labels)
    if y.dtype.kind not in "OUS":  # nhãn số liên tục
        return None
    n_classes = len(np.unique(y))
    if n_classes < 2 or n_classes >= len(y):
        return None
    try:
        return float(silhouette_score(Z, y, sample_size=min(len(y), 2000), random_state=42))
    except Exception:
        return None
