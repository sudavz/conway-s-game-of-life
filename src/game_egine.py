from collections.abc import Callable


class GameEngine:
    def __init__(self, max_rows=1000, max_columns=1000):
        self.max_rows = max_rows
        self.max_columns = max_columns
        self.reset()
        self.scanning_limit()

    def scanning_limit(self, rows=None, columns=None):

        col_resolved = columns if columns is not None else self.max_columns
        row_resolved = rows if rows is not None else self.max_rows

        diff_col = (self.max_columns - col_resolved) // 2
        diff_row = (self.max_rows - row_resolved) // 2

        self.scaning_min_j = diff_col
        self.scaning_max_j = self.max_columns - diff_col - 1

        self.scaning_min_i = diff_row
        self.scaning_max_i = self.max_rows - diff_row - 1

    def set_value_cell(self, i, j, status, in_memo=False):

        pos = (i + self.scaning_min_i, j + self.scaning_min_j)

        before_cell_value = self.get_cell_value(pos[0], pos[1])

        new_cell_value = 1 if status else 0

        self.set_cell_frecuency(pos[0], pos[1], new_cell_value)

        if new_cell_value == 1:
            if in_memo:
                self.cells_memory.add(pos)
            else:
                self.alive_cells.add(pos)
        else:
            if pos in self.cells_memory:
                self.cells_memory.remove(pos)
            if pos in self.alive_cells:
                self.alive_cells.remove(pos)

        return (new_cell_value, before_cell_value)

    def release_cells_memory(self):
        self.alive_cells = self.alive_cells.union(self.cells_memory)

    def reset(self):
        self.alive_cells = set()
        self.cells_memory = set()
        self.current_generation = 0
        self.frecuencies = {}

    def set_cell_frecuency(self, i, j, value):
        pos = (i, j)
        if self.frecuencies.get(pos) is None:
            self.frecuencies[pos] = value
        else:
            self.frecuencies[pos] += value

    def get_cell_frecuency(self, i, j):
        pos = (i, j)
        if self.frecuencies.get(pos) is None:
            return 0
        else:
            return self.frecuencies[pos]

    def get_cell_value(self, i, j):
        return 1 if (i, j) in self.alive_cells else 0

    def next_generation(self, callback: Callable[[int, int, int], None]):
        next_alive_cells = set()
        explored_cells = set()

        for i, j in self.alive_cells:  # n
            positions_ = [
                (i, j),
                (i, (j + 1) % self.max_columns),
                (i, (j - 1) % self.max_columns),
                ((i + 1) % self.max_rows, (j + 1) % self.max_columns),
                ((i + 1) % self.max_rows, (j - 1) % self.max_columns),
                ((i + 1) % self.max_rows, j),
                ((i - 1) % self.max_rows, (j - 1) % self.max_columns),
                ((i - 1) % self.max_rows, (j + 1) % self.max_columns),
                ((i - 1) % self.max_rows, j),
            ]

            for k, p in positions_:  # 3x3
                if (k, p) in explored_cells:
                    continue

                cell_value = self.get_cell_value(k, p)

                new_cell_value = self.verify_cell(k, p, self.alive_cells)  # 3x3

                if cell_value != new_cell_value:
                    self.set_cell_frecuency(k, p, new_cell_value)
                    callback(k, p, new_cell_value)

                if new_cell_value == 1:
                    next_alive_cells.add((k, p))

                explored_cells.add((k, p))

        self.current_generation += 1
        self.alive_cells = next_alive_cells

    def verify_cell(self, i, j, board: set) -> int:
        cell = 1 if (i, j) in board else 0

        total_neighbors = self.get_total_neighbors(board, i, j)

        if cell == 0 and total_neighbors == 3:
            cell = 1

        elif cell == 1 and total_neighbors < 2 or total_neighbors > 3:
            cell = 0

        return cell

    def get_total_neighbors(self, board: set, i: int, j: int) -> int:
        total_neighbors = 0

        for k in [1, 0, -1]:
            for p in [1, 0, -1]:
                ni = (i + k) % self.max_rows
                nc = (j + p) % self.max_columns

                if ni == i and nc == j:
                    continue

                total_neighbors += 1 if (ni, nc) in board else 0

        return total_neighbors
