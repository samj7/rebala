import sys

try: 
    import yfinance as yf
except ImportError:
    print("yfinance is not installed")
    sys.exit(1)

class stock:
    def __init__(self, ticker, quantity, pricePerShare):
        self.ticker = ticker
        self.quantity = quantity
        self.price = pricePerShare
        self.value = int(quantity)*int(pricePerShare)

    def __str__(self):
        return (f"{self.ticker}: {self.quantity} shares "
                f"@ ${self.price:.2f} per share. "
                f"Total = ${self.value:.2f}")
    
def get_positive_int(prompt):
    while True:
        val = input(prompt)
        try:
            val_int = int(val)
            if val_int <= 0:
                raise ValueError
            return val_int
        except ValueError:
            print("Error: enter a positive integer")

def get_non_negative_float (prompt):
    while True:
        val = input(prompt)
        try:
            val_float = float(val)
            if val_float < 0:
                raise ValueError
            return val_float
        except ValueError:
            print("Error: enter a non-negative number (float)")

def fetch_price_from_yahoo(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(period='1d')
        if data.empty:
            return None
        return float(data['Close'].iloc[-1])
    except Exception:
            return None

def main():
    stocks = []
    # Step 1 Cash amount
    cash = get_non_negative_float("Enter the amount of cash in portfolio (0 if none): ")
    
    # Step 2 Stock holdings
    while True:
        ticker = input("Enter ticker for stock, or x when finished entering stocks: ")
        if ticker.lower() == 'x':
            break

        quant = get_positive_int("Enter Quantity: ")
        
        price = fetch_price_from_yahoo(ticker)
        if price is None:
            print(f"Could not find or fetch price for '{ticker}'.")
            price = get_non_negative_float("Please enter the price (per share) manually: ")
        else:
            print(f"Fetched price for {ticker}: approximately ${price:.2f} per share.")
        stocks.append(stock(ticker,quant,price))


    # 3) Print portfolio summary
    print("\n--- Portfolio Summary ---")
    for s in stocks:
        print(s)

    # 4) Calculate total portfolio value
    total_stock_value = sum(s.value for s in stocks)
    total_portfolio_value = total_stock_value + cash

    print(f"\nCash in portfolio: ${cash:.2f}")
    print(f"Total portfolio value: ${total_portfolio_value:.2f}")

    # 5) Print each stock's percentage, plus cash
    if total_portfolio_value > 0:
        print("\n--- Current Portfolio Allocation ---")
        for s in stocks:
            percentage = (s.value / total_portfolio_value) * 100
            print(f"{s.ticker}: {percentage:.2f}%")
        cash_percentage = (cash / total_portfolio_value) * 100
        print(f"Cash: {cash_percentage:.2f}%\n")
    else:
        print("\nNo assets or cash in the portfolio.")
        return

    # 6) Ask if the user wishes to rebalance
    rebalance_choice = input("Do you want to rebalance? (y/n): ").lower()
    if rebalance_choice != 'y':
        print("No rebalance performed. Exiting.")
        return

    # 7) Prompt for desired allocations
    print("Please enter desired allocation percentages for each stock and cash.\n"
          "The total across all stocks + cash must sum to 100.\n")

    desired_allocations = {}
    sum_allocations = 0.0

    # For each stock, prompt for desired percentage
    for s in stocks:
        while True:
            val = input(f"Desired allocation for {s.ticker} (0-100): ")
            try:
                val_float = float(val)
                if val_float < 0 or val_float > 100:
                    raise ValueError
                desired_allocations[s.ticker] = val_float
                sum_allocations += val_float
                break
            except ValueError:
                print("Error: Please enter a valid percentage between 0 and 100.")

    #desired allocation for cash
    while True:
        val = input("Desired allocation for Cash (0-100): ")
        try:
            val_float = float(val)
            if val_float < 0 or val_float > 100:
                raise ValueError
            desired_allocations["Cash"] = val_float
            sum_allocations += val_float
            break
        except ValueError:
            print("Error: Please enter a valid percentage between 0 and 100.")

    # Check if sums to 100
    if abs(sum_allocations - 100.0) > 1e-6:
        print(f"\nError: The sum of allocations ({sum_allocations:.2f}%) must be 100%. Exiting.")
        return

    # 8) Calculate the new target dollar amounts for each stock/cash
    print("\n--- Rebalance Instructions ---")
    
    # Start with current cash in hand
    new_cash = cash

    for s in stocks:
        desired_pct = desired_allocations[s.ticker]
        desired_value = (desired_pct / 100.0) * total_portfolio_value
        
        current_value = s.value
        difference_value = desired_value - current_value

        if s.price > 0:
            new_shares = round(desired_value / s.price)
            current_shares = s.quantity
            shares_diff = new_shares - current_shares
            
            if shares_diff > 0:
                print(f"Buy {shares_diff} shares of {s.ticker}")
            elif shares_diff < 0:
                print(f"Sell {-shares_diff} shares of {s.ticker}")
            else:
                print(f"No change for {s.ticker}")

            money_spent_or_received = shares_diff * s.price
            new_cash -= money_spent_or_received
        else:
            # Edge case: if a stock has price 0 
            print(f"Skipping rebalancing for {s.ticker} due to zero price.")

    # handle the desired cash portion
    desired_cash = (desired_allocations["Cash"] / 100.0) * total_portfolio_value
    cash_diff = desired_cash - new_cash
    
    if abs(cash_diff) < 1e-6:
        print("No change to cash required.")
    elif cash_diff > 0:
        # We are short on cash; we need more
        print(f"You need an additional ${cash_diff:.2f} in cash.")
    else:
        # We have extra cash beyond the desired
        print(f"You will have an extra ${-cash_diff:.2f} in cash (above desired).")

    print("\nRebalance complete (instructions above).")


if __name__ == "__main__":
    main()
