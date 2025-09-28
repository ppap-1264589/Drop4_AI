import sys

class Computer:
    def __init__(self, token, opponent_token, depth_search):
        self.token = token
        self.opponent_token = opponent_token
        self.depth_search = depth_search
    # Khởi tạo token là token của mình
    # opponent_token là token của đối thủ
    
    def choose_best_move(self, board):
        best_score = sys.maxsize
        best_col = None
        alpha = -sys.maxsize
        beta = sys.maxsize
        # Cần tìm min cho máy nên đặt best_score là -maxsize trước

        for col in board.get_valid_moves():
            row = board.drop_move(col, self.token)
            score = self._minimax(board, self.depth_search - 1, alpha, beta, True, row, col)
            # Với mỗi nước đi khả thi của máy, thử gọi đệ quy
            board.undo_move(col)
            if score < best_score:
                best_score = score
                best_col = col
            beta = min(beta, score)
            if beta <= alpha:
                break
        print(best_score)
        return best_col

    def _minimax(self, board, depth, alpha, beta, maximizing, input_row, input_col):
        if board.check_win(self.opponent_token, input_row, input_col):
            return 1000 + depth  # Ưu tiên thắng sớm (điểm cao hơn nếu depth lớn)
        if board.check_win(self.token, input_row, input_col):
            return -1000 - depth  # Ưu tiên thắng sớm (điểm thấp hơn nếu depth lớn)
        if board.is_full() or depth == 0:
            return self._evaluate(board)
        # Ban đầu thì depth là một số lớn. Càng đi sâu xuống dưới thì depth càng nhỏ đi.

        if maximizing:  # MAX (opponent)
            max_eval = -sys.maxsize
            for col in board.get_valid_moves():
                row = board.drop_move(col, self.opponent_token)
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
                row = board.drop_move(col, self.token)
                eval = self._minimax(board, depth - 1, alpha, beta, True, row, col)
                board.undo_move(col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    ### LOGIC CHÍNH CỦA THUẬT TOÁN MINIMAX. CẦN CÓ THÊM LỜI GIẢI THÍCH    



    

    def _evaluate(self, board):
        # Cải thiện: Đếm chuỗi 2/3 ở tất cả hướng, score khác nhau (2: ±5, 3: ±50)
        # Không cần đếm 4 vì đã xử lý ở check_win
        score = 0
        directions = [
            (0,1), 
            (1,0), 
            (1,1), 
            (1,-1)
        ]  # Ngang, dọc, chéo \, chéo /
        
        for token, val in [(self.opponent_token, 1), (self.token, -1)]:
            for col in range(board.cols):   # Với mỗi cột, xét ngược từ dưới lên
                for row in range(board.rows-1, board.bottom[col], -1): 
                    # for ngược từ đáy bảng về đầu cho tới khi chạm thứ khác token thì thôi
                    if board.grid[row][col] != token:
                        continue
                
                    for dr, dc in directions:
                        count = 1
                        for i in range(1, 3):  # Chỉ xét thêm tối đa 1 và 2 ô nữa để được 2 và 3 ô liên tiếp nhau
                            nr, nc = row + i*dr, col + i*dc
                            if 0 <= nr < board.rows and 0 <= nc < board.cols and board.grid[nr][nc] == token:
                                count += 1

                                if count == 2:
                                    score += val * 5
                                elif count == 3:
                                    score += val * 50
                                # Score dựa trên count (chỉ đếm một hướng để tránh double-count)
                                # Ở đây, chả hạn một chuỗi 3 thì sẽ được coi như là một chuỗi 3 và 2 chuỗi 2. Tổng điểm mang lại là 50+10
                            else:
                                break

        return score