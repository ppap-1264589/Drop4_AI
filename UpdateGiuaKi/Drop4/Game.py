from Drop4.Board import Board
from Drop4.Computer import Computer

class Game:
    def __init__(self, rows, cols, depth_search, player_mark, computer_mark, player_first):
        self.turn = player_mark if player_first else computer_mark
        self.found_winner = None
        self.board = Board(rows, cols)
        self.computer = Computer(computer_mark, player_mark, depth_search)
        self.player_mark = player_mark
        self.computer_mark = computer_mark
    # Khởi tạo các tham số xác định cho trò chơi

    def print_board(self):
        self.board.print_board()

    def is_full(self):
        return self.board.is_full()
    
    def is_valid_move(self, col):
        return self.board.is_valid_move(col)
    
    def check_win(self, token, r, c):
        return self.board.check_win(token, r, c)
    





    def play_game(self):
        while not self.is_full() and not self.found_winner:
            self.print_board()

            if self.turn == self.player_mark:  # Lượt player
                input_col = int(input(f"Chọn cột (1 - {self.board.cols}): ")) - 1
                # Người dùng nhập input, map 1-based sang 0-based
                while not self.is_valid_move(input_col):
                    input_col = int(input(f"Cột không hợp lệ, chọn lại (1 - {self.board.cols}): ")) - 1
                input_row = self.board.drop_move(input_col, self.player_mark)
                if self.check_win(self.player_mark, input_row, input_col):
                    self.found_winner = self.player_mark

            else:  # Lượt computer
                input_col = self.computer.choose_best_move(self.board)
                print(f"Máy chọn cột {input_col + 1}")
                input_row = self.board.drop_move(input_col, self.computer_mark)
                if self.check_win(self.computer_mark, input_row, input_col):
                    self.found_winner = self.computer_mark

            self.turn = self.computer_mark if self.turn == self.player_mark else self.player_mark

        self.board.print_board()
        if self.found_winner == self.player_mark:
            print("Bạn thắng!")
        elif self.found_winner == self.computer_mark:
            print("Máy thắng!")
        else:
            print("Hòa!")
    # Luồng logic chơi game chính