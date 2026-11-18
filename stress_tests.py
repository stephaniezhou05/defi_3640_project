import math
import pandas as pd

from amm import ConstantProductAMM
from arbitrage import arbitrage_to_market
from risk_metrics import calculate_risk_metrics


INITIAL_PRICE = 3000
BASE_FEE = 0.003
MAX_FEE = 0.01


def dynamic_fee(market_price):
    shock = abs(math.log(market_price / INITIAL_PRICE))
    return min(MAX_FEE, BASE_FEE + 0.04 * shock)


def run_scenario(market_price, fee, strategy):
    amm = ConstantProductAMM(
        eth_reserve=100,
        usdc_reserve=300000,
        fee=fee
    )

    arb = arbitrage_to_market(amm, market_price)

    risk = calculate_risk_metrics(
        amm,
        initial_eth=100,
        initial_usdc=300000,
        market_price=market_price
    )

    return {
        "Shock (%)": (market_price / INITIAL_PRICE - 1) * 100,
        "Strategy": strategy,
        "Fee (%)": fee * 100,
        "LP vs HODL ($)": risk["LP vs HODL ($)"],
        "LP vs HODL (%)": risk["LP vs HODL (%)"],
        "Arb Profit ($)": arb["arbitrage_profit_usdc"],
        "Final AMM Price": arb["final_amm_price"],
        "Trade Amount": arb["trade_amount"]
    }


if __name__ == "__main__":
    shocks = [-50, -30, -20, -10, 0, 10, 20, 30, 50]

    results = []

    for shock in shocks:
        market_price = INITIAL_PRICE * (1 + shock / 100)

        results.append(
            run_scenario(
                market_price,
                BASE_FEE,
                "Fixed"
            )
        )

        results.append(
            run_scenario(
                market_price,
                dynamic_fee(market_price),
                "Dynamic"
            )
        )

    df = pd.DataFrame(results)

    print("\n=== STRESS TEST RESULTS ===")
    print(df.round(4).to_string(index=False))

    comparison = df.pivot(
        index="Shock (%)",
        columns="Strategy",
        values="LP vs HODL ($)"
    )

    comparison["Improvement ($)"] = (
        comparison["Dynamic"] - comparison["Fixed"]
    )

    print("\n=== DYNAMIC FEE COMPARISON ===")
    print(comparison.round(2).to_string())

    df.to_csv("stress_results.csv", index=False)

    print("\nSaved results to stress_results.csv")
