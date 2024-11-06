import sys
from colorama import init, Fore, Style
import heapq
import matplotlib.pyplot as plt
import networkx as nx

def build_min_heap(elements):
    init(autoreset=True)  # Initialize colorama

    # Copy the elements to avoid modifying the original list
    heap = []
    steps = []

    print(Fore.YELLOW + "\nBuilding Min Heap:" + Style.RESET_ALL)
    for idx, element in enumerate(elements):
        heapq.heappush(heap, element)
        steps.append({
            'action': f"Inserted {element} into heap",
            'heap': heap.copy()
        })
        print_heap_state(heap, f"After inserting {element}")

    return heap, steps

def print_heap_state(heap, message):
    # Convert heap to tree representation
    print(Fore.BLUE + f"\n{message}:" + Style.RESET_ALL)
    levels = get_heap_levels(heap)
    for level in levels:
        print("   ".join(str(node) for node in level))

def get_heap_levels(heap):
    levels = []
    level = 0
    index = 0
    while index < len(heap):
        level_size = 2 ** level
        level_nodes = heap[index:index+level_size]
        levels.append(level_nodes)
        index += level_size
        level += 1
    return levels

def visualize_heap(heap):
    # Create a binary tree representation of the heap
    G = nx.Graph()
    labels = {}
    for idx, value in enumerate(heap):
        G.add_node(idx, label=value)
        labels[idx] = str(value)
        if idx != 0:
            parent_idx = (idx - 1) // 2
            G.add_edge(parent_idx, idx)

    pos = hierarchy_pos(G, 0)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, node_size=1000, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)
    plt.title('Min Heap Visualization')
    plt.axis('off')
    plt.show()

def hierarchy_pos(G, root, width=1.5, vert_gap=0.2, vert_loc=0, xcenter=0.5,
                  pos=None, parent=None):
    '''
    If there is a cycle, then this will see infinite recursion.
    '''

    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if parent is not None and parent in children:
        children.remove(parent)
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
    # Define your list of elements here
    elements = [9, 5, 6, 2, 3]

    heap, steps = build_min_heap(elements)

    print(Fore.GREEN + "\nFinal Min Heap:" + Style.RESET_ALL)
    print_heap_state(heap, "Heap Structure")

    visualize_heap(heap)
