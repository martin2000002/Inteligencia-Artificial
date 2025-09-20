from __future__ import annotations
from typing import List, Iterator

Board = List[int]
# Representación del tablero: board[row] = col donde hay una reina. Filas 0..n-1, una reina por fila.


def _iter_solutions(n: int) -> Iterator[Board]:
    """Generador central: produce soluciones una por una usando backtracking."""
    cols = set()   # columnas ocupadas
    diag1 = set()  # diagonales r - c
    diag2 = set()  # diagonales r + c
    placement: Board = [-1] * n

    def backtrack(r: int):
        if r == n:
            # retornar una copia para evitar mutación por el backtracking
            yield placement.copy()
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            # colocar
            placement[r] = c
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            yield from backtrack(r + 1)
            # quitar
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            placement[r] = -1

    yield from backtrack(0)


def solve_nqueens(n: int) -> List[Board]:
    """Devuelve todas las soluciones como una lista (materializadas)."""
    return list(_iter_solutions(n))


def solve_nqueens_iter(n: int) -> Iterator[Board]:
    """Genera soluciones una por una (perezoso, eficiente en memoria)."""
    return _iter_solutions(n)