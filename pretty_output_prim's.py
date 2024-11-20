import networkx as nx
import matplotlib.pyplot as plt
from heapq import heappop, heappush
from collections import defaultdict
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# DisjointSet class for Kruskal's algorithm
class DisjointSet:
    def __init__(self, vertices):
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, item):
        # Path compression
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        # Union by rank
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                root_x, root_y = root_y, root_x
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1


def kruskals_algorithm(edges, positions):
    # Create the graph
    graph = nx.Graph()
    for u, v, weight in edges:
        graph.add_edge(u, v, weight=weight)

    # Get all vertices
    vertices = list(graph.nodes())

    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: (x[2], -ord(x[0][0]), -ord(x[1][0])))

    # Initialize disjoint set
    ds = DisjointSet(vertices)

    mst_edges = []

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Kruskal's Algorithm Steps:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Sorted edges: {sorted_edges}{Style.RESET_ALL}")

    # Process each edge in order of increasing weight
    for u, v, weight in sorted_edges:
        if ds.find(u) != ds.find(v):  # If including this edge doesn't create a cycle
            ds.union(u, v)
            mst_edges.append((u, v, weight))
            print(f"\n{Fore.GREEN}Adding edge: {u} -- {v} with weight: {weight}{Style.RESET_ALL}")
            current_mst = ', '.join(f'({x}, {y}, {z})' for x, y, z in mst_edges)
            print(f"{Fore.MAGENTA}Current MST edges: {current_mst}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Final Minimum Spanning Tree edges (Kruskal's):{Style.RESET_ALL}")
    total_weight = 0
    for u, v, weight in mst_edges:
        print(f"{Fore.BLUE}Edge: {u} -- {v}, Weight: {weight}{Style.RESET_ALL}")
        total_weight += weight
    print(f"{Fore.GREEN}Total MST Weight: {total_weight}{Style.RESET_ALL}")

    # Visualization
    plt.figure(figsize=(12, 8))

    # Draw original graph
    nx.draw(graph, positions, with_labels=True,
            node_color='lightblue',
            edge_color='gray',
            node_size=500,
            font_size=10,
            width=1)

    # Draw edge labels for original graph
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels)

    # Create and draw the MST
    mst_graph = nx.Graph()
    mst_graph.add_weighted_edges_from(mst_edges)

    # Draw the MST with red edges
    nx.draw(mst_graph, positions,
            node_color='lightgreen',
            edge_color='red',
            node_size=500,
            width=2)

    # Draw edge labels for MST
    mst_labels = {(u, v): weight for u, v, weight in mst_edges}
    nx.draw_networkx_edge_labels(mst_graph, positions,
                                 edge_labels=mst_labels,
                                 font_color='red')

    plt.title("Minimum Spanning Tree Using Kruskal's Algorithm")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return mst_edges


def prims_algorithm(edges, start_node, positions):
    # Create the graph
    graph = nx.Graph()
    for u, v, weight in edges:
        graph.add_edge(u, v, weight=weight)

    mst_edges = []
    visited = set([start_node])
    priority_queue = []

    # Initialize priority queue with edges from start node
    for neighbor, data in graph[start_node].items():
        heappush(priority_queue, (data['weight'], start_node, neighbor))

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Starting Prim's Algorithm from node: {start_node}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Initial Priority Queue:")
    print(f"{priority_queue}")

    while priority_queue:
        weight, u, v = heappop(priority_queue)

        if v in visited:
            print(f"\n{Fore.RED}Skipping edge {(u, v, weight)} as node {v} is already visited{Style.RESET_ALL}")
            continue

        visited.add(v)
        mst_edges.append((u, v, weight))

        print(f"\n{Fore.GREEN}Adding edge: {(u, v, weight)}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Visited nodes: {visited}{Style.RESET_ALL}")

        for neighbor, data in graph[v].items():
            if neighbor not in visited:
                heappush(priority_queue, (data['weight'], v, neighbor))
                print(f"{Fore.BLUE}Adding to priority queue: ({data['weight']}, {v}, {neighbor}){Style.RESET_ALL}")

        print(f"{Fore.YELLOW}Current Priority Queue:")
        print(f"{priority_queue}")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Final Minimum Spanning Tree edges (Prim's):{Style.RESET_ALL}")
    total_weight = 0
    for u, v, weight in mst_edges:
        print(f"{Fore.BLUE}Edge: {u} -- {v}, Weight: {weight}{Style.RESET_ALL}")
        total_weight += weight
    print(f"{Fore.GREEN}Total MST Weight: {total_weight}{Style.RESET_ALL}")

    # Visualization
    plt.figure(figsize=(12, 8))
    pos = positions

    nx.draw(graph, pos, with_labels=True,
            node_color='lightblue',
            edge_color='gray',
            node_size=500,
            font_size=10,
            width=1)

    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    mst_graph = nx.Graph()
    mst_graph.add_weighted_edges_from(mst_edges)

    nx.draw(mst_graph, pos,
            node_color='lightgreen',
            edge_color='red',
            node_size=500,
            width=2)

    mst_labels = {(u, v): weight for u, v, weight in mst_edges}
    nx.draw_networkx_edge_labels(mst_graph, pos,
                                 edge_labels=mst_labels,
                                 font_color='red')

    plt.title("Minimum Spanning Tree Using Prim's Algorithm")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return mst_edges


def dijkstras_algorithm(edges, start_node, positions):
    # Create the graph
    graph = nx.Graph()
    for u, v, weight in edges:
        graph.add_edge(u, v, weight=weight)

    # Initialize distances and priority queue
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    shortest_path_tree_edges = []

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Dijkstra's Algorithm Steps from start node '{start_node}':{Style.RESET_ALL}")

    while priority_queue:
        current_distance, current_node = heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, data in graph[current_node].items():
            distance = current_distance + data['weight']
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(priority_queue, (distance, neighbor))
                shortest_path_tree_edges.append((current_node, neighbor, data['weight']))
                print(f"{Fore.BLUE}Updated distance for {neighbor}: {distance}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}Final Shortest Path Distances from start node:{Style.RESET_ALL}")
    for node, distance in distances.items():
        print(f"{Fore.GREEN}Node: {node}, Distance: {distance}{Style.RESET_ALL}")

    # Visualization
    plt.figure(figsize=(12, 8))
    nx.draw(graph, positions, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels)

    shortest_path_graph = nx.Graph()
    shortest_path_graph.add_weighted_edges_from(shortest_path_tree_edges)
    nx.draw(shortest_path_graph, positions, node_color='lightgreen', edge_color='purple', node_size=500, width=2)

    sp_labels = {(u, v): weight for u, v, weight in shortest_path_tree_edges}
    nx.draw_networkx_edge_labels(shortest_path_graph, positions, edge_labels=sp_labels, font_color='purple')

    plt.title(f"Single Source Shortest Path from '{start_node}' using Dijkstra's Algorithm")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return distances


# Example graphs
edges = [
    ('a', 'b', 5), ('a', 'c', 7), ('a', 'e', 2),
    ('b', 'e', 3), ('b', 'd', 6), ('c', 'e', 4),
    ('c', 'd', 4), ('d', 'e', 5)
]

edges_b = [
    ('a', 'b', 3), ('a', 'd', 4), ('a', 'c', 5),
    ('b', 'e', 3), ('b', 'f', 6),
    ('c', 'd', 2), ('c', 'g', 4),
    ('d', 'e', 1), ('d', 'h', 5),
    ('e', 'f', 2), ('e', 'i', 4),
    ('f', 'j', 5),
    ('g', 'h', 3), ('g', 'k', 6),
    ('h', 'i', 6), ('h', 'k', 7),
    ('i', 'j', 3), ('i', 'l', 5),
    ('j', 'l', 9), ('k', 'l', 8)
]
edges_c = [
    ('a', 'b', 3),
    ('a', 'd', 7),
    ('b', 'c', 4),
    ('b', 'd', 2),
    ('c', 'e', 6),
    ('d', 'e', 4),
    ('d', 'c', 5)
]

# Node positions for visualization
positions = {
    'a': (0, 1), 'b': (2, 1), 'c': (0, 0),
    'd': (2, 0), 'e': (1, 0.5)
}

positions_b = {
    'a': (1, 3), 'b': (3, 3), 'c': (0, 2),
    'd': (1, 2), 'e': (3, 2), 'f': (4, 2),
    'g': (0, 1), 'h': (1, 1), 'i': (3, 1),
    'j': (4, 1), 'k': (1, 0), 'l': (3, 0)
}

positions_c = {
    'a': (0, 0),    # bottom left
    'b': (1, 2),    # top left
    'c': (2, 2),    # top middle
    'd': (1.5, 0),  # bottom middle
    'e': (3, 0)     # bottom right
}

# Run both algorithms on both graphs
print(f"{Fore.GREEN}{Style.BRIGHT}Running Prim's Algorithm on first graph:{Style.RESET_ALL}")
mst_prim_a = prims_algorithm(edges, 'a', positions)

print(f"\n{Fore.GREEN}{Style.BRIGHT}Running Kruskal's Algorithm on first graph:{Style.RESET_ALL}")
mst_kruskal_a = kruskals_algorithm(edges, positions)

print(f"\n{Fore.GREEN}{Style.BRIGHT}Running Prim's Algorithm on second graph:{Style.RESET_ALL}")
mst_prim_b = prims_algorithm(edges_b, 'a', positions_b)

print(f"\n{Fore.GREEN}{Style.BRIGHT}Running Kruskal's Algorithm on second graph:{Style.RESET_ALL}")
mst_kruskal_b = kruskals_algorithm(edges_b, positions_b)

# Function calls with print statements
print("\n" + "="*50)
print(f"{Fore.CYAN}{Style.BRIGHT}Running Prim's Algorithm on graph C:{Style.RESET_ALL}")
print("="*50)
mst_prim_c = prims_algorithm(edges_c, 'a', positions_c)

print("\n" + "="*50)
print(f"{Fore.CYAN}{Style.BRIGHT}Running Kruskal's Algorithm on graph C:{Style.RESET_ALL}")
print("="*50)
mst_kruskal_c = kruskals_algorithm(edges_c, positions_c)

# Compare results
print("\n" + "="*50)
print(f"{Fore.MAGENTA}{Style.BRIGHT}Comparing Results for Graph C:{Style.RESET_ALL}")
print("="*50)
print(f"{Fore.BLUE}Prim's MST edges: {mst_prim_c}{Style.RESET_ALL}")
print(f"{Fore.BLUE}Kruskal's MST edges: {mst_kruskal_c}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}{Style.BRIGHT}Running Dijkstra's Algorithm on first graph:{Style.RESET_ALL}")
sssp_a = dijkstras_algorithm(edges, 'a', positions)

print(f"\n{Fore.GREEN}{Style.BRIGHT}Running Dijkstra's Algorithm on second graph:{Style.RESET_ALL}")
sssp_b = dijkstras_algorithm(edges_b, 'a', positions_b)

print(f"\n{Fore.GREEN}{Style.BRIGHT}Running Dijkstra's Algorithm on third graph:{Style.RESET_ALL}")
sssp_c = dijkstras_algorithm(edges_c, 'a', positions_c)
