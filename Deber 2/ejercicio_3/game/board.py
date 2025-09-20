from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Iterable, Optional

Cell = str
BoardArr = List[List[Cell]]
Pos = Tuple[int, int]

SIZE = 4


def parse_board(lines: List[str]) -> BoardArr:
    """Parsea una representación en líneas a la estructura interna del tablero."""
    b: BoardArr = []
    for line in lines:
        row = [c for c in line.strip().split()]  # espera tokens separados por espacios
        assert len(row) == SIZE, "Cada fila debe tener 4 casillas"
        b.append(row)
    assert len(b) == SIZE, "El tablero debe ser 4x4"
    return b


def board_to_lines(b: BoardArr) -> List[str]:
    """Convierte el tablero en una lista de líneas legibles."""
    return [" ".join(row) for row in b]


def positions_of(b: BoardArr, token: Cell) -> List[Pos]:
    """Devuelve las posiciones (fila, columna) donde aparece `token`."""
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if b[r][c] == token]


def empties(b: BoardArr) -> List[Pos]:
    """Posiciones vacías ('.') en el tablero."""
    return positions_of(b, ".")


def next_player(b: BoardArr) -> Cell:
    """Determina el jugador que mueve a continuación ('X' o 'O')."""
    x = sum(cell == 'X' for row in b for cell in row)
    o = sum(cell == 'O' for row in b for cell in row)
    return 'X' if x == o else 'O'


def place(b: BoardArr, pos: Pos, token: Cell) -> BoardArr:
    """Devuelve un nuevo tablero con `token` colocado en `pos`."""
    r, c = pos
    assert b[r][c] == '.', "La casilla debe estar vacía"
    nb = [row[:] for row in b]
    nb[r][c] = token
    return nb


def winner(b: BoardArr) -> Optional[Cell]:
    """Comprueba si hay ganador y devuelve 'X' o 'O', o None si no hay."""
    lines: List[List[Cell]] = []
    # filas y columnas
    for i in range(SIZE):
        lines.append([b[i][j] for j in range(SIZE)])
        lines.append([b[j][i] for j in range(SIZE)])
    # diagonales
    lines.append([b[i][i] for i in range(SIZE)])
    lines.append([b[i][SIZE - 1 - i] for i in range(SIZE)])

    for line in lines:
        if all(c == 'X' for c in line):
            return 'X'
        if all(c == 'O' for c in line):
            return 'O'
    return None


def hamming_to_goal(cur: BoardArr, goal: BoardArr) -> int:
    """Número de casillas que difieren entre el tablero actual y el objetivo."""
    return sum(1 for r in range(SIZE) for c in range(SIZE) if cur[r][c] != goal[r][c])


def goal_consistent_moves(cur: BoardArr, goal: BoardArr) -> Iterable[Tuple[Pos, Cell]]:
    """Genera movimientos (pos, token) que son consistentes con alcanzar el objetivo.

    Solo permite colocar la ficha del jugador actual en una casilla vacía donde el objetivo
    tiene la misma ficha.
    """
    player = next_player(cur)
    for r, c in empties(cur):
        if goal[r][c] == player:
            yield (r, c), player
