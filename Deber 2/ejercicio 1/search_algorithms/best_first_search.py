from queue import PriorityQueue
from typing import Callable, Tuple, Dict, List, Optional
from eight_tile.eight_tile import EightTile

def misplaced_tiles(state: EightTile) -> int:
    return sum(1 for i, tile in enumerate(state.tiles) if tile != 0 and tile != state.goal[i])

def manhattan_distance(state: EightTile) -> int:
    distance = 0
    for idx, tile in enumerate(state.tiles):
        if tile == 0:
            continue
        goal_idx = state.goal.index(tile)
        x1, y1 = divmod(idx, 3)
        x2, y2 = divmod(goal_idx, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def euclidean_distance(state: EightTile) -> float:
    distance = 0.0
    for idx, tile in enumerate(state.tiles):
        if tile == 0:
            continue
        goal_idx = state.goal.index(tile)
        x1, y1 = divmod(idx, 3)
        x2, y2 = divmod(goal_idx, 3)
        distance += ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance

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
    if name == 'misplaced':
        return misplaced_tiles
    elif name == 'manhattan':
        return manhattan_distance
    elif name == 'euclidean':
        return euclidean_distance
    else:
        raise ValueError('Heurística no reconocida')
