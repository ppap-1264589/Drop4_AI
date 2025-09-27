class Board:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print(' ' + ' '.join(str(i) for i in range(self.cols)))

    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.board[0][col] == ' '

    def make_move(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = player
                return True
        return False

    def undo_move(self, col):
        for row in range(self.rows):
            if self.board[row][col] != ' ':
                self.board[row][col] = ' '
                return

    def check_win(self, player):
        # Ngang
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
        # Dọc
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
        # Chéo lên
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True
        # Chéo xuống
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
        return False

    def is_full(self):
        return all(self.board[0][col] != ' ' for col in range(self.cols))

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.is_valid_move(col)]