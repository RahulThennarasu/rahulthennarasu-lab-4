import sys
import unittest
from typing import * #type: ignore
from dataclasses import dataclass
sys.setrecursionlimit(10**6)
from bst import *

@dataclass(frozen=True)
class Point2:
   x: float
   y: float

class BSTTests(unittest.TestCase):
    def test_numeric_insert_and_lookup(self):
        bst = BinarySearchTree(lambda a, b: a < b, None)
        bst = insert(bst, 5)
        bst = insert(bst, 3)
        bst = insert(bst, 7)
        bst = insert(bst, 1)
        bst = insert(bst, 9)
        
        self.assertTrue(lookup(bst, 5))
        self.assertTrue(lookup(bst, 3))
        self.assertTrue(lookup(bst, 7))
        self.assertTrue(lookup(bst, 1))
        self.assertTrue(lookup(bst, 9))
        self.assertFalse(lookup(bst, 4))
        self.assertFalse(lookup(bst, 10))
    
    def test_numeric_delete(self):
        bst = BinarySearchTree(lambda a, b: a < b, None)
        bst = insert(bst, 5)
        bst = insert(bst, 3)
        bst = insert(bst, 7)
        bst = insert(bst, 1)
        bst = insert(bst, 9)
        
        bst = delete(bst, 3)
        self.assertFalse(lookup(bst, 3))
        self.assertTrue(lookup(bst, 5))
        self.assertTrue(lookup(bst, 7))
        
        bst = delete(bst, 5)
        self.assertFalse(lookup(bst, 5))
        self.assertTrue(lookup(bst, 7))
    
    def test_numeric_is_empty(self):
        bst = BinarySearchTree(lambda a, b: a < b, None)
        self.assertTrue(is_empty(bst))
        
        bst = insert(bst, 5)
        self.assertFalse(is_empty(bst))
    
    def test_string_insert_and_lookup(self):
        bst = BinarySearchTree(lambda a, b: a < b, None)
        bst = insert(bst, "dog")
        bst = insert(bst, "cat")
        bst = insert(bst, "elephant")
        bst = insert(bst, "ant")
        
        self.assertTrue(lookup(bst, "dog"))
        self.assertTrue(lookup(bst, "cat"))
        self.assertTrue(lookup(bst, "elephant"))
        self.assertTrue(lookup(bst, "ant"))
        self.assertFalse(lookup(bst, "zebra"))
    
    def test_string_delete(self):
        bst = BinarySearchTree(lambda a, b: a < b, None)
        bst = insert(bst, "dog")
        bst = insert(bst, "cat")
        bst = insert(bst, "elephant")
        
        bst = delete(bst, "cat")
        self.assertFalse(lookup(bst, "cat"))
        self.assertTrue(lookup(bst, "dog"))
        self.assertTrue(lookup(bst, "elephant"))
    
    def test_point_insert_and_lookup(self):
        def point_comes_before(p1: Point2, p2: Point2) -> bool:
            dist1 = (p1.x ** 2 + p1.y ** 2) ** 0.5
            dist2 = (p2.x ** 2 + p2.y ** 2) ** 0.5
            return dist1 < dist2
        
        bst = BinarySearchTree(point_comes_before, None)
        p1 = Point2(3, 4)
        p2 = Point2(1, 1)  
        p3 = Point2(5, 0)
        p4 = Point2(0, 1)  
        
        bst = insert(bst, p1)
        bst = insert(bst, p2)
        bst = insert(bst, p3)
        bst = insert(bst, p4)
        
        self.assertTrue(lookup(bst, p1))
        self.assertTrue(lookup(bst, p2))
        self.assertTrue(lookup(bst, p3))
        self.assertTrue(lookup(bst, p4))
        self.assertFalse(lookup(bst, Point2(10, 10)))
    
    def test_point_delete(self):
        def point_comes_before(p1: Point2, p2: Point2) -> bool:
            dist1 = (p1.x ** 2 + p1.y ** 2) ** 0.5
            dist2 = (p2.x ** 2 + p2.y ** 2) ** 0.5
            return dist1 < dist2
        
        bst = BinarySearchTree(point_comes_before, None)
        p1 = Point2(3, 4)
        p2 = Point2(1, 1)
        p3 = Point2(5, 0)
        
        bst = insert(bst, p1)
        bst = insert(bst, p2)
        bst = insert(bst, p3)
        
        bst = delete(bst, p2)
        self.assertFalse(lookup(bst, p2))
        self.assertTrue(lookup(bst, p1))
        self.assertTrue(lookup(bst, p3))

if (__name__ == '__main__'):
 unittest.main() 