import sys
import numpy as np
from colorama import init, Fore, Style

def optimal_bst(keys, freq):
    init(autoreset=True)  # Initialize colorama

    n = len(keys)
    # Initialize the cost and root tables
    cost = [[0 for _ in range(n+2)] for _ in range(n+2)]
    root = [[0 for _ in range(n+2)] for _ in range(n+2)]
    weight = [[0 for _ in range(n+2)] for _ in range(n+2)]
    # Store calculations
    calculations = [[[] for _ in range(n+2)] for _ in range(n+2)]

    # Build weight matrix
    for i in range(1, n+2):
        weight[i][i-1] = 0
        cost[i][i-1] = 0

    for i in range(1, n+1):
        weight[i][i] = weight[i][i-1] + freq[i-1]
        cost[i][i] = freq[i-1]
        root[i][i] = i
        calculations[i][i].append(f"C({i},{i})=freq[{i}]={freq[i-1]}")

    for l in range(2, n+1):  # l is the chain length
        for i in range(1, n - l + 2):  # i is the start index
            j = i + l - 1  # j is the end index
            weight[i][j] = weight[i][j-1] + freq[j-1]
            cost[i][j] = sys.maxsize
            calc_strings = []
            for r in range(i, j+1):
                c = cost[i][r-1] + cost[r+1][j] + weight[i][j]
                calc_str = f"k={r}, C({i},{j})=C({i},{r-1})+C({r+1},{j})+W[{i},{j}]={cost[i][r-1]}+{cost[r+1][j]}+{weight[i][j]}={c}"
                calc_strings.append((c, calc_str, r))
                if c < cost[i][j]:
                    cost[i][j] = c
                    root[i][j] = r
            # Store all calculations for this cell
            min_c = cost[i][j]
            min_r = root[i][j]
            calculations[i][j] = []
            for c_value, c_str, r_value in calc_strings:
                if c_value == min_c and r_value == min_r:
                    c_str = Fore.GREEN + c_str + " <- min" + Style.RESET_ALL
                calculations[i][j].append(c_str)

    return cost, root, calculations

def construct_optimal_bst(root, keys, i, j, parent=None, is_left=False, tree_edges=None):
    if tree_edges is None:
        tree_edges = []

    if i > j:
        return None

    r = root[i][j]
    key = keys[r-1]
    if parent is not None:
        tree_edges.append({
            'parent': parent,
            'child': key,
            'direction': 'left' if is_left else 'right'
        })
    else:
        tree_edges.append({
            'parent': None,
            'child': key,
            'direction': 'root'
        })
    # Left subtree
    construct_optimal_bst(root, keys, i, r-1, key, True, tree_edges)
    # Right subtree
    construct_optimal_bst(root, keys, r+1, j, key, False, tree_edges)

    return tree_edges

def print_obst_solution(keys, freq):
    init(autoreset=True)  # Initialize colorama

    n = len(keys)
    cost, root, calculations = optimal_bst(keys, freq)

    # Prepare data for the cost and root tables with calculations
    print(Fore.YELLOW + "\nOptimal Binary Search Tree (OBST) Solution:" + Style.RESET_ALL)
    print(Fore.BLUE + "\nCalculations for Cost Table:" + Style.RESET_ALL)

    for i in range(1, n+1):
        for j in range(i, n+1):
            print(Fore.CYAN + f"\nCalculations for C({i},{j}):" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX + f"Weight[{i},{j}] = Sum of frequencies from {i} to {j} = {sum(freq[i-1:j])}" + Style.RESET_ALL)
            for calc in calculations[i][j]:
                print(calc)
            print(Fore.GREEN + f"Minimum Cost C({i},{j}) = {cost[i][j]} with root at key {keys[root[i][j]-1]}" + Style.RESET_ALL)

    # Display the cost and root tables
    display_tables(cost, root, n)

    # Construct the optimal BST
    tree_edges = construct_optimal_bst(root, keys, 1, n)

    print(Fore.BLUE + "\nOptimal Binary Search Tree Structure:" + Style.RESET_ALL)
    for edge in tree_edges:
        if edge['parent'] is None:
            print(Fore.GREEN + f"Root: {edge['child']}" + Style.RESET_ALL)
        else:
            direction = 'Left' if edge['direction'] == 'left' else 'Right'
            print(Fore.GREEN + f"{direction} child of {edge['parent']}: {edge['child']}" + Style.RESET_ALL)

    # Visualize the tree
    visualize_obst(tree_edges)

def display_tables(cost, root, n):
    # Prepare data for the cost and root tables
    cost_table_data = []
    root_table_data = []

    for i in range(1, n+2):
        cost_row = []
        root_row = []
        for j in range(n+1):
            if i <= n and i <= j:
                c_value = cost[i][j] if cost[i][j] != sys.maxsize else '∞'
                r_value = root[i][j] if root[i][j] != 0 else '-'
            else:
                c_value = '-'
                r_value = '-'
            cost_row.append(str(c_value))
            root_row.append(str(r_value))
        if i <= n:
            cost_table_data.append(cost_row)
            root_table_data.append(root_row)

    headers = ['i/j'] + [str(j) for j in range(n+1)]
    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    print(Fore.BLUE + "\nCost Table:" + Style.RESET_ALL)
    if use_tabulate:
        cost_table = [[str(i)] + row for i, row in zip(range(1, n+1), cost_table_data)]
        print(tabulate(cost_table, headers=headers, tablefmt="pretty"))
    else:
        print("Tabulate module not found. Please install it for a better table format.")
        # Simple print
        print("".join(f"{h:<8}" for h in headers))
        for i, row in enumerate(cost_table_data, start=1):
            print(f"{i:<8}" + "".join(f"{cell:<8}" for cell in row))

    print(Fore.BLUE + "\nRoot Table:" + Style.RESET_ALL)
    if use_tabulate:
        root_table = [[str(i)] + row for i, row in zip(range(1, n+1), root_table_data)]
        print(tabulate(root_table, headers=headers, tablefmt="pretty"))
    else:
        print("".join(f"{h:<8}" for h in headers))
        for i, row in enumerate(root_table_data, start=1):
            print(f"{i:<8}" + "".join(f"{cell:<8}" for cell in row))

def visualize_obst(tree_edges):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    labels = {}
    for edge in tree_edges:
        child = edge['child']
        parent = edge['parent']
        if parent is not None:
            G.add_edge(parent, child)
        else:
            G.add_node(child)
        labels[child] = str(child)
        if parent is not None:
            labels[parent] = str(parent)

    pos = hierarchy_pos(G, tree_edges[0]['child'])
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, arrows=True, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, labels=labels)
    plt.title('Optimal Binary Search Tree')
    plt.axis('off')
    plt.show()

def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5,
                  pos=None, parent=None):
    '''
    If there is a cycle, then this will see infinite recursion.
    '''

    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.successors(root))
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                pos=pos, parent=root)
    return pos

# Example usage:
if __name__ == "__main__":
    # Define your keys and frequencies here
    keys = ['A', 'B', 'C', 'D']
    freq = [0.1, 0.2, 0.4, 0.3]

    print_obst_solution(keys, freq)
