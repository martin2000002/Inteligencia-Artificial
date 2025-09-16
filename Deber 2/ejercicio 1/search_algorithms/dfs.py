def dfs_search(initial_state, max_depth=50):
    visited = set()
    stack = []
    parent = {}
    level = {}
    max_width = 0
    stack.append((initial_state, 0))
    visited.add(initial_state)
    parent[initial_state] = None
    level[initial_state] = 0

    # Para ancho por nivel
    from collections import defaultdict
    level_count = defaultdict(int)
    level_count[0] = 1

    solution_found = False
    goal_state = None

    while stack:
        current, current_level = stack.pop()
        if current.is_goal():
            solution_found = True
            goal_state = current
            break
        if current_level < max_depth:
            for neighbor in current.get_successors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, current_level + 1))
                    parent[neighbor] = current
                    level[neighbor] = current_level + 1
                    level_count[current_level + 1] += 1

    max_depth_result = max(level.values()) if level else 0
    max_width = max(level_count.values()) if level_count else 0
    visited_count = len(visited)

    # Reconstruir camino
    path = []
    if solution_found:
        current = goal_state
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()

    return path, parent, max_depth_result, max_width, visited_count
