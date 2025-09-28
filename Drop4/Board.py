class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for i in range(cols)] for j in range(rows)]

    def check_win(self, token, r, c):
        # Chỉ kiểm tra 4 hướng từ vị trí (r, c)
        directions = [
            (0, 1),   # Ngang (phải)
            (1, 0),   # Dọc (xuống)
            (1, 1),   # Chéo xuống-phải
            (1, -1)   # Chéo xuống-trái
        ]
        for dr, dc in directions:
            count = 1  # Bắt đầu từ token tại (r, c)
            # Đếm về phía trước
            for i in range(1, 4):
                nr, nc = r + i * dr, c + i * dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == token:
                    count += 1
                else:
                    break
            # Đếm về phía ngược
            for i in range(1, 4):
                nr, nc = r - i * dr, c - i * dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == token:
                    count += 1
                else:
                    break
            if count >= 4:
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
    
    def drop_move(self, col, token):
        for r in range(self.rows - 1, -1, -1):
            if self.grid[r][col] == ' ':
                self.grid[r][col] = token
                return r
        return -1  # Invalid if full
    
    def undo_move(self, col):
        for row in range(self.rows):
            if self.grid[row][col] != ' ':
                self.grid[row][col] = ' '
                return