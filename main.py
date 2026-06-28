import time
from Board import Board

rows, columns = 16, 16
game_board = Board(rows, columns)

if __name__ == "__main__":
    # glider by hand for testing
    game_board.change_cell_liveness(1, 2)
    game_board.change_cell_liveness(2, 3)
    game_board.change_cell_liveness(3, 1)
    game_board.change_cell_liveness(3, 2)
    game_board.change_cell_liveness(3, 3)

    # game loop
    generations = 20
    for _ in range(generations):
        game_board.draw_board()
        game_board.step()
        time.sleep(0.5)
