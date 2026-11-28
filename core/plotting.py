"""Vẽ biểu đồ Plotly: embedding 1D/2D/3D (nhãn phân loại hoặc liên tục) và scree plot."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.data import is_continuous_label

NAVY = "#001C44"
TEAL = "#2D99AE"


def _sort_key(value):
    try:
        return (0, float(value), "")
    except ValueError:
        return (1, 0.0, value)


def plot_embedding(Z, labels, dimensions, title, label_name="Nhãn"):
    """labels: pandas Series/array hoặc None. Nhãn số liên tục được tô bằng thang màu thay vì từng lớp."""
    dimensions = int(dimensions)
    cols = [f"Dim {i + 1}" for i in range(Z.shape[1])]
    df = pd.DataFrame(Z, columns=cols)
    df.insert(0, "Mẫu", np.arange(len(df)))

    color, continuous, orders = None, False, {}
    if labels is not None:
        s = pd.Series(np.asarray(labels))
        continuous = is_continuous_label(s)
        if continuous:
            df[label_name] = s.astype(float).to_numpy()
        else:
            df[label_name] = s.astype(str).to_numpy()
            orders = {label_name: sorted(df[label_name].unique(), key=_sort_key)}
        color = label_name

    common = dict(color=color, hover_data={"Mẫu": True}, title=title)
    if continuous:
        common["color_continuous_scale"] = "Viridis"
    else:
        common["category_orders"] = orders

    if dimensions == 1:
        # Một chiều: rải ngẫu nhiên (jitter) theo trục dọc cho các điểm khỏi chồng lên nhau
        df["Jitter"] = np.random.default_rng(0).uniform(-0.5, 0.5, len(df))
        fig = px.scatter(df, x="Dim 1", y="Jitter", **common)
        fig.update_yaxes(visible=False, showticklabels=False, title="", range=[-1.2, 1.2])
        fig.update_traces(marker=dict(size=8, opacity=.75))
    elif dimensions == 2 or Z.shape[1] == 2:
        fig = px.scatter(df, x="Dim 1", y="Dim 2", **common)
        fig.update_traces(marker=dict(size=7, opacity=.8))
    else:
        fig = px.scatter_3d(df, x="Dim 1", y="Dim 2", z="Dim 3", **common)
        fig.update_traces(marker=dict(size=3.5, opacity=.85))

    fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=55, b=10), height=470,
                      legend_title_text=label_name, title=dict(font=dict(size=16)))
    return fig


def plot_scree(variance, title="Scree plot"):
    """Cột: phương sai từng thành phần; đường: phương sai cộng dồn."""
    comps = [f"PC{i + 1}" for i in range(len(variance))]
    fig = go.Figure()
    fig.add_bar(x=comps, y=variance, name="Từng thành phần", marker_color=TEAL,
                hovertemplate="%{x}: %{y:.2f}%<extra></extra>")
    fig.add_scatter(x=comps, y=np.cumsum(variance), name="Cộng dồn", mode="lines+markers",
                    line=dict(color=NAVY, width=2), hovertemplate="%{x}: %{y:.2f}%<extra></extra>")
    fig.update_layout(template="plotly_white", title=dict(text=title, font=dict(size=16)), height=340,
                      margin=dict(l=10, r=10, t=55, b=10), yaxis=dict(title="Phương sai (%)", range=[0, 105]),
                      legend=dict(orientation="h", y=-0.2))
    return fig
