from __future__ import annotations
from utils.timer import Timer
from utils.io import write_solutions_text
from nqueens.solver import solve_nqueens, solve_nqueens_iter

# Configuración:
N = 11

def main() -> None:
    n = N
    print(f"Resolviendo {n}-Reinas...")

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

if __name__ == "__main__":
    main()
