from __future__ import annotations
from typing import List, Iterator

Board = List[int]
# Board representation: board[row] = col where a queen is placed. Rows are 0..n-1, one queen per row.


def _iter_solutions(n: int) -> Iterator[Board]:
    """Core generator: yields solutions one by one using backtracking."""
    cols = set()   # occupied columns
    diag1 = set()  # r - c diagonals
    diag2 = set()  # r + c diagonals
    placement: Board = [-1] * n

    def backtrack(r: int):
        if r == n:
            # yield a copy to avoid mutation by backtracking
            yield placement.copy()
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            # place
            placement[r] = c
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            yield from backtrack(r + 1)
            # remove
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            placement[r] = -1

    yield from backtrack(0)


def solve_nqueens(n: int) -> List[Board]:
    """Return all solutions as a list (materialized)."""
    return list(_iter_solutions(n))


def solve_nqueens_iter(n: int) -> Iterator[Board]:
    """Yield solutions one by one (lazy, memory efficient)."""
    return _iter_solutions(n)