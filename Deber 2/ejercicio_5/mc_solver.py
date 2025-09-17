# Problema de los Misioneros y Canibales - Backtracking (DFS)
# Estado: (M_izq, C_izq, Bote) con Bote: 0=izquierda, 1=derecha. Total: 3 y 3.

START = (3, 3, 0)
GOAL = (0, 0, 1)

MOVES = [  # (misioneros, canibales) que se suben al bote
    (2, 0), (1, 0),
    (0, 2), (0, 1),
    (1, 1),
]


def is_safe(m_left: int, c_left: int) -> bool:
    # Rango valido
    if not (0 <= m_left <= 3 and 0 <= c_left <= 3):
        return False
    # Izquierda
    if m_left > 0 and c_left > m_left:
        return False
    # Derecha
    m_right = 3 - m_left
    c_right = 3 - c_left
    if m_right > 0 and c_right > m_right:
        return False
    return True


def neighbors(state):
    m_left, c_left, boat = state
    for m, c in MOVES:
        # El bote debe llevar max 2 y al menos 1 persona (siempre cierto por nuestra lista)
        if boat == 0:
            # Mover de izquierda a derecha
            nm, nc = m_left - m, c_left - c
        else:
            # Mover de derecha a izquierda
            nm, nc = m_left + m, c_left + c
        if not is_safe(nm, nc):
            continue
        yield (nm, nc, 1 - boat), (m, c)


# --- Backtracking (DFS) ---

def dfs_backtracking(start=START, goal=GOAL):
    visited = {start}
    path = [(start, None)]  # (estado, movimiento)
    return _dfs(start, goal, visited, path)


def _dfs(state, goal, visited, path):
    if state == goal:
        return path
    for ns, move in neighbors(state):
        if ns in visited:
            continue
        visited.add(ns)
        res = _dfs(ns, goal, visited, path + [(ns, move)])
        if res is not None:
            return res
        visited.remove(ns)
    return None


# --- Salida ---

def bank_str(m, c):
    return f"{m}M, {c}C" if (m or c) else "-"


def format_state(state):
    m_left, c_left, boat = state
    m_right, c_right = 3 - m_left, 3 - c_left
    side = "IZQ" if boat == 0 else "DER"
    return f"IZQ: {bank_str(m_left, c_left)} | DER: {bank_str(m_right, c_right)} | Bote: {side}"


def describe_move(prev, move):
    if move is None:
        return "Estado inicial"
    m, c = move
    boat = prev[2]
    direction = "izquierda -> derecha" if boat == 0 else "izquierda <- derecha"
    parts = []
    if m:
        parts.append(f"{m} misionero(s)")
    if c:
        parts.append(f"{c} canibal(es)")
    who = " y ".join(parts)
    return f"El bote lleva {who} ({direction})"


def main():
    sol = dfs_backtracking()
    if not sol:
        print("No se encontró solución.")
        return
    print("Solución (backtracking):")
    print("Paso 0: Estado inicial")
    print(format_state(sol[0][0]))
    for i in range(1, len(sol)):
        prev_state = sol[i-1][0]
        state, move = sol[i]
        print(f"\nPaso {i}: {describe_move(prev_state, move)}")
        print(format_state(state))
    print(f"\nTotal de pasos: {len(sol)-1}")


if __name__ == "__main__":
    main()
