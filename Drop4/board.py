class Board:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

    def print_board(self):
        # Code print_board ở đây
        pass

    def is_valid_move(self, col):
        # Code is_valid_move
        pass

    # Các hàm khác: make_move, undo_move, check_win, is_full, get_valid_moves