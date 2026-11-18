
import pandas as pd
import plotly.express as px

df = pd.read_csv("stress_results.csv")

# Figure 1: LP performance comparison
fig1 = px.line(
    df,
    x="Shock (%)",
    y="LP vs HODL ($)",
    color="Strategy",
    markers=True,
    title="LP Performance: Fixed vs Dynamic Fees",
    labels={"LP vs HODL ($)": "LP vs HODL (USD)"}
)
fig1.update_layout(template="plotly_white")
fig1.write_html("figure1_lp_performance.html")
fig1.show()


# Figure 2: Improvement from dynamic fees
comparison = df.pivot(
    index="Shock (%)",
    columns="Strategy",
    values="LP vs HODL ($)"
).reset_index()

comparison["Improvement ($)"] = (
    comparison["Dynamic"] - comparison["Fixed"]
)

fig2 = px.bar(
    comparison,
    x="Shock (%)",
    y="Improvement ($)",
    title="LP Improvement from Dynamic Fees",
    labels={"Improvement ($)": "Improvement (USD)"}
)
fig2.update_layout(template="plotly_white")
fig2.write_html("figure2_improvement.html")
fig2.show()


# Figure 3: Fee adjustment mechanism
fig3 = px.line(
    df,
    x="Shock (%)",
    y="Fee (%)",
    color="Strategy",
    markers=True,
    title="Trading Fees Across Market Shocks",
    labels={"Fee (%)": "Trading Fee (%)"}
)
fig3.update_layout(template="plotly_white")
fig3.write_html("figure3_fees.html")
fig3.show()

print("Successfully generated three figures!")
