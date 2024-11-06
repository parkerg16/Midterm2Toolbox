import matplotlib.pyplot as plt
from colorama import init, Fore, Style

def minimum_sum_descent(triangle):
    init(autoreset=True)  # Initialize colorama

    n = len(triangle)
    # Initialize DP table with the same dimensions as the triangle
    dp = [[0 for _ in range(len(row))] for row in triangle]

    # Base case: The last row of DP is the same as the last row of the triangle
    dp[-1] = triangle[-1][:]

    # Build the DP table from bottom to top
    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[i][j] = triangle[i][j] + min(dp[i + 1][j], dp[i + 1][j + 1])

    # Reconstruct the path
    path = [triangle[0][0]]
    index = 0
    path_indices = [0]
    for i in range(1, n):
        if dp[i][index] > dp[i][index + 1]:
            index += 1
        path.append(triangle[i][index])
        path_indices.append(index)

    return dp, dp[0][0], path, path_indices

def print_minimum_sum_descent_solution(triangle):
    init(autoreset=True)  # Initialize colorama

    dp, min_sum, path, path_indices = minimum_sum_descent(triangle)

    n = len(triangle)
    # Prepare data for the DP table
    table_data = []
    for i in range(n):
        row_data = []
        for j in range(len(triangle[i])):
            # Highlight the path taken
            if j == path_indices[i]:
                cell_color = Fore.GREEN
            else:
                # Alternate cell colors
                cell_color = Fore.LIGHTMAGENTA_EX if (i + j) % 2 == 0 else Fore.CYAN
            row_data.append(cell_color + str(dp[i][j]) + Style.RESET_ALL)
        table_data.append(row_data)

    print(Fore.YELLOW + "\nMinimum Sum Descent Problem Solution:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Minimum Path Sum: {min_sum}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nDynamic Programming Table (DP):" + Style.RESET_ALL)

    # Print the DP table
    for i in range(n):
        print(" " * (n - i - 1) * 4, end="")  # Adjust spacing
        print("   ".join(table_data[i]))

    # Display the path
    print(Fore.BLUE + "\nPath Taken to Achieve Minimum Sum:" + Style.RESET_ALL)
    path_str = " -> ".join(str(num) for num in path)
    print(Fore.MAGENTA + path_str + Style.RESET_ALL)

    # Verify the sum
    total = sum(path)
    print(Fore.GREEN + f"\nTotal Sum of Path: {total}" + Style.RESET_ALL)

    # Visualize the triangle and path using matplotlib
    visualize_triangle(triangle, path_indices)

def visualize_triangle(triangle, path_indices):
    n = len(triangle)
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.set_title('Minimum Sum Descent Visualization', fontsize=16)

    max_width = n * 2 - 1
    triangle_values = []

    for i in range(n):
        row = triangle[i]
        x_offsets = range(max_width // 2 - i, max_width // 2 + i + 1, 2)
        for j, x in enumerate(x_offsets):
            y = -i
            value = row[j]
            if j == path_indices[i]:
                # Highlight the path node
                circle = plt.Circle((x, y), 0.5, color='lightgreen')
            else:
                circle = plt.Circle((x, y), 0.5, color='lightblue')
            ax.add_artist(circle)
            ax.text(x, y, str(value), fontsize=12, ha='center', va='center')
            triangle_values.append((x, y, value))

    ax.set_xlim(-1, max_width)
    ax.set_ylim(-n - 1, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Define your triangle here
    triangle = [
        [2],
        [5, 4],
        [1, 4, 7],
        [8, 6, 9, 6]
    ]

    print_minimum_sum_descent_solution(triangle)
