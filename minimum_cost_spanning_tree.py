import networkx as nx
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

def prim_mst(graph):
    init(autoreset=True)  # Initialize colorama

    # Start with an arbitrary node, here we choose the first node
    nodes = list(graph.nodes())
    mst_nodes = [nodes[0]]
    mst_edges = []
    total_cost = 0

    steps = []

    while set(mst_nodes) != set(nodes):
        crossing_edges = []
        for u in mst_nodes:
            for v in graph.neighbors(u):
                if v not in mst_nodes:
                    weight = graph[u][v]['weight']
                    crossing_edges.append((u, v, weight))
                    steps.append({
                        'from': u,
                        'to': v,
                        'weight': weight,
                        'action': 'Considered'
                    })

        # If there are no crossing edges left, break (graph might be disconnected)
        if not crossing_edges:
            break

        # Find the edge with the minimum weight
        edge = min(crossing_edges, key=lambda x: x[2])
        u, v, weight = edge

        # Add the edge to the MST
        mst_nodes.append(v)
        mst_edges.append((u, v, {'weight': weight}))
        total_cost += weight
        steps.append({
            'from': u,
            'to': v,
            'weight': weight,
            'action': 'Selected'
        })

    return mst_edges, total_cost, steps

def build_mst_paths(mst_edges, start_node):
    # Build a tree from MST edges
    tree = nx.Graph()
    tree.add_edges_from([(u, v) for u, v, _ in mst_edges])

    # Generate paths from the start node to all other nodes
    paths = {}
    for node in tree.nodes():
        if node != start_node:
            try:
                path = nx.shortest_path(tree, source=start_node, target=node)
                paths[node] = path
            except nx.NetworkXNoPath:
                # If there is no path (disconnected graph)
                paths[node] = None
    return paths

def print_mst_solution(graph):
    init(autoreset=True)  # Initialize colorama

    mst_edges, total_cost, steps = prim_mst(graph)

    # Prepare data for the steps table
    table_data = []
    for idx, step in enumerate(steps):
        # Alternate row colors
        if idx % 2 == 0:
            row_color = Fore.LIGHTMAGENTA_EX
        else:
            row_color = Fore.CYAN
        action_color = Fore.GREEN if step['action'] == 'Selected' else Fore.YELLOW
        table_data.append([
            row_color + str(idx + 1) + Style.RESET_ALL,
            row_color + str(step['from']) + Style.RESET_ALL,
            row_color + str(step['to']) + Style.RESET_ALL,
            row_color + str(step['weight']) + Style.RESET_ALL,
            action_color + step['action'] + Style.RESET_ALL,
        ])

    headers = [
        Fore.YELLOW + "Step" + Style.RESET_ALL,
        Fore.YELLOW + "From" + Style.RESET_ALL,
        Fore.YELLOW + "To" + Style.RESET_ALL,
        Fore.YELLOW + "Weight" + Style.RESET_ALL,
        Fore.YELLOW + "Action" + Style.RESET_ALL,
    ]

    print(Fore.YELLOW + "\nMinimum Cost Spanning Tree (Prim's Algorithm):" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total Cost of MST: {total_cost}" + Style.RESET_ALL)
    print(Fore.BLUE + "\nSteps and Decisions:" + Style.RESET_ALL)

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

    # Build and print MST paths
    start_node = list(graph.nodes())[0]
    paths = build_mst_paths(mst_edges, start_node)
    print(Fore.BLUE + "\nPaths in the Minimum Spanning Tree:" + Style.RESET_ALL)
    for target_node, path in paths.items():
        if path:
            path_str = " -> ".join(f"'{node}'" for node in path)
            print(Fore.MAGENTA + f"{path_str}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"No path from '{start_node}' to '{target_node}'" + Style.RESET_ALL)

    # Draw the original graph and the MST
    draw_graph_and_mst(graph, mst_edges)

def draw_graph_and_mst(graph, mst_edges):
    pos = nx.spring_layout(graph, seed=42)

    plt.figure(figsize=(14, 7))

    # Draw the original graph
    plt.subplot(121)
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title('Original Graph')

    # Draw the MST
    plt.subplot(122)
    mst = nx.Graph()
    mst.add_nodes_from(graph.nodes(data=True))
    mst.add_edges_from(mst_edges)
    nx.draw_networkx(mst, pos, with_labels=True, node_color='lightgreen', edge_color='red')
    labels = nx.get_edge_attributes(mst, 'weight')
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=labels)
    plt.title('Minimum Spanning Tree')

    plt.show()


# Example usage:
if __name__ == "__main__":
    # Create a graph
    graph = nx.Graph()

    # Add edges: (node1, node2, weight)
    edges = [
        ('1', '2', 5),
        ('2', '3', 3),
        ('3', '4', 6),
        ('4', '1', 4),
        ('2', '4', 2),
    ]

    # Add edges to the graph
    for u, v, w in edges:
        graph.add_edge(u, v, weight=w)

    print_mst_solution(graph)
