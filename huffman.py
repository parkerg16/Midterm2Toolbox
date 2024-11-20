from heapq import heappush, heappop, heapify
from collections import defaultdict
from graphviz import Digraph
import os
import itertools  # To generate unique sequence numbers

class HuffmanNode:
    _ids = itertools.count()  # Class-level counter for unique IDs

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        self.id = next(HuffmanNode._ids)  # Assign a unique ID to each node

    def __lt__(self, other):
        if self.freq == other.freq:
            return self.id < other.id  # Use unique ID to break ties
        return self.freq < other.freq

class HuffmanCodec:
    def __init__(self, symbols, frequencies):
        self.symbols = symbols
        self.frequencies = frequencies
        self.codes = {}
        self.reverse_codes = {}
        self.step = 0  # Initialize step counter
        self.root = None  # Initialize root
        self._build_tree()
        self._generate_codes()

    def _build_tree(self):
        heap = []
        for char, freq in zip(self.symbols, self.frequencies):
            heappush(heap, HuffmanNode(char, freq))
            print(f"Initial heap push: {char} with frequency {freq}")

        # Ensure the heap is properly ordered
        heapify(heap)
        self.visualize_heap(heap, "initial_heap")

        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            internal = HuffmanNode(None, left.freq + right.freq)
            internal.left = left
            internal.right = right
            heappush(heap, internal)
            self.step += 1
            print(f"Step {self.step}: Combined nodes with frequencies {left.freq} and {right.freq} into {internal.freq}")
            # Visualize the current internal node as a partial tree
            self.visualize_tree(filename=f"huffman_tree_step_{self.step}", node=internal)
            self.visualize_heap(heap, f"heap_after_step_{self.step}")

        self.root = heap[0]  # Assign the final tree root

    def _generate_codes(self, node=None, code=""):
        if node is None:
            node = self.root

        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_codes[code] = node.char
            return

        self._generate_codes(node.left, code + "0")
        self._generate_codes(node.right, code + "1")

    def encode(self, text):
        encoded = ""
        for char in text:
            if char not in self.codes:
                raise ValueError(f"Character '{char}' not in symbol set")
            encoded += self.codes[char]
        return encoded

    def decode(self, encoded_text):
        decoded = ""
        current_code = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded += self.reverse_codes[current_code]
                current_code = ""

        if current_code:
            raise ValueError("Invalid encoded sequence")

        return decoded

    def print_codes(self):
        print("\nHuffman Codes:")
        for symbol in sorted(self.codes):
            print(f"{symbol}: {self.codes[symbol]}")

    def visualize_tree(self, filename="huffman_tree", *, node=None):
        """
        Creates a visual representation of the Huffman tree using graphviz.
        If a node is provided, visualizes the subtree rooted at that node.
        Otherwise, visualizes the entire tree.
        """
        dot = Digraph(comment='Huffman Tree')
        dot.attr(rankdir='TB')

        def add_nodes_edges(current_node, node_id=None):
            if current_node is None:
                return

            if node_id is None:
                node_id = str(id(current_node))

            # Create node label
            if current_node.char is not None:
                label = f'{current_node.char}\n{current_node.freq:.2f}'
                dot.node(node_id, label, shape='box', style='filled', color='lightblue')
            else:
                label = f'{current_node.freq:.2f}'
                dot.node(node_id, label, shape='circle', style='filled', color='lightgreen')

            # Add edges to children
            if current_node.left:
                left_id = str(id(current_node.left))
                dot.edge(node_id, left_id, '0')
                add_nodes_edges(current_node.left, left_id)

            if current_node.right:
                right_id = str(id(current_node.right))
                dot.edge(node_id, right_id, '1')
                add_nodes_edges(current_node.right, right_id)

        # Decide which node to visualize
        root_node = node if node else self.root
        add_nodes_edges(root_node)
        output_path = dot.render(filename, view=False, format='png')
        print(f"Tree visualization saved as {output_path}")

    def visualize_heap(self, heap, filename="heap"):
        """
        Creates a visual representation of the current heap using graphviz.
        """
        dot = Digraph(comment='Heap')
        dot.attr(rankdir='LR')  # Left to Right

        # Sort heap for visualization purposes
        sorted_heap = sorted(heap, key=lambda node: node.freq)
        for idx, node in enumerate(sorted_heap):
            if node.char:
                label = f'{node.char}: {node.freq:.2f}'
                dot.node(str(idx), label, shape='box', style='filled', color='lightblue')
            else:
                label = f'Internal: {node.freq:.2f}'
                dot.node(str(idx), label, shape='circle', style='filled', color='lightgreen')

        # Optionally, connect nodes to represent heap structure
        # For simplicity, we'll list them linearly

        output_path = dot.render(filename, view=False, format='png')
        print(f"Heap visualization saved as {output_path}")

# Example usage
if __name__ == "__main__":
    symbols = ['A', 'B', 'C', 'D', '_']
    frequencies = [0.4, 0.1, 0.2, 0.15, 0.15]

    # Create output directory for visualizations
    output_dir = "huffman_visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.chdir(output_dir)

    # Create Huffman codec
    codec = HuffmanCodec(symbols, frequencies)
    codec.print_codes()

    # Visualize the final tree
    codec.visualize_tree(filename="huffman_tree_final")

    # Example encoding and decoding
    text = "ABACABAD"
    encoded = codec.encode(text)
    decoded = codec.decode(encoded)

    decoded2 =codec.decode("100010111001010")

    print(f"\nOriginal text: {text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    print(f"Final Decoded: {decoded2}")
