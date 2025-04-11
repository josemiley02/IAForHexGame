import Scripts.hex_board as hex_board

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: hex_board.HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")