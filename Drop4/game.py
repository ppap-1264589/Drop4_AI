from .board import Board
from .minimax import best_move

class ConnectFour:
    def __init__(self):
        self.board = Board()  # Khởi tạo đối tượng Board
        self.turn = 'X'  # 'X' là người chơi, 'O' là máy
        self.winner = None

    def play(self):
        depth = 4  # Độ sâu minimax
        while not self.winner and not self.board.is_full():
            self.board.print_board()  # Gọi print_board từ Board
            if self.turn == 'X':  # Lượt người chơi
                col = int(input("Chọn cột (0-6): "))
                while not self.board.is_valid_move(col):
                    col = int(input("Cột không hợp lệ, chọn lại: "))
                self.board.make_move(col, 'X')  # Gọi make_move từ Board
                if self.board.check_win('X'):
                    self.winner = 'X'
            else:  # Lượt máy
                col = best_move(self.board, depth)  # Gọi best_move từ minimax.py
                print(f"Máy chọn cột {col}")
                self.board.make_move(col, 'O')  # Gọi make_move từ Board
                if self.board.check_win('O'):
                    self.winner = 'O'
            self.turn = 'O' if self.turn == 'X' else 'X'

        self.board.print_board()
        if self.winner == 'X':
            print("Bạn thắng!")
        elif self.winner == 'O':
            print("Máy thắng!")
        else:
            print("Hòa!")