from eight_tile.eight_tile import EightTile
from search_algorithms.bfs import bfs_search

if __name__ == "__main__":
    initial = [1,2,3,4,5,6,0,7,8]
    goal = [3, 7, 0, 5, 1, 8, 4, 2, 6]

    board = EightTile(initial, goal)
    print("Estado inicial:")
    print(board)
    print("\nBuscando solución con BFS...")

    path = bfs_search(board)
    if path:
        print(f"\n¡Solución encontrada en {len(path)-1} movimientos!")
        print("Estados:")
        for state in path:
            print(state)
            print("-" * 8)
    else:
        print("No se encontró solución.")