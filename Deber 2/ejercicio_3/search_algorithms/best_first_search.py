from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
import heapq
from game.board import BoardArr, place, goal_consistent_moves
from heuristics.hamming import hamming


@dataclass(order=True)
class PQItem:
    priority: float
    counter: int
    board: BoardArr = field(compare=False)
    parent_key: Optional[str] = field(compare=False, default=None)
    move: Optional[Tuple[Tuple[int, int], str]] = field(compare=False, default=None)


def board_key(b: BoardArr) -> str:
    return "".join("".join(row) for row in b)


def best_first_search(start: BoardArr, goal: BoardArr, heuristic: Optional[Callable[[BoardArr, BoardArr], float]] = None):
    """Búsqueda Greedy Best-First usando una heurística arbitraria (por defecto, Hamming)."""
    if heuristic is None:
        heuristic = hamming
    # Priority queue with (heuristic, counter) to make ordering stable
    pq: List[PQItem] = []
    counter = 0

    start_h = heuristic(start, goal)
    heapq.heappush(pq, PQItem(start_h, counter, start, None, None))

    # Mapa para reconstruir el camino: key -> (parent_key, move)
    came_from: Dict[str, Tuple[Optional[str], Optional[Tuple[Tuple[int, int], str]]]] = {}
    came_from[board_key(start)] = (None, None)

    # Conjuntos/contadores para métricas
    visited: set[str] = set()
    generated = 1

    while pq:
        item = heapq.heappop(pq)
        b = item.board
        k = board_key(b)
        if k in visited:
            continue
        visited.add(k)

        if b == goal:
            # Reconstruir la secuencia de movimientos desde el mapa came_from
            seq: List[Tuple[Tuple[int, int], str]] = []
            cur = k
            while True:
                parent, mv = came_from[cur]
                if parent is None:
                    break
                if mv is not None:
                    seq.append(mv)
                cur = parent
            seq.reverse()
            # Reconstruir los tableros aplicando los movimientos desde el inicio
            boards: List[BoardArr] = [start]
            curb = start
            for (pos, token) in seq:
                curb = place(curb, pos, token)
                boards.append(curb)

            return {
                "found": True,
                "generated": generated,
                "visited": len(visited),
                "moves": seq,
                "boards": boards,
            }

        # Expandir nodos (generar sucesores)
        for (pos, token) in goal_consistent_moves(b, goal):
            nb = place(b, pos, token)
            nk = board_key(nb)
            if nk in visited:
                continue
            counter += 1
            generated += 1
            prio = heuristic(nb, goal)
            heapq.heappush(pq, PQItem(prio, counter, nb, k, (pos, token)))
            if nk not in came_from:
                came_from[nk] = (k, (pos, token))

    return {
        "found": False,
        "generated": generated,
        "visited": len(visited),
        "moves": [],
        "boards": [],
    }
