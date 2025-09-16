from collections import deque

def bfs_search(initial_state):
    """
    Realiza una búsqueda BFS en el 8-tile desde initial_state hasta el goal.
    Retorna el camino (lista de estados) si lo encuentra, o None si no hay solución.
    """
    visited = set()
    queue = deque()
    parent = {}  # Para reconstruir el camino

    queue.append(initial_state)
    visited.add(initial_state)
    parent[initial_state] = None

    while queue:
        current = queue.popleft()
        if current.is_goal():
            # Reconstruir camino
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for neighbor in current.get_successors():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    return None