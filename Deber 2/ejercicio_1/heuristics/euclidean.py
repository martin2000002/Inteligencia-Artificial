from eight_tile.eight_tile import EightTile

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
