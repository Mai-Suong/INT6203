import numpy as np
import pandas as pd
from sklearn import datasets

SAMPLE_DATASETS = ["Iris", "Wine", "Breast Cancer", "Digits", "Swiss Roll"]

def load_sample(name: str):
    if name == "Iris":
        bunch = datasets.load_iris(as_frame=True)
        df = bunch.data.copy(); labels = pd.Series(bunch.target_names[bunch.target], name="label")
    elif name == "Wine":
        bunch = datasets.load_wine(as_frame=True)
        df = bunch.data.copy(); labels = pd.Series(bunch.target_names[bunch.target], name="label")
    elif name == "Breast Cancer":
        bunch = datasets.load_breast_cancer(as_frame=True)
        df = bunch.data.copy(); labels = pd.Series(bunch.target_names[bunch.target], name="label")
    elif name == "Digits":
        bunch = datasets.load_digits()
        df = pd.DataFrame(bunch.data, columns=[f"pixel_{i}" for i in range(bunch.data.shape[1])])
        labels = pd.Series(bunch.target.astype(str), name="label")
    else:
        X, color = datasets.make_swiss_roll(n_samples=900, noise=0.08, random_state=42)
        df = pd.DataFrame(X, columns=["x", "y", "z"])
        labels = pd.Series(color, name="label")
    return df.reset_index(drop=True), labels.reset_index(drop=True)

def clean_feature_frame(df: pd.DataFrame, feature_cols):
    X = df.loc[:, feature_cols].apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan)
    return X
