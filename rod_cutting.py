from colorama import init, Fore, Style


def rod_cutting(prices, rod_length):
    init(autoreset=True)  # Initialize colorama

    n = rod_length
    # Initialize DP table
    dp = [0] * (n + 1)
    cuts = [0] * (n + 1)

    # Build the DP table in bottom-up manner
    for i in range(1, n + 1):
        max_val = float('-inf')
        for j in range(1, i + 1):
            if j - 1 < len(prices):
                if max_val < prices[j - 1] + dp[i - j]:
                    max_val = prices[j - 1] + dp[i - j]
                    cuts[i] = j
        dp[i] = max_val

    return dp, cuts


def print_rod_cutting_solution(prices, rod_length):
    init(autoreset=True)  # Initialize colorama

    dp, cuts = rod_cutting(prices, rod_length)

    # Prepare data for the table
    table_data = []
    for i in range(1, rod_length + 1):
        # Alternate row colors
        if i % 2 == 0:
            row_color = Fore.LIGHTMAGENTA_EX
        else:
            row_color = Fore.CYAN
        table_data.append([
            row_color + str(i) + Style.RESET_ALL,
            row_color + f"{dp[i]}" + Style.RESET_ALL,
            row_color + f"{cuts[i]}" + Style.RESET_ALL,
        ])

    headers = [
        Fore.YELLOW + "Rod Length" + Style.RESET_ALL,
        Fore.YELLOW + "Max Revenue" + Style.RESET_ALL,
        Fore.YELLOW + "First Cut" + Style.RESET_ALL,
    ]

    print(Fore.YELLOW + "\nRod Cutting Solution:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Maximum Revenue for Rod Length {rod_length}: {dp[rod_length]}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nDP Table and Cuts:" + Style.RESET_ALL)

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
        print("".join(f"{h:<20}" for h in headers))
        for row in table_data:
            print("".join(f"{cell:<20}" for cell in row))

    # Reconstruct the solution to find which cuts were made
    print(Fore.BLUE + "\nOptimal Cuts to Achieve Maximum Revenue:" + Style.RESET_ALL)
    n = rod_length
    cuts_made = []
    while n > 0:
        cuts_made.append(cuts[n])
        n -= cuts[n]
    print(Fore.MAGENTA + "Cuts Made: " + " + ".join(map(str, cuts_made)) + f" = {rod_length}" + Style.RESET_ALL)
    total_price = sum(prices[cut - 1] for cut in cuts_made)
    print(Fore.GREEN + f"Total Revenue: {total_price}" + Style.RESET_ALL)


# Example usage:
if __name__ == "__main__":
    # Define your prices and rod length here
    prices = [3, 5, 8, 9, 10, 17]  # Prices for lengths 1 to 8
    rod_length = 6

    print_rod_cutting_solution(prices, rod_length)
