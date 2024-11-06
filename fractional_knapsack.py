from colorama import init, Fore, Style

def fractional_knapsack(weights, profits, capacity):
    init(autoreset=True)  # Initialize colorama

    n = len(weights)
    if n != len(profits):
        print(Fore.RED + "Error: The number of weights and profits must be the same.")
        return None
    # Calculate profit to weight ratio for each item
    items = []
    for i in range(n):
        ratio = profits[i] / weights[i]
        items.append({
            'index': i,
            'weight': weights[i],
            'profit': profits[i],
            'ratio': ratio,
            'fraction': 0.0  # Initialize fraction taken as 0
        })
    # Sort items by profit to weight ratio in descending order
    items.sort(key=lambda x: x['ratio'], reverse=True)

    total_profit = 0.0
    total_weight = 0.0

    for item in items:
        if total_weight + item['weight'] <= capacity:
            # Take the whole item
            item['fraction'] = 1.0
            total_weight += item['weight']
            total_profit += item['profit']
        else:
            # Take fraction of the item
            remain = capacity - total_weight
            fraction = remain / item['weight']
            item['fraction'] = fraction
            total_weight += item['weight'] * fraction
            total_profit += item['profit'] * fraction
            break  # Knapsack is full

    return total_profit, items

def print_fractional_knapsack_solution(weights, profits, capacity):
    init(autoreset=True)  # Initialize colorama

    result = fractional_knapsack(weights, profits, capacity)
    if result is None:
        return
    total_profit, items = result

    # Prepare data for the table
    table_data = []
    for idx, item in enumerate(items):
        # Alternate row colors
        if idx % 2 == 0:
            row_color = Fore.LIGHTMAGENTA_EX
        else:
            row_color = Fore.CYAN
        table_data.append([
            row_color + str(item['index'] + 1) + Style.RESET_ALL,
            row_color + f"{item['weight']:.2f}" + Style.RESET_ALL,
            row_color + f"{item['profit']:.2f}" + Style.RESET_ALL,
            row_color + f"{item['ratio']:.2f}" + Style.RESET_ALL,
            row_color + f"{item['fraction']:.2f}" + Style.RESET_ALL,
            row_color + f"{item['profit'] * item['fraction']:.2f}" + Style.RESET_ALL,
            row_color + f"{item['weight'] * item['fraction']:.2f}" + Style.RESET_ALL,
        ])

    headers = [
        Fore.YELLOW + "Item" + Style.RESET_ALL,
        Fore.YELLOW + "Weight" + Style.RESET_ALL,
        Fore.YELLOW + "Profit" + Style.RESET_ALL,
        Fore.YELLOW + "Profit/Weight" + Style.RESET_ALL,
        Fore.YELLOW + "Fraction Taken" + Style.RESET_ALL,
        Fore.YELLOW + "Profit Gained" + Style.RESET_ALL,
        Fore.YELLOW + "Weight Taken" + Style.RESET_ALL,
    ]

    print(Fore.YELLOW + "\nFractional Knapsack Solution:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Maximum Profit: {total_profit:.2f}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nCalculations:" + Style.RESET_ALL)

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

    total_weight_taken = sum(item['weight'] * item['fraction'] for item in items)
    print(Fore.CYAN + f"\nTotal Weight Taken: {total_weight_taken:.2f}" + Style.RESET_ALL)

    # Display the items that contribute to the maximum profit
    print(Fore.BLUE + "\nItems contributing to Maximum Profit:" + Style.RESET_ALL)
    print(f"{'Item':<10}{'Weight Taken':<15}{'Profit Gained':<15}{'Fraction Taken':<15}")
    for item in items:
        if item['fraction'] > 0:
            print(Fore.MAGENTA + f"{item['index'] + 1:<10}{(item['weight'] * item['fraction']):<15.2f}{(item['profit'] * item['fraction']):<15.2f}{item['fraction']:<15.2f}" + Style.RESET_ALL)

# Example usage:
if __name__ == "__main__":
    # Define your weights, profits, and capacity here
    weights = [10, 40, 20, 30]
    profits = [60, 40, 100, 120]
    capacity = 50

    print_fractional_knapsack_solution(weights, profits, capacity)
