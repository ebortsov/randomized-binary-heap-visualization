import random
random.seed(1337)


def draw_vertex(cx, cy, inner_text, radius, stroke_width, svg_file):
    """
    Write svg code of vertex with black border (stroke_width - the width of this border), with inner
    text, given radius and center at (cx, cy) to svg_file
    """
    svg_file.write(
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" stroke="black" stroke-width="{stroke_width}" fill="white" />\n'
    )
    svg_file.write(
        f'<text x="{cx}" y="{cy}" alignment-baseline="middle" font-weight="bold" font-family="Arial" '
        f'text-anchor="middle" font-size="{radius}">{inner_text}</text>\n'
    )


def draw_edge(x1, y1, x2, y2, stroke_width, svg_file):
    """
    draws an edge from point (x1, y1) to point (x2, y2) with width equal to stroke_width to
    svg file
    """
    svg_file.write(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{stroke_width}"\n/>')


class RandomizedBinaryHeap:
    class Node:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value
            self.priority = random.random()
            self.left_child = self.right_child = None
            self.subtree_size = 1
            self.depth = 1

        @staticmethod
        def get_subtree_size(node):
            return node.subtree_size if node else 0

        @staticmethod
        def get_depth(node):
            return node.depth if node else 0

        def recalc(self):
            """
            Recalculates the parameters of Node (subtree size and depth) from its children
            """
            self.subtree_size = (self.get_subtree_size(self.left_child) +
                                 self.get_subtree_size(self.right_child) + 1)
            self.depth = 1 + max(self.get_depth(self.left_child), self.get_depth(self.right_child))

    def __init__(self):
        self.root = None

    def _merge(self, left_node: Node, right_node: Node):
        """
        Merge tree with root at left_node and right node to single tree
        Returns the root of merged tree
        Merging is based on the priority of nodes
        """
        if not left_node:
            return right_node
        if not right_node:
            return left_node
        if left_node.priority > right_node.priority:
            # left_node should be "above" the right node
            # merge left_node.right_child and right_node to left_node.right_child
            left_node.right_child = self._merge(left_node.right_child, right_node)
            left_node.recalc()
            return left_node
        else:
            # right_node should be "above" the left node
            # merge right_child.left_child and left_node to right_node.left_child
            right_node.left_child = self._merge(left_node, right_node.left_child)
            right_node.recalc()
            return right_node

    def _split(self, node: Node, split_value):
        """
        Splits heap with node in two heaps based on split_value (the keys in left_tree will be <= split_value)
        Returns the tuple of roots of left and right tree
        """
        if not node:
            return None, None
        if node.key <= split_value:
            # split node.right_child to two trees
            (node.right_child, right_node) = self._split(node.right_child, split_value)
            node.recalc()
            return node, right_node
        else:
            # split node.left_child to two trees
            (left_node, node.left_child) = self._split(node.left_child, split_value)
            node.recalc()
            return left_node, node

    def insert(self, key, value=None):
        # Split tree into tree parts based on the key
        left, right = self._split(self.root, key)
        # Insert the element with key right "after" the left part of the tree
        self.root = self._merge(left, RandomizedBinaryHeap.Node(key, value))
        # Finally, merge all three parts together
        self.root = self._merge(self.root, right)

    # Some configuration to draw the tree
    _vertex_radius = 10
    _edge_stroke_width = 3
    _vertex_stroke_width = 3

    def _draw(self, node, left_border, right_border, top_border, svg_file, parent_x=None, parent_y=None):
        """
        Recursive function to draw the tree
        """
        if not node:
            return
        cx = left_border + self._vertex_radius * (4 * node.get_subtree_size(node.left_child) + 1)
        cy = top_border + 2 * self._vertex_radius
        if parent_x:
            # vertex is not the root
            draw_edge(x1=cx,
                      y1=cy,
                      x2=parent_x,
                      y2=parent_y,
                      stroke_width=self._edge_stroke_width,
                      svg_file=svg_file)
        self._draw(
            node=node.left_child,
            left_border=left_border,
            right_border=cx - self._vertex_radius,
            top_border=cy + self._vertex_radius,
            svg_file=svg_file,
            parent_x=cx,
            parent_y=cy
        )
        self._draw(
            node=node.right_child,
            left_border=cx + self._vertex_radius,
            right_border=right_border,
            top_border=cy + self._vertex_radius,
            svg_file=svg_file,
            parent_x=cx,
            parent_y=cy
        )
        draw_vertex(
            cx=cx,
            cy=cy,
            inner_text=node.key,
            radius=self._vertex_radius,
            stroke_width=self._vertex_radius / 5,
            svg_file=svg_file
        )

    def create_svg(self, svg_file):
        width = 100 + RandomizedBinaryHeap.Node.get_subtree_size(self.root) * (self._vertex_radius * 4)
        height = 100 + RandomizedBinaryHeap.Node.get_depth(self.root) * (self._vertex_radius * 4)
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" height="{height}" width="{width}">\n')
        svg_file.write(f'<rect width="{width}" height="{height}" x="0" y="0" fill="white"></rect>\n')
        self._draw(
            node=self.root,
            left_border=50,
            right_border=width-50,
            top_border=50,
            svg_file=svg_file,
        )
        svg_file.write('</svg>\n')
        svg_file.close()


def main():
    heap = RandomizedBinaryHeap()
    for key in random.sample(range(0, 100), k=30):
        heap.insert(key)
    with open("example.svg", mode='w') as file:
        heap.create_svg(file)


if __name__ == "__main__":
    main()
