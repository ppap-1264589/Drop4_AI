import sys

class Computer:
    def __init__(self, token, opponent_token, depth_search):
        self.token = token
        self.opponent_token = opponent_token
        self.depth_search = depth_search
        self.trans_table = {}  # {board_hash: (depth, score)}
    # Khởi tạo token là token của mình
    # opponent_token là token của đối thủ


    def board_to_hash(self, board):
        return ''.join(''.join(row) for row in board.grid)
    # Băm bảng ra thành một trạng thái duy nhất
    # Trạng thái này lưu lại độ sâu và điểm số mà thuật toán đạt được
    # Ý nghĩa: Nhỡ sau này gặp lại các trạng thái tương tự thì return điểm số luôn cho đỡ mất thời gian
    # Nhược điểm: Có nguy cơ tốn nhiều bộ nhớ (Tổng số trạng thái cần lưu khả thi là cỡ 2^(n*m))
    
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
        # Tham số truyền vào ban đầu có depth: là độ sâu cần tìm
        # depth càng lớn tức là trạng thái của game vẫn còn càng sớm
        board_hash = self.board_to_hash(board)
        if board_hash in self.trans_table and self.trans_table[board_hash][0] >= depth:
            return self.trans_table[board_hash][1]
        # Điều kiện self.trans_table[board_hash][0] >= depth đảm bảo:
        # Chỉ tái sử dụng điểm số nếu trạng thái board đã được tính toán ở độ sâu bằng hoặc lớn hơn độ sâu hiện tại.
        # Nếu độ sâu lưu trong table nhỏ hơn (self.trans_table[board_hash][0] < depth), điểm số đó không đủ đáng tin cậy (vì được tính với ít nước đi hơn), nên cần tính lại Minimax ở độ sâu hiện tại

        if board.check_win(self.opponent_token, input_row, input_col):
            score = 1000 + depth # Ưu tiên tháng sớm (điểm cao nếu depth còn lớn)
        elif board.check_win(self.token, input_row, input_col):
            score = -1000 - depth # Ưu tiên thắng sớm (điểm cao nếu depth còn lớn)
        elif board.is_full() or depth == 0:
            score = self._evaluate(board)
        else:
            if maximizing:
                max_eval = -sys.maxsize
                for col in board.get_valid_moves():
                    row = board.drop_move(col, self.opponent_token)
                    eval = self._minimax(board, depth - 1, alpha, beta, False, row, col)
                    board.undo_move(col)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                score = max_eval
            else:
                min_eval = sys.maxsize
                for col in board.get_valid_moves():
                    row = board.drop_move(col, self.token)
                    eval = self._minimax(board, depth - 1, alpha, beta, True, row, col)
                    board.undo_move(col)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                score = min_eval
        self.trans_table[board_hash] = (depth, score)
        return score
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
                for row in range(board.top[col]+1, board.rows): 
                # for từ đỉnh cột về đáy cột

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