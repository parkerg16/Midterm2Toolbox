import networkx as nx
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

def find_longest_path_dag(graph):
    init(autoreset=True)  # Initialize colorama

    # Initialize distances to all vertices as minus infinity and
    # predecessors for path reconstruction
    distances = {node: float('-inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}

    # Find a topological order of the nodes
    topo_order = list(nx.topological_sort(graph))

    # Set the distance to the starting node(s) as 0
    # For multiple sources, initialize them here
    distances[topo_order[0]] = 0

    # Detailed steps for output
    steps = []

    # Relax edges according to topological order
    for u in topo_order:
        for v in graph.successors(u):
            weight = graph[u][v]['weight']
            if distances[v] < distances[u] + weight:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                steps.append({
                    'from': u,
                    'to': v,
                    'weight': weight,
                    'action': f"Updated distance[{v}] to {distances[v]} via {u}"
                })
            else:
                steps.append({
                    'from': u,
                    'to': v,
                    'weight': weight,
                    'action': f"No update for distance[{v}]"
                })

    # Find the node with the maximum distance
    end_node = max(distances, key=distances.get)
    max_distance = distances[end_node]

    # Reconstruct the longest path
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()

    # Calculate the length of the path
    path_length = len(path)  # Number of nodes
    edge_count = path_length - 1  # Number of edges

    return distances, predecessors, steps, path, max_distance, path_length, edge_count

def print_longest_path_solution(graph):
    init(autoreset=True)  # Initialize colorama

    distances, predecessors, steps, path, max_distance, path_length, edge_count = find_longest_path_dag(graph)

    # Prepare data for the steps table
    table_data = []
    for idx, step in enumerate(steps):
        # Alternate row colors
        if idx % 2 == 0:
            row_color = Fore.LIGHTMAGENTA_EX
        else:
            row_color = Fore.CYAN
        table_data.append([
            row_color + str(idx + 1) + Style.RESET_ALL,
            row_color + str(step['from']) + Style.RESET_ALL,
            row_color + str(step['to']) + Style.RESET_ALL,
            row_color + str(step['weight']) + Style.RESET_ALL,
            row_color + step['action'] + Style.RESET_ALL,
        ])

    headers = [
        Fore.YELLOW + "Step" + Style.RESET_ALL,
        Fore.YELLOW + "From" + Style.RESET_ALL,
        Fore.YELLOW + "To" + Style.RESET_ALL,
        Fore.YELLOW + "Weight" + Style.RESET_ALL,
        Fore.YELLOW + "Action" + Style.RESET_ALL,
    ]

    print(Fore.YELLOW + "\nLongest Path in DAG:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Maximum Path Length (Total Weight): {max_distance}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Length of Path (Number of Nodes): {path_length}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Number of Edges in Path: {edge_count}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nDetailed Steps:" + Style.RESET_ALL)

    try:
        from tabulate import tabulate
        use_tabulate = True
    except ImportError:
        use_tabulate = False

    if use_tabulate:
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
    else:
        # Simple print if tabulate is not installed
        print("".join(f"{h:<10}" for h in headers))
        for row in table_data:
            print("".join(f"{cell:<10}" for cell in row))

    # Display distances
    print(Fore.BLUE + "\nFinal Distances to Nodes:" + Style.RESET_ALL)
    for node in distances:
        print(f"Distance to {node}: {distances[node]}")

    # Display the longest path
    print(Fore.BLUE + "\nLongest Path from Start to End Node:" + Style.RESET_ALL)
    path_str = " -> ".join(f"'{node}'" for node in path)
    print(Fore.MAGENTA + path_str + Style.RESET_ALL)

    # Visualize the graph and the longest path
    visualize_dag_and_longest_path(graph, path)

def visualize_dag_and_longest_path(graph, path):
    pos = nx.spring_layout(graph, seed=42)

    plt.figure(figsize=(12, 8))

    # Draw all nodes and edges
    nx.draw_networkx_nodes(graph, pos, node_color='lightblue')
    nx.draw_networkx_edges(graph, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_labels(graph, pos)

    # Highlight the longest path
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', arrows=True, width=2)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title('Longest Path in DAG')
    plt.axis('off')
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Create a DAG
    graph = nx.DiGraph()

    # Add edges: (from_node, to_node, weight)
    edges = [
        ('A', 'B', 3),
        ('A', 'C', 6),
        ('B', 'C', 4),
        ('B', 'D', 4),
        ('B', 'E', 11),
        ('C', 'D', 8),
        ('C', 'G', 11),
        ('D', 'E', -4),
        ('D', 'F', 5),
        ('D', 'G', 2),
        ('E', 'H', 9),
        ('F', 'H', 1),
        ('G', 'H', 2),
    ]

    # Add edges to the graph
    for u, v, w in edges:
        graph.add_edge(u, v, weight=w)

    print_longest_path_solution(graph)
