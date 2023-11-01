import math, queue
from collections import Counter


class TreeNode(object):
  # we assume data is a tuple (frequency, character)
  def __init__(self, left=None, right=None, data=None):
    self.left = left
    self.right = right
    self.data = data

  def __lt__(self, other):
    return (self.data < other.data)

  def children(self):
    return ((self.left, self.right))


def get_frequencies(fname):
  ## This function is done.
  ## Given any file name, this function reads line by line to count the frequency per character.
  f = open(fname, 'r')
  C = Counter()
  for l in f.readlines():
    C.update(Counter(l))
  return (dict(C.most_common()))


# given a dictionary f mapping characters to frequencies,
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
  p = queue.PriorityQueue()
  # construct heap from frequencies, the initial items should be
  # the leaves of the final tree
  for c in f.keys():
    p.put(TreeNode(None, None, (f[c], c)))

  # greedily remove the two nodes x and y with lowest frequency,
  # create a new node z with x and y as children,
  # insert z into the priority queue (using an empty character "")
  while (p.qsize() > 1):
    x = p.get()
    y = p.get()
    z = TreeNode(x, y, (x.data[0] + y.data[0], ""))
    p.put(z)

  # return root of the tree
  return p.get()


# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code={}):
  # TODO - perform a tree traversal and collect encodings for leaves in code
  if node:
    if node.data[1]:  # Check if the node is a leaf
      code[node.data[1]] = prefix
    get_code(node.left, prefix + "0", code)
    get_code(node.right, prefix + "1", code)
  return code


# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
  fixed_length = 8  # Assuming 8 bits per character (ASCII)
  total_cost = 0
  for char, freq in f.items():
    total_cost += freq * fixed_length
  return total_cost


# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
  # TODO
  total_cost = 0
  for char, freq in f.items():
    total_cost += freq * len(
        C[char])  # C[char] is the Huffman encoding of the character
  return total_cost


f = get_frequencies('fields.c')
print("Fixed-length cost:  %d" % fixed_length_cost(f))
T = make_huffman_tree(f)
C = get_code(T)
print("Huffman cost:  %d" % huffman_cost(C, f))
