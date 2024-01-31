import random

random.seed(69)


def draw_vertex(cx, cy, value, radius, stroke_width, svg_file):
    svg_file.write(
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" stroke="black" stroke-width="{stroke_width}" fill="white" />\n'
    )
    svg_file.write(
        f'<text x="{cx}" y="{cy}" alignment-baseline="middle" font-weight="bold" font-family="Arial" '
        f'text-anchor="middle" font-size="{radius}">{value}</text>\n'
    )


def draw_edge(x1, y1, x2, y2, stroke_width, svg_file):
    svg_file.write(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{stroke_width}"\n/>')


class RandomizedBinaryHeap:
    class Node:
        def __init__(self, value):
            self.value = value
            self.priority = random.random()
            self.left_child = self.right_child = None
            self.subtree_size = 1
            self.depth = 1

        @staticmethod
        def get_subtree_size(node):
            return node.subtree_size if node else 1

        @staticmethod
        def get_depth(node):
            return node.depth if node else 0

        def recalc(self):
            self.subtree_size = (self.get_subtree_size(self.left_child) +
                                 self.get_subtree_size(self.right_child) + 1)
            self.depth = 1 + max(self.get_depth(self.left_child), self.get_depth(self.right_child))

    def __init__(self):
        self.root = None

    def _merge(self, left_node: Node, right_node: Node):
        if not left_node:
            return right_node
        if not right_node:
            return left_node
        if left_node.priority > right_node.priority:
            left_node.right_child = self._merge(left_node.right_child, right_node)
            left_node.recalc()
            return left_node
        else:
            right_node.left_child = self._merge(left_node, right_node.left_child)
            right_node.recalc()
            return right_node

    def _split(self, node: Node, split_value):
        """Split heap with node in two heaps. The elements in left one has value <= split_value"""
        if not node:
            return None, None
        if node.value <= split_value:
            (node.right_child, right_node) = self._split(node.right_child, split_value)
            node.recalc()
            return node, right_node
        else:
            (left_node, node.left_child) = self._split(node.left_child, split_value)
            node.recalc()
            return left_node, node

    def insert(self, elem: int):
        left, right = self._split(self.root, elem)
        self.root = self._merge(left, RandomizedBinaryHeap.Node(elem))
        self.root = self._merge(self.root, right)

    _vertex_radius = 10

    def draw(self, node, x1, x2, y, svg_file, parent_pos=None):
        if not node:
            return
        x = x1 + self._vertex_radius * (4 * node.get_subtree_size(node.left_child) + 1)
        draw_vertex(
            cx=x, cy=y + self._vertex_radius, value=node.value,
            radius=self._vertex_radius, stroke_width=self._vertex_radius / 5, svg_file=svg_file
        )

    def create_svg(self):
        svg_file = open("file.svg", mode="w")
        width = 100 + self.root.get_subtree_size(self.root) * (self._vertex_radius * 4)
        height = 100 + self.root.get_depth(self.root) * (self._vertex_radius * 4)
        svg_file.write(f'<svg xmlns="http://www.w3.org/2000/svg" height="{height}" width="{width}">\n')
        svg_file.write(f'<rect width="{width}" height="{height}" x="0" y="0" fill="white"></rect>\n')
        self.draw(self.root, 50, width - 50, 50, svg_file)
        # draw_vertex(
        #     cx=50, cy=50, value=1, stroke_width=self._vertex_radius / 4, radius=self._vertex_radius, svg_file=svg_file
        # )
        # draw_edge(
        #     x1=10, y1=20, x2=100, y2=100, stroke_width=self._vertex_radius / 5, svg_file=svg_file
        # )
        svg_file.write('</svg>\n')
        svg_file.close()


def main():
    heap = RandomizedBinaryHeap()
    heap.insert(20)
    heap.insert(2)
    heap.insert(10)
    heap.insert(15)
    heap.insert(7)
    heap.insert(2)
    heap.create_svg()
    pass


if __name__ == "__main__":
    main()
