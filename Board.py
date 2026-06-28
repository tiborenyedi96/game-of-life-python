from Logger import logger


class Board:
    def __init__(self):
        self.live_cells = set()

    def change_cell_liveness(self, row, col):
        cell = (row, col)
        if cell in self.live_cells:
            self.live_cells.discard(cell)
            logger.debug(f"({row},{col}) -> DEAD")
        else:
            self.live_cells.add(cell)
            logger.debug(f"({row},{col}) -> ALIVE")

    def get_cell_liveness(self, row, col):
        return (row, col) in self.live_cells

    def clear(self):
        self.live_cells.clear()

    def step(self):
        neighbour_counts = {}
        for (row, col) in self.live_cells:
            for d_row in (-1, 0, 1):
                for d_col in (-1, 0, 1):
                    if d_row == 0 and d_col == 0:
                        continue
                    neighbour = (row + d_row, col + d_col)
                    neighbour_counts[neighbour] = neighbour_counts.get(neighbour, 0) + 1

        new_live_cells = set()
        for cell, count in neighbour_counts.items():
            if count == 3:
                new_live_cells.add(cell)
            elif count == 2 and cell in self.live_cells:
                new_live_cells.add(cell)
        self.live_cells = new_live_cells

    def centroid(self):
        if not self.live_cells:
            return 0.0, 0.0
        rows = [r for (r, _) in self.live_cells]
        cols = [c for (_, c) in self.live_cells]
        return sum(rows) / len(rows), sum(cols) / len(cols)