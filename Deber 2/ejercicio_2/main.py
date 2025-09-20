from __future__ import annotations
import os
import sys

# Ensure project root is on sys.path so `shared` can be imported when running the script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from utils.timer import Timer
from utils.io import write_solutions_text
from nqueens.solver import solve_nqueens, solve_nqueens_iter
from shared.format.console import print_boxed_title, subtitle_block


def run_for(n: int) -> None:
    print_boxed_title(f"N = {n}")
    print(f"Resolviendo {n}-Reinas...")

    with subtitle_block():
        if n <= 8:
            # Generar todas las soluciones (almacenadas) y exportar archivos
            with Timer() as t:
                solutions = solve_nqueens(n)
            print(f"N={n}: {len(solutions)} soluciones generadas en {t.elapsed:.3f}s")
            write_solutions_text(
                solutions,
                n,
                filename_prefix=f"nqueens_{n}x{n}"
            )
        else:
            # Generar todas las soluciones (sin almacenar) y solo contar
            count = 0
            with Timer() as t:
                for _ in solve_nqueens_iter(n):
                    count += 1
            print(f"N={n}: {count} soluciones generadas (no almacenadas) en {t.elapsed:.3f}s")


def main() -> None:
    for n in (5, 8, 11, 27):
        run_for(n)


if __name__ == "__main__":
    main()
