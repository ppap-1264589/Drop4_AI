class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for i in range(cols)] for j in range(rows)]


    # Cần sửa đổi hàm check_win này cho tối ưu hơn thông qua hai biến r c,
    # hai biến đại diện cho vị trí vừa mới thả token
    def check_win(self, token, r, c):
        # Ngang
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row][col + i] == token for i in range(4)):
                    return True
        # Dọc
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if all(self.grid[row + i][col] == token for i in range(4)):
                    return True
        # Chéo lên
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row - i][col + i] == token for i in range(4)):
                    return True
        # Chéo xuống
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.grid[row + i][col + i] == token for i in range(4)):
                    return True
        return False




    def print_board(self):
        for row in self.grid:
            print("| " + " | ".join(row) + " |")

    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.grid[0][col] == ' '

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.is_valid_move(col)]
    
    def is_full(self):
        return all(self.grid[0][col] != ' ' for col in range(self.cols))
    
    def undo_move(self, col):
        for row in range(self.rows):
            if self.grid[row][col] != ' ':
                self.grid[row][col] = ' '
                return
