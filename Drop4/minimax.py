import sys
from .board import Board
from .heuristic import evaluate

def minimax(board: Board, depth, alpha, beta, maximizing):
    if board.check_win('X'):
        return 1000
    if board.check_win('O'):
        return -1000
    if board.is_full() or depth == 0:
        return evaluate(board)

    if maximizing:  # MAX ('X')
        max_eval = -sys.maxsize
        for col in board.get_valid_moves():
            board.make_move(col, 'X')
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.undo_move(col)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:  # MIN ('O')
        min_eval = sys.maxsize
        for col in board.get_valid_moves():
            board.make_move(col, 'O')
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.undo_move(col)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board: Board, depth):
    best_score = sys.maxsize
    best_col = None
    alpha = -sys.maxsize
    beta = sys.maxsize
    for col in board.get_valid_moves():
        board.make_move(col, 'O')  # Máy là 'O'
        score = minimax(board, depth - 1, alpha, beta, True)
        board.undo_move(col)
        if score < best_score:
            best_score = score
            best_col = col
        beta = min(beta, score)
        if beta <= alpha:
            break
    return best_col