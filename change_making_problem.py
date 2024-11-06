from colorama import init, Fore, Style

def change_making(coins, amount):
    init(autoreset=True)  # Initialize colorama

    # Initialize DP array
    max_value = float('inf')
    dp = [0] + [max_value] * amount
    coin_used = [0] * (amount + 1)
    calculations = [''] * (amount + 1)

    # Build the DP table
    for x in range(1, amount + 1):
        min_coins = max_value
        used_coin = 0
        calc_steps = []
        for coin in coins:
            if x >= coin:
                if dp[x - coin] + 1 < min_coins:
                    min_coins = dp[x - coin] + 1
                    used_coin = coin
                calc_steps.append(f"F[{x} - {coin}] = F[{x - coin}]")
        if min_coins < dp[x]:
            dp[x] = min_coins
            coin_used[x] = used_coin
            calculations[x] = f"F[{x}] = min{{" + ', '.join(calc_steps) + f"}} + 1 = {dp[x]}"
        else:
            calculations[x] = f"F[{x}] remains {dp[x]}"

    if dp[amount] == max_value:
        return dp, coin_used, calculations, None  # No solution
    else:
        return dp, coin_used, calculations, dp[amount]

def print_change_making_solution(coins, amount):
    init(autoreset=True)  # Initialize colorama

    dp, coin_used, calculations, min_coins = change_making(coins, amount)

    if min_coins is None:
        print(Fore.RED + f"No solution possible to make amount {amount} with given coins." + Style.RESET_ALL)
        return

    # Prepare data for the table
    table_data = []
    for i in range(amount + 1):
        # Alternate row colors
        if i % 2 == 0:
            row_color = Fore.LIGHTMAGENTA_EX
        else:
            row_color = Fore.CYAN
        coin_str = str(coin_used[i]) if coin_used[i] != 0 else '-'
        dp_str = str(dp[i]) if dp[i] != float('inf') else '∞'
        table_data.append([
            row_color + str(i) + Style.RESET_ALL,
            row_color + dp_str + Style.RESET_ALL,
            row_color + coin_str + Style.RESET_ALL,
            row_color + calculations[i] + Style.RESET_ALL,
        ])

    headers = [
        Fore.YELLOW + "Amount" + Style.RESET_ALL,
        Fore.YELLOW + "Min Coins" + Style.RESET_ALL,
        Fore.YELLOW + "Last Coin Used" + Style.RESET_ALL,
        Fore.YELLOW + "Calculation" + Style.RESET_ALL,
    ]

    print(Fore.YELLOW + "\nChange-Making Problem Solution:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Minimum Coins Needed for Amount {amount}: {min_coins}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nDP Table with Calculations:" + Style.RESET_ALL)

    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    if use_tabulate:
        print(tabulate(table_data, headers=headers, tablefmt="pretty", maxcolwidths=[None, None, None, 50]))
    else:
        # Simple print if tabulate is not installed
        # Print headers
        print("".join(f"{h:<20}" for h in headers))
        for row in table_data:
            print("".join(f"{cell:<20}" for cell in row))

    # Reconstruct the coins used
    print(Fore.BLUE + "\nCoins Used to Make the Amount:" + Style.RESET_ALL)
    coin_list = []
    k = amount
    while k > 0:
        coin = coin_used[k]
        coin_list.append(coin)
        k -= coin
    coin_list.reverse()
    print(Fore.MAGENTA + " + ".join(map(str, coin_list)) + f" = {amount}" + Style.RESET_ALL)
    print(Fore.GREEN + f"\nTotal Coins Used: {len(coin_list)}" + Style.RESET_ALL)

# Example usage:
if __name__ == "__main__":
    # Define your coin denominations and target amount here
    coins = [1, 3, 4]  # Coin denominations
    amount = 6         # Target amount

    print_change_making_solution(coins, amount)
