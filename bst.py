import sys
import numpy as np
import unittest
from typing import * #type: ignore
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union[None, "BTNode"]

@dataclass(frozen=True)
class BTNode:
    value: Any
    left: BinTree
    right: BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Callable[[Any, Any], bool]
    tree: BinTree

# Return true if tree is empty, false otherwise
def is_empty(bst: BinarySearchTree) -> bool:
    return bst.tree is None

# Insert value to the tree using comes_before function
def insert(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    new_root = insert_helper(bst.comes_before, bst.tree, value)
    return BinarySearchTree(bst.comes_before, new_root)

def insert_helper(comes_before: Callable[[Any, Any], bool], tree: BinTree, value: Any) -> BinTree:
    if tree is None:
        return BTNode(value, None, None)
    if comes_before(value, tree.value):
        return BTNode(tree.value, insert_helper(comes_before, tree.left, value), tree.right)
    else:
        return BTNode(tree.value, tree.left, insert_helper(comes_before, tree.right, value))

# Return True if the value is stored in the tree
def lookup(bst: BinarySearchTree, value: Any) -> bool:
    return lookup_helper(bst.comes_before, bst.tree, value)

def lookup_helper(comes_before: Callable[[Any, Any], bool], tree: BinTree, value: Any) -> bool:
    if tree is None:
        return False
    if not comes_before(value, tree.value) and not comes_before(tree.value, value):
        return True
    if comes_before(value, tree.value):
        return lookup_helper(comes_before, tree.left, value)
    else:
        return lookup_helper(comes_before, tree.right, value)

# Remove value from tree while preserving the binary search tree property
def delete(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    new_root = delete_helper(bst.comes_before, bst.tree, value)
    return BinarySearchTree(bst.comes_before, new_root)

def delete_helper(comes_before: Callable[[Any, Any], bool], tree: BinTree, value: Any) -> BinTree:
    if tree is None:
        return None
    if not comes_before(value, tree.value) and not comes_before(tree.value, value):
        if tree.left is None and tree.right is None:
            return None
        elif tree.left is None:
            return tree.right
        elif tree.right is None:
            return tree.left
        else:
            min_value = find_min(tree.right)
            new_right = delete_helper(comes_before, tree.right, min_value)
            return BTNode(min_value, tree.left, new_right)
    if comes_before(value, tree.value):
        return BTNode(tree.value, delete_helper(comes_before, tree.left, value), tree.right)
    else:
        return BTNode(tree.value, tree.left, delete_helper(comes_before, tree.right, value),)

# Finds and returns the minimum value in a binary search tree.
def find_min(tree: BinTree) -> Any:
    if tree is None:
        return None
    if tree.left is None:
        return tree.value
    return find_min(tree.left)

# Return the height of the BST
def height(bst: BinarySearchTree) -> int:
    return height_helper(bst.tree)

def height_helper(tree: BinTree) -> int:
    if tree is None:
        return 0
    else:
        return 1 + max(height_helper(tree.left), height_helper(tree.right))
    

