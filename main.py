from Drop4.Game import Game

if __name__ == "__main__":
    rows = 6
    cols = 7
    depth_search = 6
    player_first = True
    player_mark = 'X'
    computer_mark = 'O'

    game = Game(rows, cols, depth_search, player_mark, computer_mark, player_first)
    game.play_game()