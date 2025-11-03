import sys
import numpy as np
import unittest
from typing import * #type: ignore
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union[None, "BTNode"]

class BTNode:
    value: Any
    rest: BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    