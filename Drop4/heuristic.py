from .board import Board

def evaluate(board: Board):
    # Code evaluate ở đây, mở rộng heuristic
    if board.check_win('X'):
        return 1000
    if board.check_win('O'):
        return -1000
    if board.is_full():
        return 0
    # Heuristic: Đếm cơ hội 3 liên tiếp
    score = 0
    for player, val in [('X', 1), ('O', -1)]:
        for row in range(board.rows):
            for col in range(board.cols - 2):
                if sum(1 for i in range(3) if board.board[row][col + i] == player) == 3:
                    score += val * 10
    return score