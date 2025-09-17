from __future__ import annotations
from typing import List, Tuple, Optional, Dict, Any

from game.board import BoardArr, Pos, SIZE, empties, next_player, place, winner


def search_any_winner(start: BoardArr) -> Dict[str, Any]:
    """DFS exhaustivo: explora todas las jugadas posibles alternando turnos.
    Devuelve si existe alguna secuencia que produzca un ganador y, de haberla,
    el camino (jugadas) y las tablas correspondientes.
    """
    visited = 0
    generated = 0

    def dfs(board: BoardArr, path: List[Tuple[Pos, str]], boards: List[BoardArr]) -> Optional[Dict[str, Any]]:
        nonlocal visited, generated
        visited += 1

        w = winner(board)
        if w is not None:
            return {
                "winner": w,
                "path": path[:],
                "boards": boards[:],
            }
        # Si no hay más espacios, no hay ganador en esta rama
        spaces = empties(board)
        if not spaces:
            return None

        token = next_player(board)
        for pos in spaces:
            nb = place(board, pos, token)
            generated += 1
            res = dfs(nb, path + [(pos, token)], boards + [nb])
            if res is not None:
                return res
        return None

    res = dfs(start, [], [start])

    return {
        "winner_possible": res is not None,
        "winner": None if res is None else res["winner"],
        "path": [] if res is None else res["path"],
        "boards": [] if res is None else res["boards"],
        "visited": visited,
        "generated": generated,
    }
