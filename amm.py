class ConstantProductAMM:
    def __init__(self, eth_reserve=100.0,
                 usdc_reserve=300000.0, fee=0.003):
        self.eth = float(eth_reserve)
        self.usdc = float(usdc_reserve)
        self.fee = fee
        self.total_fees_usdc = 0.0
        self.total_fees_eth = 0.0

    @property
    def price(self):
        return self.usdc / self.eth

    @property
    def k(self):
        return self.eth * self.usdc

    def buy_eth(self, usdc_in):
        """Swap USDC for ETH."""
        effective_in = usdc_in * (1 - self.fee)
        eth_out = (
            self.eth * effective_in
            / (self.usdc + effective_in)
        )

        self.usdc += usdc_in
        self.eth -= eth_out
        self.total_fees_usdc += usdc_in * self.fee

        return eth_out

    def sell_eth(self, eth_in):
        """Swap ETH for USDC."""
        effective_in = eth_in * (1 - self.fee)
        usdc_out = (
            self.usdc * effective_in
            / (self.eth + effective_in)
        )

        self.eth += eth_in
        self.usdc -= usdc_out
        self.total_fees_eth += eth_in * self.fee

        return usdc_out


if __name__ == "__main__":
    amm = ConstantProductAMM()

    print("Initial price:", amm.price)
    print("Initial k:", amm.k)

    eth_received = amm.buy_eth(3000)

    print("\nETH received:", eth_received)
    print("New ETH reserve:", amm.eth)
    print("New USDC reserve:", amm.usdc)
    print("New price:", amm.price)
    print("New k:", amm.k)
    print("Total USDC fees:", amm.total_fees_usdc)
