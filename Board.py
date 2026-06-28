from Logger import logger


class Board:
    def __init__(self, rows, columns):
        self.__rows: int = rows
        self.__columns: int = columns
        self.board = [["." for _ in range(self.__columns)] for _ in range(self.__rows)]

    def draw_board(self):
        for row in range(self.__rows):
            print(*self.board[row])
        print("END of iteration")

    def change_cell_liveness(self, row, col):
        if self.board[row][col] == ".":
            self.board[row][col] = "#"
            logger.debug(
                f"cell on coordinates ({row},{col}) has switched liveness to ALIVE"
            )
        else:
            self.board[row][col] = "."
            logger.debug(
                f"cell on coordinates ({row},{col}) has switched liveness to DEAD"
            )

    def get_cell_liveness(self, row, col):
        return self.board[row][col] == "#"

    def count_cell_alive_neighbours(self, row, col):
        alive_neighbours = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if 0 <= i < self.__rows and 0 <= j < self.__columns:
                    if self.get_cell_liveness(i, j):
                        alive_neighbours += 1
        logger.debug(f"({row},{col}) has {alive_neighbours} alive neighbours")
        return alive_neighbours

    def step(self):
        new_board = [row[:] for row in self.board]
        for row in range(self.__rows):
            for col in range(self.__columns):
                alive = self.get_cell_liveness(row, col)
                neighbours = self.count_cell_alive_neighbours(row, col)
                if alive and (neighbours < 2 or neighbours > 3):
                    new_board[row][col] = "."
                elif not alive and neighbours == 3:
                    new_board[row][col] = "#"
        self.board = new_board
