import sys
import unittest
from typing import * #type: ignore
from dataclasses import dataclass
import math 
import matplotlib.pyplot as plt 
import numpy as np
import random
import time
sys.setrecursionlimit(10**6)
from bst import *

def example_graph_creation() -> None:
    # Return log-base-2 of 'x' + 5.
    def f_to_graph( x : float ) -> float:
        return math.log2( x ) + 5.0
    
    # here we're using "list comprehensions": more of Python's
    # syntax sugar.
    x_coords : List[float] = [ float(i) for i in range( 1, 100 ) ]
    y_coords : List[float] = [ f_to_graph( x ) for x in x_coords ]
    # Could have just used this type from the start, but I want
    # to emphasize that 'matplotlib' uses 'numpy''s specific array
    # type, which is different from the built-in Python array
    # type.
    x_numpy : np.ndarray = np.array( x_coords )
    y_numpy : np.ndarray = np.array( y_coords )
    plt.plot( x_numpy, y_numpy, label = 'log_2(x)' )
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Example Graph")
    plt.grid(True)
    plt.legend() # makes the 'label's show up
    plt.show()

TREES_PER_RUN : int = 10000

# Return a BST with n random floats in [0, 1]
def random_tree(n: int) -> BinarySearchTree:
    bst = BinarySearchTree(lambda a, b: a < b, None)
    for _ in range(n):
       bst = insert(bst, random.random())
    return bst

# Find n_max such that generating TREES_PER_RUN trees of size n_max and inserting a value into each takes 1.5-2.5 seconds
def find_n_max_for_height() -> int:
    n_test = 1000

    while True:
        start_time = time.time()
        for _ in range(TREES_PER_RUN):
            tree = random_tree(n_test)
            tree = insert(tree, random.random())
        elapsed = time.time() - start_time

        print(f"n={n_test}: {elapsed:.2f} seconds")

        if 1.5 <= elapsed <= 2.5:
            print(f"Found n_max = {n_test}")
            return n_test
        elif elapsed < 1.5:
            n_test = int(n_test * 1.5)
        else:
            n_test = int(n_test * 0.8)

# Create a graph of average tree height that uses 50 evenly spaced N values from 0 to n_max.
def graph_average_height() -> None:

    print("\nGraphing Average Height")
    
    # Find optimal n_max
    n_max = find_n_max_for_height()
    
    # Generate 50 evenly spaced N values from 0 to n_max
    n_values = [int(i * n_max / 50) for i in range(51)]
    avg_heights = []
    
    print(f"\nCalculating average heights for 51 different N values...")
    
    for i, n in enumerate(n_values):
        if n == 0:
            avg_heights.append(0)
            continue
        
        total_height = 0
        for _ in range(TREES_PER_RUN):
            tree = random_tree(n)
            total_height += height(tree)
        
        avg_height = total_height / TREES_PER_RUN
        avg_heights.append(avg_height)
        
        # Print progress every 10 values
        if i % 10 == 0:
            print(f"Progress: {i}/51 - N={n}, Average Height={avg_height:.2f}")
    
    # Create the graph
    x_numpy = np.array(n_values)
    y_numpy = np.array(avg_heights)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_numpy, y_numpy, 'b-', linewidth=2, label='Average Height')
    
    # Optional: Add theoretical O(log n) curve for comparison
    # For random BSTs, expected height is approximately 1.39 * log2(n)
    theoretical_heights = [1.39 * math.log2(n) if n > 0 else 0 for n in n_values]
    plt.plot(x_numpy, theoretical_heights, 'r--', linewidth=1, label='1.39 * log₂(N) (theoretical)')
    
    plt.xlabel("Tree Size (N)", fontsize=12)
    plt.ylabel("Average Height", fontsize=12)
    plt.title("Average Height of Random Binary Search Trees", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('average_height_graph.png', dpi=300)
    print("\nGraph saved as 'average_height_graph.png'")
    plt.show()

# Find n_max such that generating TREES_PER_RUN trees of size n_max and inserting a value into each takes 1.5-2.5 seconds.
def find_n_max_for_insert() -> int:

    print("\nFinding optimal n_max for insert timing...")
    
    # Start with an initial guess
    n_test = 1000
    
    while True:
        start_time = time.time()
        for _ in range(TREES_PER_RUN):
            tree = random_tree(n_test)
            tree = insert(tree, random.random())
        elapsed = time.time() - start_time
        
        print(f"n={n_test}: {elapsed:.2f} seconds")
        
        if 1.5 <= elapsed <= 2.5:
            print(f"Found n_max = {n_test}")
            return n_test
        elif elapsed < 1.5:
            # Too fast, increase n
            n_test = int(n_test * 1.5)
        else:
            # Too slow, decrease n
            n_test = int(n_test * 0.8)

# Create a graph of time-required-to-insert-a-random-value
def graph_insert_time() -> None:
    n_max = find_n_max_for_insert()

    n_values = [int(i * n_max / 50) for i in range(51)]
    avg_times = []

    for i, n in enumerate(n_values):
        if n == 0:
            avg_times.append(0)
            continue
        
        start_time = time.time()
        for _ in range(TREES_PER_RUN):
            tree = random_tree(n)
            tree = insert(tree, random.random())
        elapsed = time.time() - start_time

        avg_time = (elapsed / TREES_PER_RUN) * 1_000_000
        avg_times.append(avg_time)

        if i % 10 == 0:
            print(f"Progress: {i}/51 - N={n}, Average Insert Time={avg_time:.2f} μs")
        
        x_numpy = np.array(n_values)
    y_numpy = np.array(avg_times)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_numpy, y_numpy, 'g-', linewidth=2, label='Average Insert Time')
    
    plt.xlabel("Tree Size (N)", fontsize=12)
    plt.ylabel("Average Insert Time (microseconds)", fontsize=12)
    plt.title("Time to Insert a Random Value into Random Binary Search Trees", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('insert_time_graph.png', dpi=300)
    print("\nGraph saved as 'insert_time_graph.png'")
    plt.show()

if (__name__ == '__main__'):
    print("Binary Search Tree Performance Analysis")
    print("=" * 50)
    print(f"TREES_PER_RUN = {TREES_PER_RUN}")
    print()
    
    # Generate height graph
    graph_average_height()
    
    # Generate insert time graph
    graph_insert_time()
    
    print("\n" + "=" * 50)
    print("Analysis complete!")