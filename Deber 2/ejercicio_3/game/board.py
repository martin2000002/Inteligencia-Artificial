from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Iterable, Optional

Cell = str  # 'X', 'O', or '.'
BoardArr = List[List[Cell]]  # 4x4
Pos = Tuple[int, int]

SIZE = 4


def parse_board(lines: List[str]) -> BoardArr:
    b: BoardArr = []
    for line in lines:
        row = [c for c in line.strip().split()]  # expects tokens separated by spaces
        assert len(row) == SIZE, "Each row must have 4 cells"
        b.append(row)
    assert len(b) == SIZE, "Board must be 4x4"
    return b


def board_to_lines(b: BoardArr) -> List[str]:
    return [" ".join(row) for row in b]


def positions_of(b: BoardArr, token: Cell) -> List[Pos]:
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if b[r][c] == token]


def empties(b: BoardArr) -> List[Pos]:
    return positions_of(b, ".")


def next_player(b: BoardArr) -> Cell:
    x = sum(cell == 'X' for row in b for cell in row)
    o = sum(cell == 'O' for row in b for cell in row)
    return 'X' if x == o else 'O'


def place(b: BoardArr, pos: Pos, token: Cell) -> BoardArr:
    r, c = pos
    assert b[r][c] == '.', "Cell must be empty"
    nb = [row[:] for row in b]
    nb[r][c] = token
    return nb


def winner(b: BoardArr) -> Optional[Cell]:
    lines: List[List[Cell]] = []
    # rows and cols
    for i in range(SIZE):
        lines.append([b[i][j] for j in range(SIZE)])
        lines.append([b[j][i] for j in range(SIZE)])
    # diagonals
    lines.append([b[i][i] for i in range(SIZE)])
    lines.append([b[i][SIZE - 1 - i] for i in range(SIZE)])

    for line in lines:
        if all(c == 'X' for c in line):
            return 'X'
        if all(c == 'O' for c in line):
            return 'O'
    return None


def hamming_to_goal(cur: BoardArr, goal: BoardArr) -> int:
    """Number of cells that differ between current board and goal board."""
    return sum(1 for r in range(SIZE) for c in range(SIZE) if cur[r][c] != goal[r][c])


def goal_consistent_moves(cur: BoardArr, goal: BoardArr) -> Iterable[Tuple[Pos, Cell]]:
    """Generate moves (pos, token) that are consistent with eventually reaching goal.

    Only allow placing the current player's token on an empty cell where goal has the same token.
    """
    player = next_player(cur)
    for r, c in empties(cur):
        if goal[r][c] == player:
            yield (r, c), player
