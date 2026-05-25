
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ═══════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="House Pricing — AI Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], horizontal=True)
is_dark = theme == "Dark"

BG        = "#0f172a"    if is_dark else "#f8fafc"
SURFACE   = "#1e293b"    if is_dark else "#ffffff"
SURFACE2  = "#273549"    if is_dark else "#f1f5f9"
BORDER    = "#334155"    if is_dark else "#e2e8f0"
TEXT      = "#f1f5f9"    if is_dark else "#0f172a"
TEXT_MUTED= "#94a3b8"    if is_dark else "#64748b"
ACCENT    = "#6366f1"
ACCENT2   = "#f97316"
SUCCESS   = "#22c55e"
DANGER    = "#ef4444"
WARNING   = "#f59e0b"
GRID_C    = "#334155"    if is_dark else "#e2e8f0"
PLOT_BG   = SURFACE
FIG_BG    = BG if is_dark else "#f8fafc"

# ═══════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
}}

[data-testid="stSidebar"] {{
    background-color: {SURFACE} !important;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

section[data-testid="stSidebar"] .stRadio label {{
    font-size: 14px;
    color: {TEXT_MUTED} !important;
}}

h1, h2, h3, h4 {{ color: {TEXT} !important; font-family: 'DM Sans', sans-serif !important; }}

.metric-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 20px 24px;
    height: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
}}
.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}}
.metric-label {{
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    margin-bottom: 6px;
}}
.metric-value {{
    font-size: 28px;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 2px;
    font-variant-numeric: tabular-nums;
}}
.metric-sub {{
    font-size: 13px;
    color: {TEXT_MUTED};
}}
.badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
}}
.badge-best {{
    background: rgba(99,102,241,0.15);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.3);
}}
.badge-good {{
    background: rgba(34,197,94,0.12);
    color: #4ade80;
    border: 1px solid rgba(34,197,94,0.25);
}}
.badge-avg {{
    background: rgba(249,115,22,0.12);
    color: #fb923c;
    border: 1px solid rgba(249,115,22,0.25);
}}
.model-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 22px 24px;
    height: 100%;
    position: relative;
    overflow: hidden;
}}
.model-card.best {{
    border: 2px solid {ACCENT};
    background: linear-gradient(135deg, {SURFACE}, rgba(99,102,241,0.08));
}}
.model-card-name {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT};
    margin-bottom: 4px;
}}
.model-card-rmse {{
    font-size: 36px;
    font-weight: 700;
    color: {ACCENT};
    font-variant-numeric: tabular-nums;
    margin: 10px 0 6px;
    font-family: 'DM Mono', monospace;
}}
.model-card-desc {{
    font-size: 12px;
    color: {TEXT_MUTED};
    margin-top: 8px;
}}
.insight-box {{
    background: {SURFACE};
    border-left: 4px solid {ACCENT};
    border-radius: 0 12px 12px 0;
    padding: 18px 22px;
    margin: 12px 0;
}}
.insight-box p {{
    margin: 0;
    color: {TEXT};
    font-size: 15px;
    line-height: 1.65;
}}
.section-header {{
    font-size: 18px;
    font-weight: 600;
    color: {TEXT};
    margin: 28px 0 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.section-header::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {BORDER};
    margin-left: 12px;
}}
.hero-title {{
    font-size: 38px;
    font-weight: 700;
    color: {TEXT};
    margin: 0;
    line-height: 1.2;
}}
.hero-sub {{
    font-size: 15px;
    color: {TEXT_MUTED};
    margin-top: 6px;
}}
.stat-row {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 18px 0;
}}
.stat-pill {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    color: {TEXT_MUTED};
}}
.stat-pill span {{
    font-weight: 600;
    color: {TEXT};
    margin-left: 4px;
}}
.price-tag {{
    background: linear-gradient(135deg, {ACCENT}, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 20px 28px;
    text-align: center;
}}
.price-tag .label {{
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 4px;
}}
.price-tag .value {{
    font-size: 42px;
    font-weight: 700;
    font-family: 'DM Mono', monospace;
}}
.stDataFrame {{ border-radius: 12px; overflow: hidden; }}
div[data-testid="stDataFrame"] > div {{ border-radius: 12px !important; }}

.stSelectbox > div > div {{
    background: {SURFACE2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}
.stSlider > div {{ color: {TEXT_MUTED}; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MATPLOTLIB THEME
# ═══════════════════════════════════════════
def apply_mpl_theme():
    plt.rcParams.update({
        "figure.facecolor":  FIG_BG,
        "axes.facecolor":    PLOT_BG,
        "axes.edgecolor":    BORDER,
        "axes.labelcolor":   TEXT_MUTED,
        "axes.titlecolor":   TEXT,
        "axes.grid":         True,
        "grid.color":        GRID_C,
        "grid.linewidth":    0.6,
        "grid.alpha":        0.6,
        "xtick.color":       TEXT_MUTED,
        "ytick.color":       TEXT_MUTED,
        "text.color":        TEXT,
        "font.family":       "sans-serif",
        "figure.dpi":        130,
    })

apply_mpl_theme()

# ═══════════════════════════════════════════
# DATA LOADING — robust paths
# ═══════════════════════════════════════════
@st.cache_data
def load_data():
    # Try multiple paths for train CSV
    train_candidates = [
        "train_clean.csv",
        "data/Cleaned/train_clean.csv",
        "C:/Users/guerf/OneDrive/Documenti/Bureau/House Pricing R/data/Cleaned/train_clean.csv",
    ]
    pred_candidates = [
        "Prediction.csv",
        "prediction.csv",
        "data/Prediction.csv",
    ]

    train_df = None
    for path in train_candidates:
        if os.path.exists(path):
            train_df = pd.read_csv(path)
            break

    pred_df = None
    for path in pred_candidates:
        if os.path.exists(path):
            pred_df = pd.read_csv(path)
            break

    return train_df, pred_df

train_raw, pred = load_data()

# ═══════════════════════════════════════════
# DEMO DATA FALLBACK
# ═══════════════════════════════════════════
USE_DEMO = train_raw is None or pred is None

if USE_DEMO:
    rng = np.random.default_rng(42)
    n_train = 1460
    n_pred  = 500

    log_prices = rng.normal(12.0, 0.4, n_train)
    train_raw  = pd.DataFrame({
        "SalePrice":    log_prices,
        "GrLivArea":    rng.integers(600, 4000, n_train),
        "OverallQual":  rng.integers(1, 11, n_train),
        "YearBuilt":    rng.integers(1900, 2010, n_train),
        "Neighborhood": rng.choice(["NAmes","CollgCr","OldTown","Edwards","Somerst"], n_train),
    })

    sale_prices = np.exp(rng.normal(12.0, 0.4, n_pred)).round(0)
    pred = pd.DataFrame({
        "Id":        np.arange(1, n_pred + 1),
        "SalePrice": sale_prices,
    })

    st.sidebar.warning("⚠️ Demo data — place your CSV files next to app.py to use real data.")

train = train_raw.copy()
train["SalePrice"] = np.exp(train["SalePrice"])

# ═══════════════════════════════════════════
# MODEL DATA
# ═══════════════════════════════════════════
MODELS = [
    {"name": "Linear Regression", "rmse": 0.1299, "cv": 0.1312, "r2": 0.897, "desc": "Interpretable · Stable · Fast"},
    {"name": "Random Forest",     "rmse": 0.1449, "cv": 0.1481, "r2": 0.874, "desc": "Robust · Handles non-linearity"},
    {"name": "XGBoost",           "rmse": 0.1304, "cv": 0.1318, "r2": 0.895, "desc": "Powerful · Gradient boosting"},
]
model_df   = pd.DataFrame(MODELS)
best_idx   = model_df["rmse"].idxmin()
best_model = model_df.loc[best_idx, "name"]

# ═══════════════════════════════════════════
# SIDEBAR — FILTERS
# ═══════════════════════════════════════════
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

min_p = int(pred["SalePrice"].min())
max_p = int(pred["SalePrice"].max())
price_range = st.sidebar.slider(
    "Price range (€)",
    min_value=min_p,
    max_value=max_p,
    value=(min_p, max_p),
    format="€%d",
)
top_n = st.sidebar.select_slider("Top N houses", options=[5, 10, 20, 50], value=10)

filtered = pred[
    (pred["SalePrice"] >= price_range[0]) &
    (pred["SalePrice"] <= price_range[1])
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='font-size:12px; color:{TEXT_MUTED}; line-height:1.8;'>
<b style='color:{TEXT};'>Dataset</b><br>
Train samples: <b style='color:{TEXT};'>{len(train):,}</b><br>
Predictions: <b style='color:{TEXT};'>{len(pred):,}</b><br>
Filtered: <b style='color:{TEXT};'>{len(filtered):,}</b>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════
col_t, col_s = st.columns([3, 1])
with col_t:
    st.markdown(f"""
    <div class="hero-title">🏠 AI House Pricing Dashboard</div>
    <div class="hero-sub">Model comparison &nbsp;·&nbsp; Predictions &nbsp;·&nbsp; Distribution analysis</div>
    """, unsafe_allow_html=True)
with col_s:
    avg_pred  = int(pred["SalePrice"].mean())
    avg_train = int(train["SalePrice"].mean())
    delta_pct = (avg_pred - avg_train) / avg_train * 100
    sign = "+" if delta_pct >= 0 else ""
    st.markdown(f"""
    <div class="metric-card" style="text-align:right;">
        <div class="metric-label">Avg predicted price</div>
        <div class="metric-value">€{avg_pred:,}</div>
        <div class="metric-sub" style="color:{'#4ade80' if delta_pct>=0 else '#f87171'}">
            {sign}{delta_pct:.1f}% vs train avg
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── KPI row ────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpi_data = [
    ("Best RMSE",      f"{model_df['rmse'].min():.4f}",     best_model,     ACCENT),
    ("Predictions",    f"{len(pred):,}",                    "Test houses",  "#22c55e"),
    ("Train size",     f"{len(train):,}",                   "Samples",      "#f97316"),
    ("Filtered",       f"{len(filtered):,}",                "In range",     "#8b5cf6"),
]
for col, (label, val, sub, color) in zip([k1, k2, k3, k4], kpi_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color}">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# MODEL CARDS
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">🤖 Model performance</div>', unsafe_allow_html=True)
mcols = st.columns(3)
badge_map = {True: ("badge-best", "★ Best"), False: ("badge-avg", "Candidate")}

for col, row in zip(mcols, MODELS):
    is_best = row["name"] == best_model
    badge_cls, badge_txt = badge_map[is_best]
    card_cls = "model-card best" if is_best else "model-card"
    color_rmse = ACCENT if is_best else TEXT_MUTED
    with col:
        st.markdown(f"""
        <div class="{card_cls}">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
                <div class="model-card-name">{row['name']}</div>
                <span class="badge {badge_cls}">{badge_txt}</span>
            </div>
            <div class="model-card-rmse" style="color:{color_rmse}">{row['rmse']:.4f}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin:10px 0;">
                <div style="background:{SURFACE2}; border-radius:8px; padding:8px 10px;">
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-bottom:2px;">CV RMSE</div>
                    <div style="font-size:15px; font-weight:600; color:{TEXT}; font-family:'DM Mono',monospace;">{row['cv']:.4f}</div>
                </div>
                <div style="background:{SURFACE2}; border-radius:8px; padding:8px 10px;">
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-bottom:2px;">R²</div>
                    <div style="font-size:15px; font-weight:600; color:{TEXT}; font-family:'DM Mono',monospace;">{row['r2']:.3f}</div>
                </div>
            </div>
            <div class="model-card-desc">{row['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# CHARTS ROW 1 — RMSE bar + R² bar
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">📊 Comparative metrics</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

with ch1:
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    colors_ = [ACCENT if m["name"] == best_model else TEXT_MUTED for m in MODELS]
    names   = [m["name"].replace(" ", "\n") for m in MODELS]
    rmses   = [m["rmse"] for m in MODELS]
    bars    = ax.bar(names, rmses, color=colors_, width=0.5, zorder=2, linewidth=0)
    ax.set_title("RMSE  (lower = better)", pad=10, fontsize=13, fontweight="600")
    ax.set_ylabel("RMSE")
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
    for bar, val in zip(bars, rmses):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.001,
                f"{val:.4f}", ha="center", va="bottom",
                fontsize=11, fontweight="600", color=TEXT, fontfamily="monospace")
    ax.set_ylim(0, max(rmses) * 1.18)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

with ch2:
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    r2s    = [m["r2"] for m in MODELS]
    colors_r = ["#22c55e" if r == max(r2s) else TEXT_MUTED for r in r2s]
    bars2  = ax.bar(names, r2s, color=colors_r, width=0.5, zorder=2, linewidth=0)
    ax.set_title("R²  (higher = better)", pad=10, fontsize=13, fontweight="600")
    ax.set_ylabel("R²")
    for bar, val in zip(bars2, r2s):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.002,
                f"{val:.3f}", ha="center", va="bottom",
                fontsize=11, fontweight="600", color=TEXT, fontfamily="monospace")
    ax.set_ylim(0.82, max(r2s) * 1.06)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ═══════════════════════════════════════════
# CHARTS ROW 2 — distributions
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">📈 Price distributions</div>', unsafe_allow_html=True)
d1, d2 = st.columns(2)

def dist_plot(data, color, title, ax):
    n, bins, patches = ax.hist(data, bins=35, color=color, alpha=0.85,
                                edgecolor="none", zorder=2)
    ax.axvline(data.mean(),   color="#f8fafc", linewidth=1.5, linestyle="--", alpha=0.9, label=f"Mean: €{data.mean():,.0f}")
    ax.axvline(data.median(), color="#fbbf24", linewidth=1.5, linestyle=":",  alpha=0.9, label=f"Median: €{data.median():,.0f}")
    ax.legend(fontsize=10, framealpha=0.15, labelcolor=TEXT)
    ax.set_title(title, pad=10, fontsize=13, fontweight="600")
    ax.set_xlabel("Price (€)")
    ax.set_ylabel("Count")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x/1000:.0f}k"))
    ax.spines[["top", "right"]].set_visible(False)

with d1:
    fig1, ax1 = plt.subplots(figsize=(5.5, 3.4))
    dist_plot(train["SalePrice"], ACCENT, "Train data — SalePrice", ax1)
    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close()

with d2:
    fig2, ax2 = plt.subplots(figsize=(5.5, 3.4))
    dist_plot(pred["SalePrice"], ACCENT2, "Predictions — SalePrice", ax2)
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close()

# ═══════════════════════════════════════════
# SCATTER — price vs index
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">🔵 Prediction scatter</div>', unsafe_allow_html=True)
fig3, ax3 = plt.subplots(figsize=(11, 3.2))
sorted_pred = pred.sort_values("SalePrice").reset_index(drop=True)
sc = ax3.scatter(sorted_pred.index, sorted_pred["SalePrice"],
                 c=sorted_pred["SalePrice"], cmap="coolwarm",
                 s=12, alpha=0.75, linewidths=0, zorder=2)
cb = fig3.colorbar(sc, ax=ax3, pad=0.01)
cb.ax.yaxis.set_tick_params(color=TEXT_MUTED)
cb.outline.set_edgecolor(BORDER)
plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT_MUTED, fontsize=9)
ax3.axhline(sorted_pred["SalePrice"].mean(), color=ACCENT2, linewidth=1.5,
            linestyle="--", alpha=0.8, label=f"Mean €{sorted_pred['SalePrice'].mean():,.0f}")
ax3.legend(fontsize=10, framealpha=0.15, labelcolor=TEXT)
ax3.set_xlabel("Rank (sorted by price)")
ax3.set_ylabel("Predicted price (€)")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x/1000:.0f}k"))
ax3.spines[["top", "right"]].set_visible(False)
fig3.tight_layout()
st.pyplot(fig3, use_container_width=True)
plt.close()

# ═══════════════════════════════════════════
# TOP PREDICTIONS TABLE
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">💰 Top {top_n} predictions</div>', unsafe_allow_html=True)

top_df = (
    filtered
    .sort_values("SalePrice", ascending=False)
    .head(top_n)
    .copy()
)
top_df["Price (€)"] = top_df["SalePrice"].apply(lambda x: f"€{int(x):,}")
top_df["vs Mean"]   = top_df["SalePrice"].apply(
    lambda x: f"+{(x/pred['SalePrice'].mean()-1)*100:.1f}%"
    if x >= pred["SalePrice"].mean()
    else f"{(x/pred['SalePrice'].mean()-1)*100:.1f}%"
)
display_cols = ["Id", "Price (€)", "vs Mean"]
if "GrLivArea" in top_df.columns: display_cols.insert(2, "GrLivArea")

st.dataframe(
    top_df[display_cols].reset_index(drop=True),
    use_container_width=True,
    height=min(42 * top_n + 50, 460),
)

# ═══════════════════════════════════════════
# EXPLORE A HOUSE
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">🏡 Explore a house</div>', unsafe_allow_html=True)
sel_id = st.selectbox("Select house ID", pred["Id"].tolist(), label_visibility="collapsed")
row    = pred[pred["Id"] == sel_id]

if not row.empty:
    price = int(row["SalePrice"].values[0])
    pct   = (price / pred["SalePrice"].mean() - 1) * 100
    e1, e2, e3 = st.columns([2, 1, 1])

    with e1:
        st.markdown(f"""
        <div class="price-tag">
            <div class="label">Predicted sale price</div>
            <div class="value">€{price:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with e2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">vs mean price</div>
            <div class="metric-value" style="color:{'#4ade80' if pct>=0 else '#f87171'}">
                {'+'if pct>=0 else ''}{pct:.1f}%
            </div>
            <div class="metric-sub">Population avg €{int(pred['SalePrice'].mean()):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with e3:
        rank = int((pred["SalePrice"] <= price).sum())
        pct_rank = rank / len(pred) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Percentile rank</div>
            <div class="metric-value">{pct_rank:.0f}th</div>
            <div class="metric-sub">Rank {rank:,} of {len(pred):,}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# AI INSIGHTS
# ═══════════════════════════════════════════
st.markdown(f'<div class="section-header">🧠 Model insights</div>', unsafe_allow_html=True)

insight_map = {
    "Linear Regression": (
        "Linear Regression achieves the best RMSE, suggesting the log-transformed SalePrice "
        "is largely explained by linear feature relationships. This simplicity is a strength: "
        "the model generalises well without overfitting the training noise."
    ),
    "XGBoost": (
        "XGBoost closely rivals Linear Regression thanks to its ability to capture non-linear "
        "interactions. The small gap in RMSE indicates the data structure is largely linear, "
        "yet XGBoost's flexibility provides a useful safety net for outlier properties."
    ),
    "Random Forest": (
        "Random Forest is the most robust to outliers but shows a higher RMSE, hinting at "
        "mild overfitting on bagged trees. Tuning max_features and n_estimators or stacking "
        "it with a linear model could close the gap significantly."
    ),
}

for m in MODELS:
    is_best = m["name"] == best_model
    accent  = ACCENT if is_best else BORDER
    icon    = "★ " if is_best else ""
    st.markdown(f"""
    <div class="insight-box" style="border-left-color:{accent};">
        <p><b style="color:{TEXT}">{icon}{m['name']}</b> &mdash; {insight_map.get(m['name'], '')}</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:40px; padding-top:20px; border-top:1px solid {BORDER};
            text-align:center; font-size:12px; color:{TEXT_MUTED};">
    AI House Pricing Dashboard &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp;
    Models: Linear Regression · Random Forest · XGBoost
</div>
""", unsafe_allow_html=True)