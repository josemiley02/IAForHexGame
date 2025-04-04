class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = [[0] * size for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador
        def clone(self) -> HexBoard:
            return self
    
    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row, col] == 0:
            self.board[row, col] = player_id
            return True
        return False

    def get_possible_moves(self) -> list:
        """Devuelve una lista con las casillas vacias"""
        empty_spaces = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i,j] == 0:
                    empty_spaces.append([i,j])
        return empty_spaces
    
    def check_connection(self, player_id: int) -> bool:
        """Verifica si hay una conexión de fichas del jugador en el tablero"""
        movments = [[0,1],[0,-1],[1,0],[-1,0],[1,-1],[-1,1]]
        if player_id is 1:
            for j in range(self.size):
                visited = [[False for _ in range(self.board)] for _ in range(self.board)]
                if self.board[0,j] == 1:
                    if self.find_the_other_size(0,j, player_id, visited, movments):
                        return True
                if self.board[self.size - 1, j] == 1:
                    if self.find_the_other_size(self.size - 1,j, player_id, visited, movments):
                        return True
        else:
            for i in range(self.size):
                visited = [[False for _ in range(self.board)] for _ in range(self.board)]
                if self.board[i,0] == 2:
                    if self.find_the_other_size(i, 0, player_id, visited, movments):
                        return True
                if self.board[i, self.size - 1] == 2:
                    if self.find_the_other_size(i, self.size-1, player_id, visited, movments):
                        return True
        return False

    def find_the_other_size(self ,star_row: int, star_col: int, value: int, visited: list, movments: list) -> bool:
        """Chequea la conexion de un lado del tablero a otro"""
        visited[star_row, star_col] = True
        for mov in movments:
            new_row = star_row + mov[0][1]
            new_col = star_col + mov[0][1]
            if 0 <= new_row < self.size and 0 <= new_col < self.size and self.board[new_row, new_col] == value and not visited[new_row, new_col]:
                if self.find_the_other_size(new_row, new_col, value, visited):
                    return True
        return False