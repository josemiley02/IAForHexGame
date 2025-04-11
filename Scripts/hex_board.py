import copy
from collections import deque
class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0] * size for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador

    def clone(self) -> "HexBoard":
            return copy.copy(self)
        
    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] == 0:
            self.board[row][col] = player_id
            self.player_positions[player_id].add((row, col))
            return True
        return False
    
    def get_possible_moves(self) -> list:
        """Devuelve una lista con las casillas vacias"""
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
    
    def check_connection(self, player_id: int) -> bool:
        """Verifica si hay una conexión de fichas del jugador en el tablero"""
        size = self.size
        visited = set()
        queue = deque()
        if player_id == 1:  # Conecta izquierda (columna 0) -> derecha (columna size-1)
            start_nodes = [(i, 0) for i in range(size) if self.board[i][0] == player_id]
            target_col = size - 1
        else:  # Conecta arriba (fila 0) -> abajo (fila size-1)
            start_nodes = [(0, j) for j in range(size) if self.board[0][j] == player_id]
            target_row = size - 1
        for node in start_nodes:
            queue.append(node)
            visited.add(node)
        directions = [ (-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1) ]
        while queue:
            x, y = queue.popleft()
            if (player_id == 1 and y == target_col) or (player_id == 2 and x == target_row):
                return True
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < size and 0 <= ny < size and self.board[nx][ny] == player_id and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return False