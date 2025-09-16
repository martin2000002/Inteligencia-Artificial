from typing import List, Tuple, Optional

class EightTile:
    def __init__(self, tiles: Optional[List[int]] = None, goal: Optional[List[int]] = None):
        self.tiles = tiles if tiles is not None else [1,2,3,4,5,6,7,8,0]
        self.goal = goal if goal is not None else [1,2,3,4,5,6,7,8,0]
    
    def __str__(self):
        rows = [self.tiles[i*3:(i+1)*3] for i in range(3)]
        return "\n".join(
            " ".join(str(val) if val != 0 else ' ' for val in row)
            for row in rows
        )
    
    def find_blank(self) -> Tuple[int, int]:
        idx = self.tiles.index(0)
        return idx // 3, idx % 3
    
    def move(self, direction: str) -> Optional['EightTile']:
        row, col = self.find_blank()
        target_row, target_col = row, col
        if direction == 'up':
            target_row -= 1
        elif direction == 'down':
            target_row += 1
        elif direction == 'left':
            target_col -= 1
        elif direction == 'right':
            target_col += 1
        else:
            return None
        
        if 0 <= target_row < 3 and 0 <= target_col < 3:
            blank_idx = row * 3 + col
            target_idx = target_row * 3 + target_col
            new_tiles = self.tiles.copy()
            new_tiles[blank_idx], new_tiles[target_idx] = new_tiles[target_idx], new_tiles[blank_idx]
            return EightTile(new_tiles, self.goal)
        return None

    def get_successors(self) -> List['EightTile']:
        successors = []
        for direction in ['up', 'down', 'left', 'right']:
            new_state = self.move(direction)
            if new_state:
                successors.append(new_state)
        return successors

    def is_goal(self) -> bool:
        return self.tiles == self.goal

    def set_goal(self, goal: List[int]):
        self.goal = goal.copy()

    def __eq__(self, other):
        return isinstance(other, EightTile) and self.tiles == other.tiles

    def __hash__(self):
        return hash(tuple(self.tiles))