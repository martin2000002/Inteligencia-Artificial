from queue import PriorityQueue
from typing import Callable, Tuple, Dict, List, Optional
from eight_tile.eight_tile import EightTile
import importlib

def best_first_search(initial_state: EightTile, heuristic: Callable[[EightTile], float]) -> Tuple[List[EightTile], Dict[EightTile, Optional[EightTile]], int, int, int]:
    import itertools
    visited = set()
    parent = {}
    level = {}
    pq = PriorityQueue()
    counter = itertools.count()
    pq.put((heuristic(initial_state), next(counter), initial_state))
    visited.add(initial_state)
    parent[initial_state] = None
    level[initial_state] = 0
    from collections import defaultdict
    level_count = defaultdict(int)
    level_count[0] = 1
    solution_found = False
    goal_state = None
    while not pq.empty():
        _, _, current = pq.get()
        current_level = level[current]
        if current.is_goal():
            solution_found = True
            goal_state = current
            break
        for neighbor in current.get_successors():
            if neighbor not in visited:
                visited.add(neighbor)
                pq.put((heuristic(neighbor), next(counter), neighbor))
                parent[neighbor] = current
                level[neighbor] = current_level + 1
                level_count[current_level + 1] += 1
    max_depth = max(level.values()) if level else 0
    max_width = max(level_count.values()) if level_count else 0
    visited_count = len(visited)
    path = []
    if solution_found:
        current = goal_state
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path, parent, max_depth, max_width, visited_count

# Diccionario para seleccionar heurística fácilmente
def get_heuristic(name: str) -> Callable[[EightTile], float]:
    """Carga la heurística de forma perezosa desde el paquete heuristics.

    Los módulos disponibles: heuristics.misplaced, heuristics.manhattan, heuristics.euclidean
    Cada módulo exporta una función con nombre *_distance o misplaced_tiles según corresponda.
    """
    module_map = {
        'misplaced': ('heuristics.misplaced', 'misplaced_tiles'),
        'manhattan': ('heuristics.manhattan', 'manhattan_distance'),
        'euclidean': ('heuristics.euclidean', 'euclidean_distance'),
    }
    if name not in module_map:
        raise ValueError('Heurística no reconocida')
    module_name, func_name = module_map[name]
    mod = importlib.import_module(module_name)
    return getattr(mod, func_name)
