from queue import PriorityQueue
from typing import Callable, Tuple, Dict, List, Optional
from eight_tile.eight_tile import EightTile

# Heurística por defecto
from heuristics.misplaced import misplaced_tiles as default_heuristic

def best_first_search(initial_state: EightTile, heuristic: Optional[Callable[[EightTile], float]] = None) -> Tuple[List[EightTile], Dict[EightTile, Optional[EightTile]], int, int, int]:
    import itertools
    if heuristic is None:
        heuristic = default_heuristic
    visited = set()
    parent: Dict[EightTile, Optional[EightTile]] = {}
    level: Dict[EightTile, int] = {}
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
    goal_state: Optional[EightTile] = None
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
    path: List[EightTile] = []
    if solution_found and goal_state is not None:
        current: Optional[EightTile] = goal_state
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path, parent, max_depth, max_width, visited_count
