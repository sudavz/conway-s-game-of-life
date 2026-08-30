from math import ceil

import numpy as np
import pygame

from game_egine import GameEngine
from utils import calculate_rgb_color


class Simulation:
    BACKGROUND_COLOR = (15, 15, 15)
    CELL_ALIVE_COLOR = (198, 229, 245)
    CELL_DEAD_COLOR = (0, 0, 0)
    CELL_SIZE = 10
    CELL_BORDER = 1

    def __init__(self, parent_surface: pygame.Surface):
        parent_surface_size = parent_surface.get_size()
        self.parent_surface = parent_surface
        self.surface = pygame.Surface(parent_surface_size)
        self.surface_width = parent_surface_size[0]
        self.surface_height = parent_surface_size[1]
        self.surface.fill(self.BACKGROUND_COLOR)
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.show_cell_border = True
        self.show_frecuencies = False
        self.is_running = False
        self.build_simulation()

    def build_simulation(self):
        self.max_window_rows = ceil(self.surface_height / self.CELL_SIZE)
        self.max_window_columns = ceil(self.surface_width / self.CELL_SIZE)
        display_width, display_heignt = pygame.display.get_desktop_sizes()[
            0
        ]  # Get full display size to create game world
        max_rows_engine = ceil(display_heignt / self.CELL_SIZE)
        max_cols_engine = ceil(display_width / self.CELL_SIZE)
        self.game_engine = GameEngine(max_rows_engine, max_cols_engine)
        self.game_engine.scanning_limit(self.max_window_rows, self.max_window_columns)
        self.build_rects()

    def build_rects(self):
        cell_rects = []

        for py in range(0, self.surface_height, self.CELL_SIZE):
            column_cell_rects = []
            for px in range(0, self.surface_width, self.CELL_SIZE):
                rect = pygame.rect.Rect(px, py, self.CELL_SIZE, self.CELL_SIZE)

                i = py // self.CELL_SIZE
                j = px // self.CELL_SIZE

                i_ = i + self.game_engine.scaning_min_i
                j_ = j + self.game_engine.scaning_min_j

                value = self.game_engine.get_cell_value(i_, j_)

                self.update_rect(i, j, value, rect)

                column_cell_rects.append(rect)

            cell_rects.append(np.array(column_cell_rects))

        self.cell_rects = np.array(cell_rects)

    def switch_cell_border(self):
        self.show_cell_border = not self.show_cell_border
        self.refresh_all_rects()

    def switch_show_frecuencies(self):
        self.show_frecuencies = not self.show_frecuencies
        self.refresh_all_rects()

    def update_rect(self, i, j, new_cell_value, rect=None):

        if i >= self.max_window_rows or j >= self.max_window_columns or i < 0 or j < 0:
            return

        cell_rect = rect if rect is not None else self.cell_rects[i][j]

        color = self.CELL_ALIVE_COLOR if new_cell_value == 1 else self.CELL_DEAD_COLOR

        cell_border = 0

        if self.show_cell_border:
            cell_border = 0 if new_cell_value == 1 else self.CELL_BORDER
            if cell_border == self.CELL_BORDER:
                pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, cell_rect, 0)

        if self.show_frecuencies:
            frecuency = self.game_engine.get_cell_frecuency(
                i + self.game_engine.scaning_min_i, j + self.game_engine.scaning_min_j
            )
            color = calculate_rgb_color.calculate_rgb_color(frecuency)

        pygame.draw.rect(self.surface, color, cell_rect, cell_border)

    def resize(self, width, heigth):
        self.surface_height = heigth
        self.surface_width = width
        self.surface = pygame.Surface((width, heigth))
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.surface.fill(self.BACKGROUND_COLOR)
        self.max_window_rows = ceil(self.surface_height / self.CELL_SIZE)
        self.max_window_columns = ceil(self.surface_width / self.CELL_SIZE)
        self.game_engine.scanning_limit(self.max_window_rows, self.max_window_columns)
        self.build_rects()

    def set_cell_status(self, coord_x: int, coord_y: int, status: bool) -> tuple[int]:
        j = coord_x // self.CELL_SIZE  # columns
        i = coord_y // self.CELL_SIZE  # rows

        (new_cell_value, before_cell_value) = self.game_engine.set_value_cell(
            i,
            j,
            status,
            in_memo=self.is_running,
        )

        # Optimization  only render the cell that have change
        if self.show_frecuencies or before_cell_value != new_cell_value:
            self.update_rect(i, j, new_cell_value)

        return (i, j)

    def release_cells_memory(self):
        self.game_engine.release_cells_memory()

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def clear(self):
        self.stop()
        self.game_engine.reset()
        for i in range(self.max_window_rows):
            for j in range(self.max_window_columns):
                self.update_rect(i, j, 0)

    def refresh_all_rects(self):
        for i in range(self.max_window_rows):
            for j in range(self.max_window_columns):
                i_ = i + self.game_engine.scaning_min_i
                j_ = j + self.game_engine.scaning_min_j
                cell_value = self.game_engine.get_cell_value(i_, j_)
                self.update_rect(i, j, cell_value)

    def next_generation(self):
        self.game_engine.next_generation(
            lambda i, j, v: self.update_rect(
                i - self.game_engine.scaning_min_i,
                j - self.game_engine.scaning_min_j,
                v,
            )
        )

    def get_total_alive_cells(self):
        return len(self.game_engine.alive_cells)

    def get_current_generation(self):
        return self.game_engine.current_generation
