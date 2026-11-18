
from amm import ConstantProductAMM
from arbitrage import arbitrage_to_market
import math


def calculate_risk_metrics(amm, initial_eth, initial_usdc, market_price):
    # Value of assets remaining in the AMM
    lp_value = amm.eth * market_price + amm.usdc

    # Value if the LP had simply held the assets
    hodl_value = (
        initial_eth * market_price + initial_usdc
    )

    # Difference relative to HODL, including fees
    lp_underperformance = lp_value - hodl_value

    relative_underperformance = (
        lp_underperformance / hodl_value * 100
    )

    # Theoretical impermanent loss without fees
    initial_price = initial_usdc / initial_eth
    price_ratio = market_price / initial_price

    theoretical_il = (
        2 * math.sqrt(price_ratio)
        / (1 + price_ratio) - 1
    ) * 100

    return {
        "LP value ($)": lp_value,
        "HODL value ($)": hodl_value,
        "LP vs HODL ($)": lp_underperformance,
        "LP vs HODL (%)": relative_underperformance,
        "Theoretical fee-free IL (%)": theoretical_il,
        "USDC fees collected": amm.total_fees_usdc,
        "ETH fees collected": amm.total_fees_eth,
    }


if __name__ == "__main__":
    scenarios = {
        "20% crash": 2400,
        "20% increase": 3600,
        "No change": 3000,
    }

    for name, market_price in scenarios.items():
        amm = ConstantProductAMM()
        initial_eth = amm.eth
        initial_usdc = amm.usdc

        arbitrage_to_market(amm, market_price)

        metrics = calculate_risk_metrics(
            amm, initial_eth, initial_usdc,
            market_price
        )

        print(f"\n--- {name} ---")

        for key, value in metrics.items():
            print(f"{key}: {value:.4f}")
