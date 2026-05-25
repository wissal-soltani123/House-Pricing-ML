import streamlit as st
import pandas as pd
import numpy as np

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="House Pricing — AI Dashboard", layout="wide")

# ===============================
# THEME SWITCH 🌙
# ===============================
mode = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

if mode == "Dark":
    bg_color = "#0f172a"
    text_color = "#f1f5f9"
    card_color = "#1e293b"
else:
    bg_color = "#f8fafc"
    text_color = "#0f172a"
    card_color = "#ffffff"

st.markdown(f"""
<style>
.main {{
    background-color: {bg_color};
    color: {text_color};
}}
.card {{
    background-color: {card_color};
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}}
</style>
""", unsafe_allow_html=True)

# ===============================
# TITLE
# ===============================
st.markdown(f"<h1 style='text-align:center;'>🏠 AI House Price Dashboard</h1>", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================
train = pd.read_csv("C:/projetR/House Pricing R/data/Cleaned/train_clean.csv")
prediction = pd.read_csv("Prediction.csv")

train["SalePrice"] = np.exp(train["SalePrice"])

# ===============================
# KPIs (CARDS)
# ===============================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'><h3>Average Price</h3><h2>{int(train['SalePrice'].mean()):,} €</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><h3>Max Price</h3><h2>{int(train['SalePrice'].max()):,} €</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><h3>Min Price</h3><h2>{int(train['SalePrice'].min()):,} €</h2></div>", unsafe_allow_html=True)

# ===============================
# MODEL COMPARISON (PLOTLY 🔥)
# ===============================
st.subheader("🤖 Model Performance")

models = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest", "XGBoost"],
    "RMSE": [0.1299, 0.1449, 0.1304]
})

fig_model = px.bar(
    models,
    x="Model",
    y="RMSE",
    color="Model",
    text="RMSE",
    color_discrete_sequence=["#ff7f0e", "#94a3b8", "#111827"]
)

fig_model.update_layout(title="Model Comparison (RMSE — Lower is Better)")

st.plotly_chart(fig_model, use_container_width=True)

best_model = models.loc[models["RMSE"].idxmin(), "Model"]

st.success(f"🏆 Best Model: {best_model}")

# ===============================
# DISTRIBUTION (INTERACTIVE)
# ===============================
st.subheader("📈 Price Distribution")

fig_dist = px.histogram(
    train,
    x="SalePrice",
    nbins=40,
    title="Train Price Distribution",
    color_discrete_sequence=["#6366f1"]
)

st.plotly_chart(fig_dist, use_container_width=True)

# ===============================
# PREDICTIONS DISTRIBUTION
# ===============================
st.subheader("📊 Predicted Prices")

fig_pred = px.histogram(
    prediction,
    x="SalePrice",
    nbins=40,
    title="Predicted Prices Distribution",
    color_discrete_sequence=["#f97316"]
)

st.plotly_chart(fig_pred, use_container_width=True)

# ===============================
# TRAIN VS PREDICTION
# ===============================
st.subheader("📉 Train vs Prediction")

fig_compare = px.histogram(
    train,
    x="SalePrice",
    nbins=40,
    opacity=0.5,
)

fig_compare.add_histogram(x=prediction["SalePrice"], opacity=0.5)

fig_compare.update_layout(title="Train vs Prediction Distribution")

st.plotly_chart(fig_compare, use_container_width=True)

# ===============================
# FILTER 🔍
# ===============================
st.sidebar.header("🔍 Filters")

min_price = int(prediction["SalePrice"].min())
max_price = int(prediction["SalePrice"].max())

price_range = st.sidebar.slider(
    "Price Range",
    min_price,
    max_price,
    (min_price, max_price)
)

filtered = prediction[
    (prediction["SalePrice"] >= price_range[0]) &
    (prediction["SalePrice"] <= price_range[1])
]

# ===============================
# TOP HOUSES
# ===============================
st.subheader("💰 Top Houses")

st.dataframe(filtered.sort_values(by="SalePrice", ascending=False).head(10))

# ===============================
# AI EXPLANATION 🧠🔥
# ===============================
st.subheader("🧠 AI Explanation")

if best_model == "Linear Regression":
    explanation = """
    The Linear Regression model performs best, indicating that the relationship between variables and price is mostly linear after transformation.
    """
elif best_model == "XGBoost":
    explanation = """
    XGBoost captures complex relationships and interactions, showing strong predictive power.
    """
else:
    explanation = """
    Random Forest captures non-linear patterns but may struggle with high-dimensional data.
    """

st.markdown(f"<div class='card'>{explanation}</div>", unsafe_allow_html=True)