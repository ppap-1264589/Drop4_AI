import random
import sys
import time

# ==========================================
# 1. CÁC HÀM QUẢN LÝ BẢNG (BOARD FUNCTIONS)
# ==========================================

def create_board(rows, cols):
    """Khởi tạo các thành phần của bảng game"""
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    top = [rows - 1 for _ in range(cols)]
    remain = rows * cols
    return grid, top, remain

def print_board(grid, rows, cols):
    """In bảng ra màn hình"""
    col_names = [str(i) for i in range(1, cols + 1)]
    print("\n| " + " | ".join(col_names) + " |")
    for row in grid:
        print("| " + " | ".join(row) + " |")
    print("-" * (cols * 4 + 1))

def is_valid_move(grid, col, cols):
    """Kiểm tra cột chọn có hợp lệ không"""
    return 0 <= col < cols and grid[0][col] == ' '

def get_valid_moves(grid, cols):
    """Lấy danh sách các cột còn trống"""
    moves = [col for col in range(cols) if is_valid_move(grid, col, cols)]
    random.shuffle(moves)
    return moves

def drop_move(grid, top, col, token):
    """Thực hiện thả quân cờ vào cột"""
    row = top[col]
    top[col] -= 1
    grid[row][col] = token
    return row

def undo_move(grid, top, col):
    """Hoàn tác nước đi"""
    top[col] += 1
    row = top[col]
    grid[row][col] = ' '

def check_win(grid, rows, cols, token, r, c):
    """Kiểm tra xem nước đi tại (r, c) có tạo thành chuỗi 4 không"""
    if r < 0 or grid[r][c] != token:
        return False

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # Kiểm tra hướng tới
        for i in range(1, 4):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == token:
                count += 1
            else: break
        # Kiểm tra hướng ngược lại
        for i in range(1, 4):
            nr, nc = r - i * dr, c - i * dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == token:
                count += 1
            else: break
        if count >= 4:
            return True
    return False

# ==========================================
# 2. CÁC HÀM CHO MÁY (AI / MINIMAX FUNCTIONS)
# ==========================================
node_visited = 0
cache_hit = 0
pruning = 0
total_node_visited = 0
total_cache_hit = 0
total_pruning = 0
total_computer_move = 0
total_thinking_time = 0

def board_to_hash(grid):
    """Chuyển bảng thành chuỗi để lưu vào bộ nhớ đệm (Transposition Table)"""
    return ''.join(''.join(row) for row in grid)

def evaluate_board(grid, rows, cols, top, my_token, opponent_token):
    """Hàm đánh giá điểm số của bảng hiện tại (Heuristic)"""
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for token, val in [(opponent_token, 1), (my_token, -1)]:
        for col in range(cols):
            # Duyệt từ dưới lên trong mỗi cột
            for row in range(top[col] + 1, rows):
                if grid[row][col] != token:
                    continue
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 3):
                        nr, nc = row + i * dr, col + i * dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == token:
                            count += 1
                            if count == 2: score += val * 5
                            elif count == 3: score += val * 50
                        else: break
    return score


def minimax(grid, rows, cols, top, remain, depth, alpha, beta, maximizing, 
            last_r, last_c, my_token, opponent_token, trans_table):
    """Thuật toán Minimax tìm nước đi tối ưu"""
    global node_visited, cache_hit, pruning

    node_visited += 1

    # Kiểm tra bộ nhớ đệm
    board_hash = board_to_hash(grid)
    if board_hash in trans_table and trans_table[board_hash][0] >= depth:
        cache_hit += 1
        return trans_table[board_hash][1]
        

    # Điều kiện dừng: Có người thắng hoặc hết chiều sâu/đầy bảng
    if check_win(grid, rows, cols, opponent_token, last_r, last_c):
        return 1000 + depth
    if check_win(grid, rows, cols, my_token, last_r, last_c):
        return -1000 - depth
    if remain == 0 or depth == 0:
        return evaluate_board(grid, rows, cols, top, my_token, opponent_token)

    if maximizing:
        max_eval = -sys.maxsize
        for col in get_valid_moves(grid, cols):
            r = drop_move(grid, top, col, opponent_token)
            eval = minimax(grid, rows, cols, top, remain - 1, depth - 1, alpha, beta, False, 
                           r, col, my_token, opponent_token, trans_table)
            undo_move(grid, top, col)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                pruning += 1 
                break
        score = max_eval
    else:
        min_eval = sys.maxsize
        for col in get_valid_moves(grid, cols):
            r = drop_move(grid, top, col, my_token)
            eval = minimax(grid, rows, cols, top, remain - 1, depth - 1, alpha, beta, True, 
                           r, col, my_token, opponent_token, trans_table)
            undo_move(grid, top, col)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                pruning += 1 
                break
        score = min_eval

    trans_table[board_hash] = (depth, score)
    return score




def choose_best_move(grid, rows, cols, top, remain, depth, my_token, opponent_token):
    """Hàm để máy quyết định chọn cột nào"""
    start_time = time.time()
    best_score = sys.maxsize
    best_col = None
    alpha = -sys.maxsize
    beta = sys.maxsize
    trans_table = {}

    valid_moves = get_valid_moves(grid, cols)
    if not valid_moves: return None

    global node_visited, cache_hit, pruning, total_node_visited, total_cache_hit, total_pruning, total_computer_move, total_thinking_time
    node_visited = 0
    cache_hit = 0
    pruning = 0

    for col in valid_moves:
        r = drop_move(grid, top, col, my_token)
        score = minimax(grid, rows, cols, top, remain - 1, depth - 1, alpha, beta, True, 
                        r, col, my_token, opponent_token, trans_table)
        undo_move(grid, top, col)

        if score < best_score:
            best_score = score
            best_col = col
        beta = min(beta, score)
        if beta <= alpha: 
            pruning += 1
            break

    thinking_time = time.time() - start_time
    print(f"Máy suy nghĩ trong:             {thinking_time:.4f} giây")
    print(f"Số trạng thái máy đã thăm:      {node_visited}");
    print(f"Số lần gặp bộ nhớ đệm:          {cache_hit}");
    print(f"Số lần cắt tỉa alpha-beta:      {pruning}");
    print(f"Tỉ lệ cache hit:                {cache_hit / node_visited :.2%}")
    print(f"Tỉ lệ pruning:                  {pruning / node_visited :.2%}")
    total_node_visited += node_visited
    total_cache_hit += cache_hit
    total_pruning += pruning
    total_thinking_time += thinking_time
    total_computer_move += 1
    return best_col

# ==========================================
# 3. LUỒNG CHƠI CHÍNH (MAIN GAME LOOP)
# ==========================================

def play_game():
    # Cấu hình trò chơi
    ROWS, COLS = 6, 7
    DEPTH = 6  # Độ khó
    PLAYER_MARK = 'X'
    COMPUTER_MARK = 'O'
    player_turn = True # Người đi trước

    # Khởi tạo dữ liệu
    grid, top, remain = create_board(ROWS, COLS)
    found_winner = None

    print("--- TRÒ CHƠI DROP 4 ---")

    while remain > 0 and not found_winner:
        print_board(grid, ROWS, COLS)

        if player_turn:
            # Lượt của người chơi
            try:
                move = int(input(f"Lượt bạn ({PLAYER_MARK}), chọn cột (1-{COLS}): ")) - 1
                if not is_valid_move(grid, move, COLS):
                    print("Cột đầy hoặc không hợp lệ!")
                    continue
            except ValueError:
                print("Vui lòng nhập số!")
                continue
            
            row = drop_move(grid, top, move, PLAYER_MARK)
            if check_win(grid, ROWS, COLS, PLAYER_MARK, row, move):
                found_winner = "PLAYER"
        else:
            # Lượt của máy
            print(f"Máy ({COMPUTER_MARK}) đang suy nghĩ...")
            move = choose_best_move(grid, ROWS, COLS, top, remain, DEPTH, COMPUTER_MARK, PLAYER_MARK)
            row = drop_move(grid, top, move, COMPUTER_MARK)
            print(f"Máy chọn cột: {move + 1}")
            if check_win(grid, ROWS, COLS, COMPUTER_MARK, row, move):
                found_winner = "COMPUTER"

        remain -= 1
        player_turn = not player_turn

    # Kết quả chung cuộc
    print_board(grid, ROWS, COLS)
    if found_winner == "PLAYER":
        print("CHÚC MỪNG! BẠN ĐÃ THẮNG!")
    elif found_winner == "COMPUTER":
        print("MÁY THẮNG! HÃY THỬ LẠI LẦN SAU.")
    else:
        print("HÒA!")

    global total_node_visited, total_cache_hit, total_pruning, total_computer_move, total_thinking_time
    print(f"Tổng số nước máy đã đi:         {total_computer_move}");
    print(f"Tổng thời gian máy đã nghĩ:     {total_thinking_time}");
    print(f"Tổng trạng thái máy đã thăm:    {total_node_visited}");
    print(f"Tổng số lần gặp bộ nhớ đệm:     {total_cache_hit}");
    print(f"Tổng số lần cắt tỉa alpha-beta: {total_pruning}");
    print(f"Thời gian nghĩ trung bình:      {total_thinking_time/total_computer_move:.4f}");
    print(f"Tỉ lệ cache hit trung bình:     {total_cache_hit / total_node_visited :.2%}")
    print(f"Tỉ lệ pruning trung bình:       {total_pruning / total_node_visited :.2%}")

    # Số cạnh = số đỉnh - 1
    # Mà số đỉnh ngay từ đầu đã cố tính bỏ qua trạng thái "không có gì cả" từ đầu
    # Nên total_node_visited cũng đại diện cho số cạnh đã đi qua trên cây tìm kiếm
if __name__ == "__main__":
    play_game()
