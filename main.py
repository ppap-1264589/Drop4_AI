from Drop4.Game import Game

if __name__ == "__main__":
    rows = 5
    cols = 6
    depth_search = 8
    player_first = True
    player_mark = 'X'
    computer_mark = 'O'
    # Chọn các tham số cho trò chơi

    game = Game(rows, cols, depth_search, player_mark, computer_mark, player_first)
    game.play_game()