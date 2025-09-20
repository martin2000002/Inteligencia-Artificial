from __future__ import annotations
from typing import List
from game.board import BoardArr
from heuristics.distance import board_to_vector

def euclidean_vector(v1: List[int], v2: List[int]) -> float:
    s = sum((a - b) ** 2 for a, b in zip(v1, v2))
    return s ** 0.5

def euclidean(cur: BoardArr, goal: BoardArr) -> float:
    """Distancia Euclídea entre la representación vectorial de dos tableros."""
    v1 = board_to_vector(cur)
    v2 = board_to_vector(goal)
    return euclidean_vector(v1, v2)
