class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.enf_of_word = False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_child(self, child_node):
        self.children.append(child_node)

class LexTree:
    def add_node(self, node):
        pass


if __name__ == '__main__':
    # lex_tree = LexTree()
    # lex_tree.add_node(Node('*'))
    root = Node('*')
    tree_ptr = root

    for line in open('small_dict.txt'):
        tree_ptr = root
        line = line.rstrip('\n')
        for idx, char in enumerate(map(str, line)):
            is_last_char = (idx == len(line) -1)
            if not is_last_char and Node(char) in tree_ptr.children:
                tree_ptr = tree_ptr.children[tree_ptr.children.index(Node(char))]
            else:
                new_node = Node(char)
                if is_last_char : new_node.enf_of_word = True
                tree_ptr.add_child(new_node)
                tree_ptr = new_node

pass


