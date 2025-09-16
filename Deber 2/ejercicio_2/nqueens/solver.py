from __future__ import annotations
from typing import List

Board = List[int]
# Board representation: board[row] = col where a queen is placed. Rows are 0..n-1, one queen per row.


def solve_nqueens(n: int) -> List[Board]:
    """Return all solutions for N-Queens using backtracking with efficient conflict checks.

    A solution is represented as a list of column indices, one per row.
    Example for N=4: [1, 3, 0, 2]
    """
    solutions: List[Board] = []

    cols = set()  # occupied columns
    diag1 = set()  # r - c diagonals
    diag2 = set()  # r + c diagonals
    placement: Board = [-1] * n

    def backtrack(r: int) -> None:
        if r == n:
            solutions.append(placement.copy())
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            # place
            placement[r] = c
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            backtrack(r + 1)
            # remove
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            placement[r] = -1

    backtrack(0)
    return solutions
