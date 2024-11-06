from colorama import init, Fore, Style

def coin_row(coins):
    init(autoreset=True)  # Initialize colorama

    n = len(coins)
    if n == 0:
        return 0, [], []

    # Initialize DP arrays
    dp = [0] * n
    selected = [False] * n

    # Base cases
    dp[0] = coins[0]
    if n > 1:
        dp[1] = max(coins[0], coins[1])

    # Build the DP table
    for i in range(2, n):
        if dp[i - 1] > dp[i - 2] + coins[i]:
            dp[i] = dp[i - 1]
        else:
            dp[i] = dp[i - 2] + coins[i]

    # Reconstruct the solution
    i = n - 1
    selected_indices = []
    while i >= 0:
        if i == 0:
            selected_indices.append(0)
            break
        if i == 1:
            if dp[1] != dp[0]:
                selected_indices.append(1)
            else:
                selected_indices.append(0)
            break
        if dp[i - 1] >= dp[i - 2] + coins[i]:
            i -= 1
        else:
            selected_indices.append(i)
            i -= 2

    selected_indices.reverse()

    return dp, selected_indices, dp[-1]

def print_coin_row_solution(coins):
    init(autoreset=True)  # Initialize colorama

    dp, selected_indices, max_value = coin_row(coins)

    n = len(coins)
    # Prepare data for the table
    table_data = []
    for i in range(n):
        # Alternate row colors
        if i % 2 == 0:
            row_color = Fore.LIGHTMAGENTA_EX
        else:
            row_color = Fore.CYAN
        selected_str = 'Yes' if i in selected_indices else 'No'
        table_data.append([
            row_color + str(i + 1) + Style.RESET_ALL,
            row_color + f"{coins[i]}" + Style.RESET_ALL,
            row_color + f"{dp[i]}" + Style.RESET_ALL,
            row_color + selected_str + Style.RESET_ALL,
        ])

    headers = [
        Fore.YELLOW + "Position" + Style.RESET_ALL,
        Fore.YELLOW + "Coin Value" + Style.RESET_ALL,
        Fore.YELLOW + "Max Value" + Style.RESET_ALL,
        Fore.YELLOW + "Selected" + Style.RESET_ALL,
    ]

    print(Fore.YELLOW + "\nCoin Row Problem Solution:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Maximum Amount Collected: {max_value}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nDP Table and Coin Selection:" + Style.RESET_ALL)

    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    if use_tabulate:
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    else:
        # Simple print if tabulate is not installed
        # Print headers
        print("".join(f"{h:<15}" for h in headers))
        for row in table_data:
            print("".join(f"{cell:<15}" for cell in row))

    # Display the coins selected
    print(Fore.BLUE + "\nCoins Selected to Achieve Maximum Amount:" + Style.RESET_ALL)
    total_value = 0
    print(f"{'Position':<10}{'Coin Value':<15}")
    for idx in selected_indices:
        coin_value = coins[idx]
        total_value += coin_value
        print(Fore.MAGENTA + f"{idx + 1:<10}{coin_value:<15}" + Style.RESET_ALL)
    print(Fore.GREEN + f"\nTotal Value Collected: {total_value}" + Style.RESET_ALL)

# Example usage:
if __name__ == "__main__":
    # Define your list of coin values here
    coins = [5, 1, 2, 10, 6, 2]

    print_coin_row_solution(coins)
