from __future__ import annotations
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from utils.io import write_solutions_text
from nqueens.solver import solve_nqueens_with_limit
from shared.format.console import print_boxed_title, subtitle_block


def run_for(n: int) -> None:
    print_boxed_title(f"N = {n}")

    with subtitle_block():
        time_limit = 15
        print(f"Resolviendo {n}-Reinas (límite {time_limit}s)...")
        res = solve_nqueens_with_limit(n, time_limit_sec=time_limit, collect_solutions=True)
        print(f"Tiempo: {res['elapsed']:.3f}s  |  Timeout: {res['timed_out']}")
        print(f"Nodos visitados: {res['nodes_visited']}  |  Peor caso (n!): {res['worst_nodes']}")
        solutions = res['solutions'] or []
        print(f"Soluciones encontradas: {len(solutions)}")
        if n <= 8:
            write_solutions_text(
                solutions,
                n,
                filename_prefix=f"nqueens_{n}x{n}"
            )


def main() -> None:
    for n in (5, 8, 11, 27):
        run_for(n)


if __name__ == "__main__":
    main()
