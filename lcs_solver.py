from colorama import init, Fore, Style


def lcs_with_all_solutions(X, Y):
    m, n = len(X), len(Y)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    def backtrack(i, j, current_lcs=""):
        if i == 0 or j == 0:
            return [current_lcs[::-1]]

        if X[i - 1] == Y[j - 1]:
            return backtrack(i - 1, j - 1, current_lcs + X[i - 1])

        solutions = []
        if dp[i - 1][j] == dp[i][j]:
            solutions.extend(backtrack(i - 1, j, current_lcs))
        if dp[i][j - 1] == dp[i][j]:
            solutions.extend(backtrack(i, j - 1, current_lcs))

        return list(dict.fromkeys(solutions))

    all_solutions = backtrack(m, n)
    return dp, all_solutions


def print_excel_format(X, Y, dp_table):
    print(Fore.YELLOW + "\nExcel-friendly format (tab-separated, copy everything below this line):" + Style.RESET_ALL)
    print("i/j\t" + "\t".join(str(i) for i in range(len(Y) + 1)))
    for i in range(len(X) + 1):
        row_values = [str(val) for val in dp_table[i]]
        if i == 0:
            print(f"{i}\t" + "\t".join(row_values))
        else:
            print(f"{i}({X[i - 1]})\t" + "\t".join(row_values))


def print_lcs_solution(X, Y):
    init(autoreset=True)

    print(Fore.YELLOW + f"\nSolving LCS for strings:" + Style.RESET_ALL)
    print(Fore.CYAN + f"X = \"{X}\"" + Style.RESET_ALL)
    print(Fore.CYAN + f"Y = \"{Y}\"" + Style.RESET_ALL)

    dp_table, solutions = lcs_with_all_solutions(X, Y)

    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    # Prepare table headers with numbers
    headers = [Fore.YELLOW + "i\\j" + Style.RESET_ALL]
    headers.extend([Fore.YELLOW + str(j) + Style.RESET_ALL for j in range(len(Y) + 1)])

    table = []
    # Add rows with index numbers and characters
    for i in range(len(X) + 1):
        if i == 0:
            row_label = Fore.CYAN + "0" + Style.RESET_ALL
        else:
            row_label = Fore.CYAN + f"{i}({X[i - 1]})" + Style.RESET_ALL
        row = [row_label]
        for val in dp_table[i]:
            row.append(str(val))
        table.append(row)

    # Print the DP table
    print(Fore.YELLOW + "\nDynamic Programming Table:" + Style.RESET_ALL)
    if use_tabulate:
        print(tabulate(table, headers=headers, tablefmt="pretty"))
    else:
        print(" ".join(f"{str(h):>6}" for h in headers))
        for row in table:
            print(" ".join(f"{str(cell):>6}" for cell in row))

    # Print Excel-friendly format
    print_excel_format(X, Y, dp_table)

    # Print solutions
    print(Fore.GREEN + f"\nLength of Longest Common Subsequence: {dp_table[-1][-1]}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nAll optimal solutions:" + Style.RESET_ALL)
    for idx, solution in enumerate(solutions, 1):
        print(Fore.MAGENTA + f"Solution {idx}: {solution}" + Style.RESET_ALL)

    # Print explanation of how to read the table
    print(Fore.YELLOW + "\nHow to read the table:" + Style.RESET_ALL)
    print("1. Numbers in brackets show the corresponding character from the strings")
    print("2. Each cell [i,j] contains the length of the LCS up to position i in X and position j in Y")
    print("3. When characters match (diagonal), add 1 to the value from top-left diagonal")
    print("4. When characters don't match, take maximum from left or top cell")


# Example usage with your specific case
if __name__ == "__main__":
    X = "bdcaba"
    Y = "abcbdab"
    print_lcs_solution(X, Y)