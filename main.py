from Drop4.Game import Game

if __name__ == "__main__":
    rows = 6
    cols = 7
    depth_search = 9
    player_first = False
    player_mark = 'X'
    computer_mark = 'O'
    # Chọn các tham số cho trò chơi
    # Cho phép điều chỉnh ai đánh trước, ai đánh sau
    # Cho phép điều chỉnh độ sâu của cây tìm kiếm

    game = Game(rows, cols, depth_search, player_mark, computer_mark, player_first)
    game.play_game()