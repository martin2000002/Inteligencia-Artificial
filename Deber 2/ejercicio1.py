from typing import List, Tuple, Optional

class EightTile:
    def __init__(self, tiles: Optional[List[int]] = None):
        # Si no se pasa un tablero, crea el tablero ordenado por defecto
        self.tiles = tiles if tiles is not None else [1,2,3,4,5,6,7,8,0]
    
    def __str__(self):
        # Representación bonita del tablero
        rows = [self.tiles[i*3:(i+1)*3] for i in range(3)]
        return "\n".join(
            " ".join(str(val) if val != 0 else ' ' for val in row)
            for row in rows
        )
    
    def find_blank(self) -> Tuple[int, int]:
        idx = self.tiles.index(0)
        return idx // 3, idx % 3
    
    def move(self, direction: str) -> bool:
        # Mueve el espacio en blanco en la dirección dada si es posible
        # Direcciones válidas: 'up', 'down', 'left', 'right'
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
            return False
        
        if 0 <= target_row < 3 and 0 <= target_col < 3:
            blank_idx = row * 3 + col
            target_idx = target_row * 3 + target_col
            # Intercambiar el espacio en blanco con la baldosa objetivo
            self.tiles[blank_idx], self.tiles[target_idx] = self.tiles[target_idx], self.tiles[blank_idx]
            return True
        return False

    def copy(self):
        return EightTile(self.tiles.copy())

    def is_goal(self) -> bool:
        return self.tiles == [1,2,3,4,5,6,7,8,0]

# Ejemplo de uso
if __name__ == "__main__":
    board = EightTile([1,2,0,4,5,6,7,3,8])
    print("Estado inicial:")
    print(board)
    print("\nMoviendo derecha:")
    board.move('right')
    print(board)
    print("\nMoviendo abajo:")
    board.move('down')
    print(board)
    print("\nMoviendo izquierda:")
    board.move('left')
    print(board)