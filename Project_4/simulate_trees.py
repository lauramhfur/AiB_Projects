import random

class TreeNode:
    def __init__(self, label = None, left = None, right = None):
        self.label = label
        self.left = left
        self.right = right

def generate_tree(n, used_labels = None):
    if n == 1:
        label = 'seq1'  # Ensuring that the trees always have at least one shared sequence.
        while label in used_labels:
            label = 'seq' + str(random.randint(2, 1000))  # Drawing sequences from a pool of 1000 sequences.
        used_labels.add(label)  # Keeping track of used labels to ensure that sequences in the tree are unique.
        return TreeNode(label = label)

    left_size = random.randint(1, n - 1) # The left subtree has at least one node (n > 1) and at most n - 1 nodes, leaving at least one node for the right subtree.
    right_size = n - left_size

    left_subtree = generate_tree(left_size, used_labels)
    right_subtree = generate_tree(right_size, used_labels)

    return TreeNode(left = left_subtree, right = right_subtree)

def tree_to_newick(node):
    if node is None:
        return ''
    if node.left is None and node.right is None:
        return node.label
    return '(' + tree_to_newick(node.left) + ',' + tree_to_newick(node.right) + ')'

def write_newick(tree, filename):
    newick = tree_to_newick(tree) + ';'
    with open(filename, 'w') as file:
        file.write(newick)

        