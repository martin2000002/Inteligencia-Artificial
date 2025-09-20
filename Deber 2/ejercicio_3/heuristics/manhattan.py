from __future__ import annotations
from typing import List
from game.board import BoardArr
from heuristics.distance import board_to_vector

def manhattan_vector(v1: List[int], v2: List[int]) -> int:
    return sum(abs(a - b) for a, b in zip(v1, v2))

def manhattan(cur: BoardArr, goal: BoardArr) -> int:
    """Distancia Manhattan entre la representación vectorial de dos tableros."""
    v1 = board_to_vector(cur)
    v2 = board_to_vector(goal)
    return manhattan_vector(v1, v2)
