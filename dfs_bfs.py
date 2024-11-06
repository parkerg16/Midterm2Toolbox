import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

def traverse_graph(graph, start_node, use_bfs=True):
    """
    Traverses the graph using BFS or DFS based on the use_bfs parameter.

    :param graph: A dictionary representing the adjacency list of the graph.
    :param start_node: The node from which to start the traversal.
    :param use_bfs: Boolean value; if True, performs BFS; else performs DFS.
    :return: A list of nodes in the order they were visited.
    """
    visited = set()
    traversal_order = []
    traversal_edges = []

    if use_bfs:
        # Breadth-First Search
        queue = deque([start_node])
        print(f"Starting BFS from node '{start_node}'")
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                traversal_order.append(node)
                print(f"Visited: {node}")
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        traversal_edges.append((node, neighbor))
    else:
        # Depth-First Search
        stack = [start_node]
        print(f"Starting DFS from node '{start_node}'")
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                traversal_order.append(node)
                print(f"Visited: {node}")
                for neighbor in reversed(graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        traversal_edges.append((node, neighbor))

    return traversal_order, traversal_edges

def visualize_graph(graph, traversal_edges, traversal_order, use_bfs=True):
    """
    Visualizes the graph and highlights the traversal path.

    :param graph: A dictionary representing the adjacency list of the graph.
    :param traversal_edges: A list of edges in the traversal path.
    :param traversal_order: A list of nodes in the order they were visited.
    :param use_bfs: Boolean value; if True, BFS traversal; else DFS traversal.
    """
    G = nx.DiGraph()

    # Add nodes and edges to the graph
    for node in graph:
        G.add_node(node)
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)

    plt.figure(figsize=(12, 8))
    plt.title('Graph Traversal Visualization - ' + ('BFS' if use_bfs else 'DFS'))

    # Draw all nodes and edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, alpha=0.5)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    # Highlight traversal edges
    nx.draw_networkx_edges(
        G, pos,
        edgelist=traversal_edges,
        edge_color='red',
        arrows=True,
        width=2
    )

    # Annotate traversal order
    for idx, node in enumerate(traversal_order):
        x, y = pos[node]
        plt.text(
            x, y + 0.1, s=str(idx + 1),
            bbox=dict(facecolor='yellow', alpha=0.5),
            horizontalalignment='center',
            fontsize=10
        )

    plt.axis('off')
    plt.show()

# Example usage:
if __name__ == "__main__":
    # Define your graph as an adjacency list
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    start_node = 'A'

    # Perform BFS
    bfs_order, bfs_edges = traverse_graph(graph, start_node, use_bfs=True)
    print("\nBFS Traversal Order:", bfs_order)

    visualize_graph(graph, bfs_edges, bfs_order, use_bfs=True)

    print("\n" + "-"*50 + "\n")

    # Perform DFS
    dfs_order, dfs_edges = traverse_graph(graph, start_node, use_bfs=False)
    print("\nDFS Traversal Order:", dfs_order)

    visualize_graph(graph, dfs_edges, dfs_order, use_bfs=False)
