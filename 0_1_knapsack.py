from colorama import init, Fore, Style


def knapsack(weights, profits, capacity):
    n = len(weights)
    # Initialize DP table
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build the DP table in bottom-up fashion
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(profits[i - 1] + dp[i - 1][w - weights[i - 1]],
                               dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Traceback to find the items to include
    res = dp[n][capacity]
    w = capacity
    items_selected = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res != dp[i - 1][w]:
            items_selected.append(i - 1)
            res -= profits[i - 1]
            w -= weights[i - 1]
    items_selected.reverse()

    return dp, dp[n][capacity], items_selected


def print_knapsack_solution(weights, profits, capacity):
    init(autoreset=True)  # Initialize colorama

    if len(weights) != len(profits):
        print(Fore.RED + "Error: The number of weights and profits must be the same.")
        return

    dp_table, max_profit, items = knapsack(weights, profits, capacity)

    # Output DP table
    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    n = len(weights)
    headers = [Fore.YELLOW + 'Item\\Capacity' + Style.RESET_ALL] + [Fore.YELLOW + str(i) + Style.RESET_ALL for i in
                                                                    range(capacity + 1)]
    table = []
    for i in range(n + 1):
        if i == 0:
            row_label = Fore.CYAN + "0" + Style.RESET_ALL
        else:
            row_label = Fore.CYAN + f"Item {i} (W={weights[i - 1]}, P={profits[i - 1]})" + Style.RESET_ALL
        row = [row_label]
        for w in range(capacity + 1):
            cell_value = dp_table[i][w]
            if i > 0 and w == capacity and cell_value == max_profit:
                # Highlight the cell that contains the maximum profit
                row.append(Fore.GREEN + str(cell_value) + Style.RESET_ALL)
            else:
                row.append(str(cell_value))
        table.append(row)

    print(Fore.YELLOW + "\nDynamic Programming Table:" + Style.RESET_ALL)
    if use_tabulate:
        print(tabulate(table, headers=headers, tablefmt="pretty"))
    else:
        # Fallback if tabulate is not installed
        header_row = "".join(f"{str(h):>5}" for h in headers)
        print(header_row)
        for row in table:
            print("".join(f"{str(item):>5}" for item in row))

    print(Fore.GREEN + f"\nMaximum Profit: {max_profit}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nItems selected:" + Style.RESET_ALL)
    total_weight = 0
    for i in items:
        print(Fore.MAGENTA + f"Item {i + 1}: Weight = {weights[i]}, Profit = {profits[i]}" + Style.RESET_ALL)
        total_weight += weights[i]
    print(Fore.CYAN + f"Total Weight: {total_weight}" + Style.RESET_ALL)


def print_excel_format(weights, profits, capacity):
    if len(weights) != len(profits):
        print("Error: The number of weights and profits must be the same.")
        return

    dp_table, max_profit, items = knapsack(weights, profits, capacity)
    n = len(weights)

    # Print headers with tab separation for Excel
    print("Capacity\t" + "\t".join(str(i) for i in range(capacity + 1)))

    # Print each row with item information and values
    for i in range(n + 1):
        if i == 0:
            row_label = "Initial"
        else:
            row_label = f"Item {i} (W={weights[i - 1]}, P={profits[i - 1]})"

        # Print row with tab separation
        row_values = "\t".join(str(dp_table[i][w]) for w in range(capacity + 1))
        print(f"{row_label}\t{row_values}")

    # Print summary information
    print("\nSolution Summary")
    print(f"Maximum Profit:\t{max_profit}")
    print("\nSelected Items:")
    total_weight = 0
    for i in items:
        print(f"Item {i + 1}\tWeight: {weights[i]}\tProfit: {profits[i]}")
        total_weight += weights[i]
    print(f"Total Weight:\t{total_weight}")


def print_colored_and_excel(weights, profits, capacity):
    # Print both colored console output and Excel-compatible format
    print("=" * 50)
    print("=== COLORED CONSOLE OUTPUT ===")
    print("=" * 50)
    print_knapsack_solution(weights, profits, capacity)

    print("\n" + "=" * 50)
    print("=== EXCEL-COMPATIBLE OUTPUT (Copy from here) ===")
    print("=" * 50)
    print_excel_format(weights, profits, capacity)
    print("=" * 50)


if __name__ == "__main__":
    # Define your weights, profits, and capacity here
    weights = [1, 2, 3, 5]
    profits = [1, 6, 10, 16]
    capacity = 7

    print_colored_and_excel(weights, profits, capacity)