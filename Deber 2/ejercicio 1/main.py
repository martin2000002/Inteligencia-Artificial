from eight_tile.eight_tile import EightTile
from search_algorithms.bfs import bfs_search
from search_algorithms.dfs import dfs_search
from search_algorithms.best_first_search import best_first_search, get_heuristic
from visualization.generator.graphml_export import export_search_tree

if __name__ == "__main__":
    initial = [1,2,3,0,5,6,4,7,8]
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    board = EightTile(initial, goal)
    print("Estado inicial:")
    print(board)

    print("\nBuscando solución con BFS...")
    path_bfs, parent_bfs, max_depth_bfs, max_width_bfs = bfs_search(board)
    if path_bfs:
        print(f"\n¡Solución BFS encontrada en {len(path_bfs)-1} movimientos!")
        print("Profundidad del árbol generado:", max_depth_bfs)
        print("Ancho máximo del árbol:", max_width_bfs)
        print("Estados del camino solución:")
        for state in path_bfs:
            print(state)
            print("-" * 8)
        export_search_tree(parent_bfs, path_bfs, "bfs_tree.graphml")
    else:
        print("No se encontró solución con BFS.")

    print("\nBuscando solución con DFS...")
    path_dfs, parent_dfs, max_depth_dfs, max_width_dfs = dfs_search(board)
    if path_dfs:
        print(f"\n¡Solución DFS encontrada en {len(path_dfs)-1} movimientos!")
        print("Profundidad del árbol generado:", max_depth_dfs)
        print("Ancho máximo del árbol:", max_width_dfs)
        print("Estados del camino solución:")
        for state in path_dfs:
            print(state)
            print("-" * 8)
        export_search_tree(parent_dfs, path_dfs, "dfs_tree.graphml")
    else:
        print("No se encontró solución con DFS.")

    # Best First Search con heurística seleccionable
    heuristics = {
        'misplaced': 'Número de baldosas bien ubicadas',
        'manhattan': 'Distancia Manhattan',
        'euclidean': 'Distancia Euclideana'
    }
    print("\nSeleccione heurística para Best First Search:")
    for key, desc in heuristics.items():
        print(f"  {key}: {desc}")
    selected = input("Ingrese heurística (misplaced/manhattan/euclidean): ").strip().lower()
    if selected not in heuristics:
        print("Heurística no válida. Usando 'misplaced' por defecto.")
        selected = 'misplaced'
    heuristic_fn = get_heuristic(selected)
    print(f"\nBuscando solución con Best First Search usando '{heuristics[selected]}'...")
    path_best, parent_best, max_depth_best, max_width_best = best_first_search(board, heuristic_fn)
    if path_best:
        print(f"\n¡Solución Best First Search encontrada en {len(path_best)-1} movimientos!")
        print("Profundidad del árbol generado:", max_depth_best)
        print("Ancho máximo del árbol:", max_width_best)
        print("Estados del camino solución:")
        for state in path_best:
            print(state)
            print("-" * 8)
        export_search_tree(parent_best, path_best, f"best_first_{selected}_tree.graphml")
    else:
        print("No se encontró solución con Best First Search.")