from .board import Board  # Import để dùng board

def evaluate(board: Board):
    # Code evaluate ở đây, mở rộng heuristic
    if board.check_win('X'):
        return 1000
    # ...
    return score