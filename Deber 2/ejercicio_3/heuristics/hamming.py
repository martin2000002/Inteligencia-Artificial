from __future__ import annotations
from typing import List
from game.board import BoardArr, SIZE

def hamming(cur: BoardArr, goal: BoardArr) -> int:
    return sum(1 for r in range(SIZE) for c in range(SIZE) if cur[r][c] != goal[r][c])
