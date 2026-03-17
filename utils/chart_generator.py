import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
def _apply_style(fig, ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize= 10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
def _save_to_bytes(fig):
    buf= io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    image_bytes = buf.getvalue()
    plt.close(fig)
    return image_bytes
def bar_chart(df, x_col, y_col, title=""):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    colors = plt.cm.Blues([0.4 + 0.5 * i / len(df) for i in range(len(df))])
    
    ax.bar(df[x_col].astype(str), df[y_col], color=colors, edgecolor="white", linewidth=0.5)
    
    if len(df) > 5:
        plt.xticks(rotation=35, ha="right")
    
    _apply_style(fig, ax, title or f"{y_col} by {x_col}", x_col, y_col)
    return _save_to_bytes(fig)
def line_chart(df, x_col, y_col, title=""):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    ax.plot(df[x_col].astype(str), df[y_col],
            marker="o", linewidth=2, color="#2563EB",
            markersize=6, markerfacecolor="white", markeredgewidth=2)
    
    ax.fill_between(range(len(df)), df[y_col], alpha=0.1, color="#2563EB")
    
    if len(df) > 5:
        plt.xticks(rotation=35, ha="right")
    
    _apply_style(fig, ax, title or f"{y_col} over {x_col}", x_col, y_col)
    return _save_to_bytes(fig)
def pie_chart(df, label_col, value_col, title=""):
    fig, ax = plt.subplots(figsize=(7, 6))
    
    wedges, texts, autotexts = ax.pie(
        df[value_col],
        labels=df[label_col],
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Set2.colors,
        pctdistance=0.75,
        wedgeprops={"linewidth": 1.5, "edgecolor": "white"}
    )
    
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    
    ax.set_title(title or f"{value_col} distribution", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    return _save_to_bytes(fig)
def horizontal_bar_chart(df, x_col, y_col, title=""):
    fig, ax = plt.subplots(figsize=(9, max(4, len(df) * 0.5)))
    
    colors = plt.cm.Purples([0.4 + 0.5 * i / len(df) for i in range(len(df))])
    
    ax.barh(df[x_col].astype(str), df[y_col], color=colors, edgecolor="white")
    
    _apply_style(fig, ax, title or f"{y_col} by {x_col}", y_col, x_col)
    return _save_to_bytes(fig)