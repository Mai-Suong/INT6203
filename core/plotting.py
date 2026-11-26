import pandas as pd
import plotly.express as px

def plot_embedding(Z, labels, dimensions, title):
    cols = [f"Dim {i+1}" for i in range(Z.shape[1])]
    plot_df = pd.DataFrame(Z, columns=cols)
    if labels is not None:
        plot_df["Nhãn"] = pd.Series(labels).astype(str).values
    color = "Nhãn" if labels is not None else None
    if dimensions == 1:
        plot_df["Trục phụ"] = 0
        fig = px.scatter(plot_df, x="Dim 1", y="Trục phụ", color=color, title=title)
        fig.update_yaxes(visible=False, showticklabels=False, title="")
        fig.update_traces(marker=dict(size=8, opacity=.8))
    elif dimensions == 2:
        fig = px.scatter(plot_df, x="Dim 1", y="Dim 2", color=color, title=title)
        fig.update_traces(marker=dict(size=8, opacity=.8))
    else:
        fig = px.scatter_3d(plot_df, x="Dim 1", y="Dim 2", z="Dim 3", color=color, title=title)
        fig.update_traces(marker=dict(size=4, opacity=.8))
    fig.update_layout(margin=dict(l=10, r=10, t=55, b=10), legend_title_text="Nhãn lớp")
    return fig
