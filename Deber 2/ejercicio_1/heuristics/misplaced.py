from eight_tile.eight_tile import EightTile

def misplaced_tiles(state: EightTile) -> int:
    """Número de baldosas mal colocadas (ignora el espacio en blanco)."""
    return sum(1 for i, tile in enumerate(state.tiles) if tile != 0 and tile != state.goal[i])
