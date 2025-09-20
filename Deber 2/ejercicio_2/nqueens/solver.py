from __future__ import annotations
from typing import List, Iterator
import time
import math

Board = List[int]

def _iter_solutions_limited(n: int, deadline: float, counters: dict) -> Iterator[Board]:
    """Igual que _iter_solutions pero corta al llegar al time limit.

    - deadline: instante absoluto (time.perf_counter()) en el que abortar.
    - counters: diccionario con acumuladores (al menos 'nodes_visited' y 'solutions_count').
    """
    cols = set()
    diag1 = set()
    diag2 = set()
    placement: Board = [-1] * n

    def backtrack(r: int):
        # chequeo de tiempo al entrar en cada nodo del árbol
        if time.perf_counter() >= deadline:
            raise TimeoutError
        counters['nodes_visited'] = counters.get('nodes_visited', 0) + 1

        if r == n:
            counters['solutions_count'] = counters.get('solutions_count', 0) + 1
            yield placement.copy()
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            placement[r] = c
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            yield from backtrack(r + 1)
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)
            placement[r] = -1

    yield from backtrack(0)

def solve_nqueens_with_limit(n: int, time_limit_sec: float, collect_solutions: bool = True):
    """Resuelve N-Reinas con límite de tiempo.

    Retorna un diccionario con:
      - nodes_visited: nodos visitados (llamadas al backtracking)
      - timed_out: True si se alcanzó el límite de tiempo
      - elapsed: tiempo empleado en segundos
      - worst_nodes: cota superior ignorando diagonales (n!)
      - solutions: lista de soluciones (si collect_solutions=True)
    """
    deadline = time.perf_counter() + time_limit_sec
    counters = { 'nodes_visited': 0, 'solutions_count': 0 }
    solutions: List[Board] | None = [] if collect_solutions else None

    start = time.perf_counter()
    timed_out = False
    try:
        for sol in _iter_solutions_limited(n, deadline, counters):
            if collect_solutions:
                solutions.append(sol)  # type: ignore[arg-type]
    except TimeoutError:
        timed_out = True
    elapsed = time.perf_counter() - start

    result = {
        'nodes_visited': counters.get('nodes_visited', 0),
        'timed_out': timed_out,
        'elapsed': elapsed,
        'worst_nodes': math.factorial(n),
        'solutions': solutions if collect_solutions else None,
    }
    return result