from Drop4.Board import Board
from Drop4.Player import Player
from Drop4.Computer import Computer

class Game:
    def __init__(self, rows, cols, depth_search, player_mark, computer_mark, player_first):
        if player_first:
            self.turn = player_mark
        else:
            self.turn = computer_mark

        self.found_winner = None
        self.board = Board(rows, cols)
        self.player = Player(player_mark)
        self.computer = Computer(computer_mark, depth_search, player_mark)  # Truyền opponent_token
        self.player_mark = player_mark
        self.computer_mark = computer_mark








    def print_board(self):
        self.board.print_board()

    def is_full(self):
        return self.board.is_full()
    
    def is_valid_move(self, col):
        return self.board.is_valid_move(col)
    
    def check_win(self, token, r, c):
        return self.board.check_win(token, r, c)
    # Một số hàm chuyển hướng cho lớp board làm việc




    def play_game(self):
        while not self.is_full() and not self.found_winner:
            self.print_board()

            if self.turn == self.player_mark:  # Lượt player
                input_col = int(input("Chọn cột (0-6): "))
                while not self.is_valid_move(input_col):
                    input_col = int(input("Cột không hợp lệ, chọn lại: "))
                input_row = self.player.make_move(self.board, input_col)
                if self.check_win(self.player_mark, input_row, input_col):
                    self.found_winner = self.player_mark

            else:  # Lượt computer
                input_col = self.computer.choose_best_move(self.board)  # Chỉ gọi choose_best_move, ẩn chi tiết
                print(f"Máy chọn cột {input_col}")
                input_row = self.computer.make_move(self.board, input_col)
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