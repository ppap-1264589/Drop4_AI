class Player:
    def __init__(self, token):
        self.token = token
        pass

    def make_move(self, board, col):
        for r in range(board.rows - 1, -1, -1):
            if board.grid[r][col] == ' ':
                board.grid[r][col] = self.token
                return r
        return -1