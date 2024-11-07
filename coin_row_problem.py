from colorama import init, Fore, Style


def coin_row_all_solutions_trace(coins):
    init(autoreset=True)  # Initialize colorama

    n = len(coins)
    if n == 0:
        return [], [], 0

    # Initialize DP array of tuples: (max_value, list of selections)
    dp = [(0, []) for _ in range(n)]
    dp_values = []  # For storing max values at each step

    # Base cases
    dp[0] = (coins[0], [[0]])
    dp_values.append(dp[0][0])
    print(f"F[1] = {coins[0]}, Selections: {[1]}")

    if n > 1:
        if coins[0] > coins[1]:
            dp[1] = (coins[0], [[0]])
            dp_values.append(dp[1][0])
            print(f"F[2] = max{{{coins[1]} + 0, {coins[0]}}} = {dp[1][0]}, Selections: {[1]}")
        elif coins[0] < coins[1]:
            dp[1] = (coins[1], [[1]])
            dp_values.append(dp[1][0])
            print(f"F[2] = max{{{coins[1]} + 0, {coins[0]}}} = {dp[1][0]}, Selections: {[2]}")
        else:  # coins[0] == coins[1]
            dp[1] = (coins[0], [[0], [1]])
            dp_values.append(dp[1][0])
            print(f"F[2] = max{{{coins[1]} + 0, {coins[0]}}} = {dp[1][0]}, Selections: {[1], [2]}")

    # Build the DP table with trace
    for i in range(2, n):
        sum1 = dp[i - 1][0]
        sum2 = dp[i - 2][0] + coins[i]

        # Print the calculation step
        print(
            f"F[{i + 1}] = max{{{coins[i]} + F[{i - 1}], F[{i}]}} = max{{{coins[i]} + {dp[i - 2][0]}, {dp[i - 1][0]}}}",
            end='')

        if sum1 > sum2:
            dp[i] = (sum1, dp[i - 1][1])
            print(f" = {sum1}, Selections: {[[idx + 1 for idx in sel] for sel in dp[i][1]]}")
        elif sum1 < sum2:
            selections = [sel + [i] for sel in dp[i - 2][1]]
            dp[i] = (sum2, selections)
            print(f" = {sum2}, Selections: {[[idx + 1 for idx in sel] for sel in dp[i][1]]}")
        else:  # sum1 == sum2
            selections = dp[i - 1][1] + [sel + [i] for sel in dp[i - 2][1]]
            dp[i] = (sum1, selections)
            print(f" = {sum1}, Selections: {[[idx + 1 for idx in sel] for sel in dp[i][1]]}")
        dp_values.append(dp[i][0])  # Append the max value at position i

        # After each step, print the DP table evolution
        print("\nCurrent DP table:")
        print_dp_table(i, coins, dp_values)

    # The maximum amount is dp[n - 1][0]
    max_value = dp[n - 1][0]
    # All optimal selections are dp[n - 1][1]
    optimal_selections = dp[n - 1][1]

    return dp, optimal_selections, max_value


def print_dp_table(i, coins, dp_values):
    # i: current position (0-based index)
    # coins: list of coin values
    # dp_values: list of DP max values up to current position

    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    positions = [str(idx + 1) for idx in range(i + 1)]
    coin_values = [str(coins[idx]) for idx in range(i + 1)]
    max_values = [str(dp_values[idx]) for idx in range(i + 1)]

    table_data = [
        [Fore.YELLOW + "Index" + Style.RESET_ALL] + positions,
        [Fore.YELLOW + "Coin (c)" + Style.RESET_ALL] + coin_values,
        [Fore.YELLOW + "F[i]" + Style.RESET_ALL] + max_values,
    ]

    if use_tabulate:
        # Transpose the table data for tabulate
        table_data_transposed = list(map(list, zip(*table_data)))
        print(tabulate(table_data_transposed, tablefmt="pretty"))
    else:
        # Simple print if tabulate is not installed
        for row in table_data:
            print("  ".join(row))
    print()


def print_coin_row_solution_trace(coins):
    init(autoreset=True)  # Initialize colorama

    print(Fore.YELLOW + "\nTracing the Dynamic Programming Algorithm for the Coin-Row Problem:\n" + Style.RESET_ALL)
    dp, optimal_selections, max_value = coin_row_all_solutions_trace(coins)
    n = len(coins)

    # Final DP table
    positions = [str(idx + 1) for idx in range(n)]
    coin_values = [str(coins[idx]) for idx in range(n)]
    max_values = [str(dp[idx][0]) for idx in range(n)]

    print(Fore.BLUE + "Final DP Table:" + Style.RESET_ALL)
    table_data = [
        [Fore.YELLOW + "Index" + Style.RESET_ALL] + positions,
        [Fore.YELLOW + "Coin (c)" + Style.RESET_ALL] + coin_values,
        [Fore.YELLOW + "F[i]" + Style.RESET_ALL] + max_values,
    ]

    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    if use_tabulate:
        # Transpose the table data for tabulate
        table_data_transposed = list(map(list, zip(*table_data)))
        print(tabulate(table_data_transposed, tablefmt="pretty"))
    else:
        # Simple print if tabulate is not installed
        for row in table_data:
            print("  ".join(row))
    print()

    # Display all optimal selections
    print(Fore.GREEN + f"Maximum Amount Collected: {max_value}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nAll Optimal Coin Selections to Achieve Maximum Amount:" + Style.RESET_ALL)
    for idx, selection in enumerate(optimal_selections, 1):
        selection_positions = [idx + 1 for idx in selection]
        coin_values_sel = [coins[idx] for idx in selection]
        selection_str = ', '.join(
            f"Position {pos} (Value {val})" for pos, val in zip(selection_positions, coin_values_sel))
        print(Fore.MAGENTA + f"Selection {idx}: {selection_str}" + Style.RESET_ALL)


# Example usage:
if __name__ == "__main__":
    # Define your list of coin values here
    coins = [7, 9, 10, 9, 3, 5, 2]

    print_coin_row_solution_trace(coins)
