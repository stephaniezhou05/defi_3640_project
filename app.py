import pandas as pd
import plotly.express as px
import streamlit as st

from stress_tests import BASE_FEE, INITIAL_PRICE, dynamic_fee, run_scenario

SHOCKS = [-50, -30, -20, -10, 0, 10, 20, 30, 50]

st.set_page_config(page_title="DeFi Stress Lab", layout="wide")
st.title("DeFi Stress Lab")
st.caption("Constant-product AMM (xy = k) under market shocks. Fixed vs dynamic fees.")

shock = st.sidebar.selectbox("Highlighted shock (%)", SHOCKS, index=2)

results = []
for s in SHOCKS:
    market_price = INITIAL_PRICE * (1 + s / 100)
    results.append(run_scenario(market_price, BASE_FEE, "Fixed"))
    results.append(run_scenario(market_price, dynamic_fee(market_price), "Dynamic"))

df = pd.DataFrame(results)
selected = df[df["Shock (%)"].round().astype(int) == int(shock)]
fixed = selected[selected["Strategy"] == "Fixed"].iloc[0]
dyn = selected[selected["Strategy"] == "Dynamic"].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("LP vs HODL (Fixed)", f"${fixed['LP vs HODL ($)']:.0f}")
col2.metric("LP vs HODL (Dynamic)", f"${dyn['LP vs HODL ($)']:.0f}")
col3.metric("Arb profit (Fixed)", f"${fixed['Arb Profit ($)']:.0f}")

st.plotly_chart(
    px.line(
        df,
        x="Shock (%)",
        y="LP vs HODL ($)",
        color="Strategy",
        markers=True,
        title="LP Performance: Fixed vs Dynamic Fees",
    ),
    use_container_width=True,
)

st.dataframe(df.round(2), use_container_width=True)
