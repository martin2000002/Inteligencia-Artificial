import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from eight_tile.eight_tile import EightTile
from search_algorithms.breadth_first_search import breadth_first_search
from search_algorithms.depth_first_search import depth_first_search
from search_algorithms.best_first_search import best_first_search
from visualization.generator.graphml_export import export_search_tree
from heuristics.misplaced import misplaced_tiles
from heuristics.manhattan import manhattan_distance
from heuristics.euclidean import euclidean_distance
from shared.format.console import print_boxed_title, subtitle_block

if __name__ == "__main__":
    initial = [5,4,2,3,0,8,1,6,7]
    goal = [5,2,8,3,0,7,1,4,6]

    board = EightTile(initial, goal)
    print("Estado inicial:")
    print(board)
    print("\nEstado objetivo:")
    print(EightTile(goal, goal))


    SUMMARY_TEMPLATE = "Movimientos para solución = {moves}\nProfundidad = {depth}\nAncho = {width}\nEstados visitados = {visited}"
    TITLE_TEMPLATE = "{method}:"
    NO_SOLUTION_MSG = "No se encontró solución."

    def _boxed(method_name: str):
        title = TITLE_TEMPLATE.format(method=method_name)
        print_boxed_title(title)

    _boxed("Breadth First Search")
    with subtitle_block():
        path_bfs, parent_bfs, max_depth_bfs, max_width_bfs, visited_bfs = breadth_first_search(board)
        if path_bfs:
            print(SUMMARY_TEMPLATE.format(moves=len(path_bfs)-1, depth=max_depth_bfs, width=max_width_bfs, visited=visited_bfs))
            export_search_tree(parent_bfs, path_bfs, "breadth_first_search.graphml")
        else:
            print(NO_SOLUTION_MSG)

    _boxed("Depth First Search")
    with subtitle_block():
        path_dfs, parent_dfs, max_depth_dfs, max_width_dfs, visited_dfs = depth_first_search(board)
        if path_dfs:
            print(SUMMARY_TEMPLATE.format(moves=len(path_dfs)-1, depth=max_depth_dfs, width=max_width_dfs, visited=visited_dfs))
            export_search_tree(parent_dfs, path_dfs, "depth_first_search.graphml")
        else:
            print(NO_SOLUTION_MSG)

    heuristics = [
        ("Número de baldosas bien ubicadas", misplaced_tiles, "best_first_search_misplaced.graphml"),
        ("Distancia Manhattan", manhattan_distance, "best_first_search_manhattan.graphml"),
        ("Distancia Euclideana", euclidean_distance, "best_first_search_euclidean.graphml"),
    ]
    for desc, heuristic_fn, out_name in heuristics:
        _boxed(f"Best First Search ({desc})")
        with subtitle_block():
            path_bf, parent_bf, max_depth_bf, max_width_bf, visited_bf = best_first_search(board, heuristic=heuristic_fn)
            if path_bf:
                print(SUMMARY_TEMPLATE.format(moves=len(path_bf)-1, depth=max_depth_bf, width=max_width_bf, visited=visited_bf))
                export_search_tree(parent_bf, path_bf, out_name)
            else:
                print(NO_SOLUTION_MSG)
    print()