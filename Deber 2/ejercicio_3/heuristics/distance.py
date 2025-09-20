from __future__ import annotations
from typing import List, Mapping
from game.board import BoardArr, SIZE

SYMBOL_MAP_DEFAULT: Mapping[str, int] = {
    '.': 0,
    'X': -1,
    'O': 1,
}

def board_to_vector(board: BoardArr, symbol_map: Mapping[str, int] = SYMBOL_MAP_DEFAULT) -> List[int]:
    vec: List[int] = []
    for r in range(SIZE):
        for c in range(SIZE):
            v = board[r][c]
            vec.append(symbol_map.get(v, 0))
    return vec