# Estado como tupla (F, W, G, C): 0 = izquierda, 1 = derecha
START = (0, 0, 0, 0)
GOAL = (1, 1, 1, 1)
NAMES_SHORT = ['F', 'W', 'G', 'C']
NAMES_ES = ['Granjero', 'Lobo', 'Cabra', 'Col']

def is_safe(state):
    F, W, G, C = state
    # Si lobo y cabra se quedan solos en una orilla sin el granjero -> inválido
    if W == G and W != F:
        return False
    # Si cabra y col se quedan solas en una orilla sin el granjero -> inválido
    if G == C and G != F:
        return False
    return True

def neighbors(state):
    F, W, G, C = state
    # Movimientos: granjero solo o con uno que esté en su misma orilla
    candidates = [None, 'W', 'G', 'C']
    idx = {'F': 0, 'W': 1, 'G': 2, 'C': 3}
    for carry in candidates:
        # Debe estar en la misma orilla que el granjero
        if carry is not None:
            if state[idx[carry]] != F:
                continue
        new_state = list(state)
        # Mueve al granjero
        new_state[0] = 1 - new_state[0]
        # Mueve el que lleva (si aplica)
        if carry is not None:
            new_state[idx[carry]] = 1 - new_state[idx[carry]]
        new_state = tuple(new_state)
        if is_safe(new_state):
            yield new_state, carry

# --- Backtracking (DFS) en lugar de BFS ---

def dfs_backtracking(start: tuple = START, goal: tuple = GOAL):
    """Retorna una ruta desde start a goal usando backtracking (DFS).
    Formato de salida: lista de (state, move), comenzando con (start, None).
    Nota: No garantiza mínimos pasos.
    """
    visited = {start}
    path = [(start, None)]
    return _dfs(start, goal, visited, path)

def _dfs(state: tuple, goal: tuple, visited: set, path: list):
    if state == goal:
        return path
    for ns, carry in neighbors(state):
        if ns in visited:
            continue
        visited.add(ns)
        res = _dfs(ns, goal, visited, path + [(ns, carry)])
        if res is not None:
            return res
        visited.remove(ns)
    return None

# --- Salida y utilidades ---

def format_banks(state):
    left = [NAMES_ES[i] for i, side in enumerate(state) if side == 0]
    right = [NAMES_ES[i] for i, side in enumerate(state) if side == 1]
    def fmt(xs): return ', '.join(xs) if xs else '—'
    return f"IZQ: {fmt(left)} | DER: {fmt(right)}"

def describe_move(prev, carry):
    F_prev = prev[0]
    direction = "izquierda -> derecha" if F_prev == 0 else "izquierda <- derecha"
    if carry is None:
        return f"El Granjero cruza solo ({direction})"
    name = {'W': 'Lobo', 'G': 'Cabra', 'C': 'Col'}[carry]
    return f"El Granjero lleva la {name} ({direction})"

def main():
    solution = dfs_backtracking()
    if not solution:
        print("No se encontró solución.")
        return
    print("Solución (backtracking):")
    # Imprime estado inicial
    print(f"Paso 0: Estado inicial")
    print(format_banks(solution[0][0]))
    for i in range(1, len(solution)):
        prev_state = solution[i-1][0]
        state, carry = solution[i]
        print(f"\nPaso {i}: {describe_move(prev_state, carry)}")
        print(format_banks(state))
    print(f"\nTotal de pasos: {len(solution)-1}")

if __name__ == "__main__":
    main()