
from amm import ConstantProductAMM


def arbitrage_to_market(amm, market_price):
    """
    Simulate an arbitrageur trading until
    the AMM reaches the no-arbitrage fee band.
    """
    initial_price = amm.price
    initial_eth = amm.eth
    initial_usdc = amm.usdc
    fee = amm.fee

    if not 0 <= fee < 1:
        raise ValueError("Fee must be between 0 and 1.")
    if market_price <= 0:
        raise ValueError("Market price must be positive.")

    # ETH is overpriced in the pool:
    # arbitrageur sells ETH to the AMM.
    if market_price < initial_price * (1 - fee):
        target_price = market_price / (1 - fee)

        # Solve for the required ETH input,
        # accounting for fees retained in reserves.
        a = 1 - fee
        eth_in = (
            -(2 - fee) * initial_eth
            + (
                (fee * initial_eth) ** 2
                + 4 * a * initial_usdc * initial_eth
                / target_price
            ) ** 0.5
        ) / (2 * a)

        usdc_out = amm.sell_eth(eth_in)
        profit = usdc_out - eth_in * market_price
        direction = "Sell ETH into AMM"
        amount = eth_in

    # ETH is underpriced in the pool:
    # arbitrageur buys ETH from the AMM.
    elif market_price > initial_price / (1 - fee):
        target_price = market_price * (1 - fee)

        a = 1 - fee
        usdc_in = (
            -(2 - fee) * initial_usdc
            + (
                (fee * initial_usdc) ** 2
                + 4 * a * initial_eth * initial_usdc
                * target_price
            ) ** 0.5
        ) / (2 * a)

        eth_out = amm.buy_eth(usdc_in)
        profit = eth_out * market_price - usdc_in
        direction = "Buy ETH from AMM"
        amount = usdc_in

    else:
        direction = "No arbitrage"
        amount = 0.0
        profit = 0.0

    return {
        "market_price": market_price,
        "initial_amm_price": initial_price,
        "final_amm_price": amm.price,
        "direction": direction,
        "trade_amount": amount,
        "arbitrage_profit_usdc": profit,
        "final_eth_reserve": amm.eth,
        "final_usdc_reserve": amm.usdc,
    }


if __name__ == "__main__":
    scenarios = {
        "20% crash": 2400,
        "20% increase": 3600,
        "No price change": 3000,
    }

    for name, market_price in scenarios.items():
        amm = ConstantProductAMM()
        result = arbitrage_to_market(amm, market_price)

        print(f"\n--- {name} ---")
        for key, value in result.items():
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")
