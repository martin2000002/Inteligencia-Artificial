from __future__ import annotations
from typing import List
import os

Board = List[int]

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def board_to_absolute_positions(board: Board) -> List[int]:
    """Mapea un tablero a posiciones absolutas 1..N^2 como pide el enunciado.

    Representación del tablero: board[row] = col donde está la reina (indexado desde 0).
    Numeración absoluta (indexada desde 1), orden por filas:
      posición = row * N + col + 1
    """
    n = len(board)
    return [r * n + c + 1 for r, c in enumerate(board)]


def board_to_text_grid(board: Board) -> str:
    n = len(board)
    rows = []
    for r in range(n):
        row = ["."] * n
        c = board[r]
        if 0 <= c < n:
            row[c] = "Q"
        rows.append(" ".join(row))
    return "\n".join(rows)


def write_solutions_text(
    solutions: List[Board],
    n: int,
    filename_prefix: str,
    limit: int | None = None,
) -> None:
    out_dir = "Deber 2/ejercicio_2/visualization"
    ensure_dir(out_dir)
    # 1) archivo con posiciones absolutas
    abs_path = os.path.join(out_dir, f"{filename_prefix}_absolute.txt")
    # 2) archivo con visualización en rejilla
    grid_path = os.path.join(out_dir, f"{filename_prefix}_grids.txt")

    max_items = len(solutions) if limit is None else min(limit, len(solutions))

    with open(abs_path, "w", encoding="utf-8") as fa, open(grid_path, "w", encoding="utf-8") as fg:
        fa.write(f"N={n} total_solutions={len(solutions)}\n\n")
        fg.write(f"N={n} total_solutions={len(solutions)}\n\n")
        for idx, sol in enumerate(solutions[:max_items], start=1):
            positions = board_to_absolute_positions(sol)
            fa.write(f"Solution {idx}: {positions}\n")

            fg.write(f"Solution {idx}:\n")
            fg.write(board_to_text_grid(sol))
            fg.write("\n\n")
