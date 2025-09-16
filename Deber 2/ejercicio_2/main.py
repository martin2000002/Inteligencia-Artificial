from __future__ import annotations
from utils.timer import Timer
from utils.io import write_solutions_text, ensure_dir
from nqueens.solver import solve_nqueens
from nqueens.counter import total_n_queens

# Configuración:
N = 14

def main() -> None:
    n = N
    print(f"Resolviendo {n}-Reinas...")

    if n <= 8:
        # Enumerar soluciones y exportar archivos
        with Timer() as t:
            solutions = solve_nqueens(n)
        print(f"N={n}: {len(solutions)} soluciones encontradas en {t.elapsed:.3f}s")

        write_solutions_text(
            solutions,
            n,
            filename_prefix=f"nqueens_{n}x{n}"
        )
    else:
        # Solo contar para N grandes
        with Timer() as t:
            count = total_n_queens(n)
        print(f"N={n}: {count} soluciones (solo conteo) en {t.elapsed:.3f}s")

if __name__ == "__main__":
    main()
