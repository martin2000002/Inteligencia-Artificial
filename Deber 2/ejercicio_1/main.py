from eight_tile.eight_tile import EightTile
from search_algorithms.breadth_first_search import breadth_first_search
from search_algorithms.depth_first_search import depth_first_search
from search_algorithms.best_first_search import best_first_search, get_heuristic
from visualization.generator.graphml_export import export_search_tree

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

    def print_boxed_title(method_name: str):
        title = TITLE_TEMPLATE.format(method=method_name)
        sep = '-' * len(title)
        print('\n' + sep)
        print(title)
        print(sep)

    print_boxed_title("Breadth First Search")
    path_bfs, parent_bfs, max_depth_bfs, max_width_bfs, visited_bfs = breadth_first_search(board)
    if path_bfs:
        print(SUMMARY_TEMPLATE.format(moves=len(path_bfs)-1, depth=max_depth_bfs, width=max_width_bfs, visited=visited_bfs))
        export_search_tree(parent_bfs, path_bfs, "breadth_first_search.graphml")
    else:
        print(NO_SOLUTION_MSG)

    print_boxed_title("Depth First Search")
    path_dfs, parent_dfs, max_depth_dfs, max_width_dfs, visited_dfs = depth_first_search(board)
    if path_dfs:
        print(SUMMARY_TEMPLATE.format(moves=len(path_dfs)-1, depth=max_depth_dfs, width=max_width_dfs, visited=visited_dfs))
        export_search_tree(parent_dfs, path_dfs, "depth_first_search.graphml")
    else:
        print(NO_SOLUTION_MSG)

    heuristics = {
        'misplaced': 'Número de baldosas bien ubicadas',
        'manhattan': 'Distancia Manhattan',
        'euclidean': 'Distancia Euclideana'
    }
    for key, desc in heuristics.items():
        print_boxed_title(f"Best First Search ({desc})")
        heuristic_fn = get_heuristic(key)
        path_bf, parent_bf, max_depth_bf, max_width_bf, visited_bf = best_first_search(board, heuristic_fn)
        if path_bf:
            print(SUMMARY_TEMPLATE.format(moves=len(path_bf)-1, depth=max_depth_bf, width=max_width_bf, visited=visited_bf))
            export_search_tree(parent_bf, path_bf, f"best_first_search_{key}.graphml")
        else:
            print(NO_SOLUTION_MSG)
    print()