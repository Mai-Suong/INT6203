import time
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, TruncatedSVD, KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import MDS, TSNE, Isomap, LocallyLinearEmbedding


def _fit_transform(name, X, n_components, y=None):
    n_samples, n_features = X.shape
    k = min(int(n_components), n_samples, n_features)
    if name == "LDA":
        if y is None:
            raise ValueError("LDA cần cột nhãn (Label column). Hãy chọn cột nhãn trước khi chạy.")
        n_classes = len(np.unique(y))
        max_k = min(n_features, n_classes - 1)
        if max_k < 1:
            raise ValueError("LDA cần ít nhất 2 lớp dữ liệu.")
        k = min(k, max_k)
        model = LinearDiscriminantAnalysis(n_components=k)
        return model.fit_transform(X, y), k, None
    if name == "Kernel PCA":
        k = min(k, n_samples - 1)
    if name == "PCA":
        model = PCA(n_components=k, random_state=42)
        Z = model.fit_transform(X)
        return Z, k, model.explained_variance_ratio_ * 100
    if name == "SVD":
        model = TruncatedSVD(n_components=k, random_state=42)
        Z = model.fit_transform(X)
        return Z, k, model.explained_variance_ratio_ * 100
    if name == "MDS":
        model = MDS(n_components=k, random_state=42, n_init=1, max_iter=100, init="random")
    elif name == "t-SNE":
        if n_samples < 4:
            raise ValueError("t-SNE cần ít nhất 4 mẫu dữ liệu.")
        perplexity = min(30.0, max(2.0, (n_samples - 1) / 3.0))
        model = TSNE(n_components=k, perplexity=perplexity, init="pca", learning_rate="auto", random_state=42)
    elif name == "UMAP":
        try:
            from umap import UMAP
        except ImportError as exc:
            raise ImportError("Chưa cài UMAP. Mở terminal và chạy: pip install umap-learn") from exc
        model = UMAP(n_components=k, n_neighbors=min(15, n_samples - 1), random_state=42)
    elif name == "Isomap":
        model = Isomap(n_components=k, n_neighbors=min(5, n_samples - 1))
    elif name == "LLE":
        neighbors = min(max(5, k + 1), n_samples - 1)
        model = LocallyLinearEmbedding(n_components=k, n_neighbors=neighbors, random_state=42)
    elif name == "Kernel PCA":
        model = KernelPCA(n_components=k, kernel="rbf", eigen_solver="arpack", random_state=42)
    else:
        raise ValueError(f"Chưa hỗ trợ thuật toán {name}.")
    return model.fit_transform(X), k, None


def run_algorithm(name, X, n_components, y=None, standardize=False):
    X_input = np.asarray(X, dtype=float)
    if standardize:
        X_input = StandardScaler().fit_transform(X_input)
    start = time.perf_counter()
    Z, actual_k, variance = _fit_transform(name, X_input, n_components, y)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return Z, actual_k, variance, elapsed_ms
