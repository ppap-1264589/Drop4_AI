import sys

class Computer:
    def __init__(self, token, depth_search, opponent_token):
        self.token = token
        self.depth_search = depth_search
        self.opponent_token = opponent_token  # Token của player để đánh giá

    def make_move(self, board, col):
        for r in range(board.rows - 1, -1, -1):
            if board.grid[r][col] == ' ':
                board.grid[r][col] = self.token
                return r
        return -1

    def choose_best_move(self, board):
        # Phương thức public để chọn move tốt nhất (ẩn đi chi tiết minimax)
        best_score = sys.maxsize
        best_col = None
        alpha = -sys.maxsize
        beta = sys.maxsize
        for col in board.get_valid_moves():
            row = self.make_move(board, col)  # Thử move
            score = self._minimax(board, self.depth_search - 1, alpha, beta, True, row, col)
            board.undo_move(col)  # Undo
            if score < best_score:
                best_score = score
                best_col = col
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_col

    def _minimax(self, board, depth, alpha, beta, maximizing, input_row, input_col):
        # Private method, tương tự minimax cũ
        if board.check_win(self.opponent_token, input_row, input_col):
            return 1000  # Opponent thắng -> xấu cho computer
        if board.check_win(self.token, input_row, input_col):
            return -1000  # Computer thắng -> tốt (nhưng vì là MIN, dùng negative?)
        if board.is_full() or depth == 0:
            return self._evaluate(board, input_row, input_col)

        if maximizing:  # MAX (opponent)
            max_eval = -sys.maxsize
            for col in board.get_valid_moves():
                row = self.make_move(board, col) 
                # Lưu ý: Ở đây cần switch token đúng. Maximizing là cho opponent (player), nên dùng opponent make_move.
                eval = self._minimax(board, depth - 1, alpha, beta, False, row, col)
                board.undo_move(col)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:  # MIN (computer)
            min_eval = sys.maxsize
            for col in board.get_valid_moves():
                row = self.make_move(board, col)
                eval = self._minimax(board, depth - 1, alpha, beta, True, row, col)
                board.undo_move(col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate(self, board, input_row, input_col):
        if board.check_win(self.opponent_token, input_row, input_col):
            return 1000
        if board.check_win(self.token, input_row, input_col):
            return -1000
        if board.is_full():
            return 0
        
        score = 0
        for token, val in [(self.opponent_token, 1), (self.token, -1)]:  # 1 cho opponent, -1 cho self
            for row in range(board.rows):
                for col in range(board.cols - 2):
                    if sum(1 for i in range(3) if board.grid[row][col + i] == token) == 3:
                        score += val * 10
        return score