from __future__ import annotations
from typing import List

from game.board import parse_board, board_to_lines, winner
from search_algorithms.best_first_search import best_first_search
from search_algorithms.exhaustive_playout import search_any_winner


def run_case(name: str, start_lines: List[str], goal_lines: List[str]) -> None:
    print(f"\n=== Caso {name} ===")
    start = parse_board(start_lines)
    goal = parse_board(goal_lines)

    res = best_first_search(start, goal)

    print(f"Encontrado: {res['found']}")
    print(f"Generados: {res['generated']}")
    print(f"Visitados: {res['visited']}")
    if res['found']:
        print(f"Longitud del camino: {len(res['moves'])} jugadas")
        for i, b in enumerate(res['boards']):
            print(f"Paso {i}:")
            print("\n".join(board_to_lines(b)))
            print()


def analyze_case_b_final(goal_lines: List[str]) -> None:
    print("\n=== Caso (b): análisis de que no hay ganador posible continuando ===")
    final_b = parse_board(goal_lines)
    w = winner(final_b)
    if w:
        print(f"Ya hay ganador en el estado final: {w}")
        return

    res = search_any_winner(final_b)
    print(f"Estados visitados: {res['visited']}")
    print(f"Estados generados: {res['generated']}")
    if not res['winner_possible']:
        print("No existe secuencia de jugadas que produzca un ganador desde este estado final (b).")
    else:
        print("Se encontró una secuencia ganadora (esto contradice la hipótesis):")
        for i, b in enumerate(res['boards']):
            print(f"Paso {i}:")
            print("\n".join(board_to_lines(b)))
            print()


if __name__ == "__main__":
    # Caso (a)
    start_a = [
        ". . . O",
        ". X . .",
        ". . O .",
        ". . . X",
    ]
    goal_a = [
        ". . . O",
        "X X O .",
        ". O O .",
        "X O X X",
    ]
    run_case("(a)", start_a, goal_a)

    # Caso (b)
    start_b = [
        ". . . .",
        ". . . .",
        ". . . .",
        ". . . .",
    ]
    goal_b = [
        "X X X O",
        "O O O X",
        ". X . .",
        "O . . .",
    ]
    run_case("(b)", start_b, goal_b)
    analyze_case_b_final(goal_b)

    # Caso (c)
    start_c = [
        "X . . O",
        ". X O O",
        ". X X X",
        ". . . O",
    ]
    goal_c = [
        "X X X O",
        "X X O O",
        "O X X X",
        "O O O O",
    ]
    run_case("(c)", start_c, goal_c)
