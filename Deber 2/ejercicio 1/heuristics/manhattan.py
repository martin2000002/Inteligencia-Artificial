from eight_tile.eight_tile import EightTile

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
