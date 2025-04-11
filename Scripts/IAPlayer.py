import Player
from hex_board import HexBoard
from collections import deque
import numpy as np
import random


class IAPlayer(Player.Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.cells_beetween_bridges = {}

    def play(self, board: HexBoard) -> tuple:
        move = None
        if board.player_positions[self.player_id] == []:
            return self.get_center(board)
        key = -1
        if len(self.cells_beetween_bridges) > 1:
            move = self.connect_bridge(board)
        if move is not None:
            return move
        return self.bridges(board) if len(board.player_positions[self.player_id]) < 7 else self.final_steps(board)
                                                                                                            
    def get_center(self, board: HexBoard):
        center = (board.size // 2, board.size // 2)
        if board.board[center[0]][center[1]] == 0:
            return center
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        index = random.randint(0, len(deltas) - 1)
        return (center[0] + deltas[index][0], center[1] + deltas[index][1])
        
    #---------------------------BRIDGES----------------------------------#
    def connect_bridge(self, board: HexBoard):
        best_move = None
        best_score = -np.inf
        for i in self.cells_beetween_bridges.keys():
            if len(self.cells_beetween_bridges[i]) != 2:
                continue
            cell1 = self.cells_beetween_bridges[i][0]
            cell2 = self.cells_beetween_bridges[i][1]
            if board.board[cell1[0]][cell1[1]] == 3 - self.player_id:
                move = cell2 if board.board[cell2[0]][cell2[1]] == 0 else None
                if move is not None:
                    score = self.evaluate(board)
                    if score > best_score:
                        best_score = score
                        best_move = move
            if board.board[cell2[0]][cell2[1]] == 3 - self.player_id:
                move = cell1 if board.board[cell1[0]][cell1[1]] == 0 else None
                if move is not None:
                    score = self.evaluate(board)
                    if score > best_score:
                        best_score = score
                        best_move = move
        #---------------------------------------------------------#
        keys = list(self.cells_beetween_bridges.keys())
        for k in keys:
            if best_move in self.cells_beetween_bridges[k]:
                del self.cells_beetween_bridges[k]
        return best_move
    
    def bridges(self, board: HexBoard):
        best_score = -np.inf
        best_move = None
        selected_pos = None
        directions_bridges = [(-1, -1), (1, 1), (2, -1), (-1, 2), (-2, 1), (1, -2)]
        for r,c in board.player_positions[self.player_id]:
            for dir in directions_bridges:
                nr = r + dir[0]
                nc = c + dir[1]
                if 0 <= nr < board.size and 0 <= nc < board.size and board.board[nr][nc] == 0:
                    score = self.evaluate_bridge(board, (nr, nc))
                    if score >= best_score:
                        best_score = score
                        best_move = (nr, nc)
                        selected_pos = (r,c)
        self.get_bridge_cells(board, selected_pos, best_move)
        return best_move

    def get_bridge_cells(self,board: HexBoard, cell1: tuple, cell2: tuple):
        r1, c1 = cell1
        r2, c2 = cell2
        dx = abs(r1 - r2)
        dy = abs(c1 - c2)
        if dx == 2 and dy == 1:
            b1 = ((r1 + r2) // 2, c1)
            b2 = ((r1 + r2) // 2, c2) 
        if dx == 1 and dy == 1:
            b1 = (r1, c2)
            b2 = (r2, c1)
        if dx == 1 and dy == 2:
            b1 = (r1, (c1 + c2) // 2)
            b2 = (r2, (c1 + c2) // 2)   
        n = len(self.cells_beetween_bridges)
        if n not in self.cells_beetween_bridges.keys():
            self.cells_beetween_bridges[n] = []
        if board.board[b1[0]][b1[1]] == 0:
            self.cells_beetween_bridges[n].append(b1)
        if board.board[b2[0]][b2[1]] == 0:
            self.cells_beetween_bridges[n].append(b2)

    def evaluate_bridge(self, board: HexBoard, cell: tuple):
        r, c = cell
        temp_board = board.clone()
        temp_board.board[r][c] = self.player_id
        my_dist = self.calculate_min_distance_bfs01(board, self.player_id)
        opp_dist = self.calculate_min_distance_bfs01(board, 3 - self.player_id)

        return (opp_dist - my_dist) * 10
    
    #-------------------------MINMAX---------------------------#
    def evaluate(self, board: HexBoard):
        distance = self.calculate_min_distance_bfs01(board, self.player_id) # mi distancia
        if distance == 0:
            return np.inf
        opponent = self.calculate_min_distance_bfs01(board, 3 - self.player_id) # distancia del oponente
        if opponent == 0:
            return -np.inf
        return (opponent - distance) * 10
    
    def calculate_min_distance_bfs01(self, board: HexBoard, player_id: int):
        dist = np.full((board.size, board.size), np.inf)
        dq = deque()
        if player_id == 2:
            start_nodes = [(i, 0) for i in range(board.size) if board.board[i][0] != 3 - player_id]
        else:
            start_nodes = [(0, j) for j in range(board.size) if board.board[0][j] != 3 - player_id]
        
        for node in start_nodes:
            init_cost = 0 if board.board[node[0]][node[1]] == player_id else 1
            dist[node[0]][node[1]] = init_cost
            if init_cost == 0:
                dq.appendleft(node)
            else:
                dq.append(node)
        deltas = [(-1, 0), (1, 0), (-1, 1), (1, -1), (0, -1), (0, 1)] if self.player_id == 2 else [(0, -1), (0, 1), (-1, 1), (1, -1), (-1, 0), (1, 0)]
        while dq:
            r, c = dq.popleft()
            for dr, dc in deltas:
                nr, nc = r + dr, c + dc
                if 0 <= nr < board.size and 0 <= nc < board.size and board.board[nr][nc] != 3 - player_id:
                    new_cost = dist[r][c] + (0 if board.board[nr][nc] == player_id else 1)
                    if new_cost < dist[nr][nc]:
                        dist[nr][nc] = new_cost
                        if new_cost == 0:
                            dq.appendleft((nr, nc))
                        else:
                            dq.append((nr, nc))
        if player_id == 2:
            target = [(i, board.size-1) for i in range(board.size)]
        else :
            target = [(board.size-1, j) for j in range(board.size)]

        min_distance = min(dist[x, y] for (x, y) in target if not np.isinf(dist[x, y]))
        return min_distance if not np.isinf(min_distance) else 1000
    
    def find_critical_move(self, board: HexBoard):
        for mov in self.best_possibles_moves(board):
            new_board = board.clone()
            new_board.place_piece(mov[0], mov[1], self.player_id) 
            if self.calculate_min_distance_bfs01(board, self.player_id) == 0:
                return mov
        for mov in self.best_possibles_moves(board):
            new_board = board.clone()
            new_board.place_piece(mov[0], mov[1],3 - self.player_id)
            if self.calculate_min_distance_bfs01(board, 3 - self.player_id) == 0:
                return mov
    
    def max_function(self, board: HexBoard, depth: int,bool, alpha: float, beta: float):
        if depth == 0 or board.check_connection(self.player_id):
            return self.evaluate(board)
        best_score = -np.inf
        for mov in self.best_possibles_moves(board):
            new_board = board.clone()
            new_board.board[mov[0]][mov[1]] = self.player_id
            score = self.min_function(new_board, depth - 1, alpha, beta)
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    
    def min_function(self, board: HexBoard, depth: int, alpha: float, beta: float):
        if depth == 0 or board.check_connection(3 - self.player_id):
            return self.evaluate(board)
        best_score = np.inf
        for mov in self.best_possibles_moves(board):
            new_board = board.clone()
            new_board.board[mov[0]][mov[1]] = 3 - self.player_id
            score = self.max_function(new_board, depth - 1, True, alpha, beta)
            best_score = min(score, best_score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score
    
    def final_steps(self, board: HexBoard):
        critical_move = self.find_critical_move(board)
        if critical_move:
            return critical_move
        best_score = -np.inf
        best_move = None
        alpha = -np.inf
        beta = np.inf
        for mov in self.best_possibles_moves(board):
            new_board = board.clone()
            new_board.place_piece(mov[0], mov[1], self.player_id)
            score = self.min_function(new_board, 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = mov
                alpha = max(alpha, score)
        return best_move
    
    def best_possibles_moves(self, board: HexBoard):
        empty = []
        deltas = [(-1, 0), (1, 0), (-1, 1), (1, -1), (0, -1), (0, 1)] if self.player_id == 2 else [(0, -1), (0, 1), (-1, 1), (1, -1), (-1, 0), (1, 0)]
        for cells in board.player_positions[self.player_id]:
            for dx, dy in deltas:
                x, y = cells[0] + dx, cells[1] + dy
                if 0 <= x < board.size and 0 <= y < board.size and board.board[x][y] == 0:
                    empty.append((x, y))
        return list(empty) if empty else self.best_possibles_moves()