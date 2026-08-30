import pygame


class NavbarInfo:
    BACKGROUND_COLOR = (0, 0, 0, 100)
    TEXT_COLOR = "white"
    TEXT_SIZE = 15

    def __init__(self, parent_surface: pygame.Surface):
        self.parent_surface = parent_surface
        self.text_font: pygame.font.SysFont = pygame.font.Font(
            "assets/EightBitDragon-anqx.ttf", self.TEXT_SIZE
        )
        self.surface_height = 27
        self.build()

    def build(self):
        parent_surface_size = self.parent_surface.get_size()
        self.surface_width = parent_surface_size[0]
        self.surface = pygame.surface.Surface(
            (self.surface_width, self.surface_height), pygame.SRCALPHA
        )
        self.surface.fill(self.BACKGROUND_COLOR)
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.update_generation(0)
        self.update_cell_alives(0)
        self.update_size(parent_surface_size[0], parent_surface_size[1])

    def update_generation(self, value):
        generation_text = self.text_font.render(f"gen: {value}", True, self.TEXT_COLOR)
        generation_text_rect = generation_text.get_rect(topleft=(10, 5))
        generation_text_rect.width += 10
        pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, generation_text_rect)
        self.surface.blit(generation_text, generation_text_rect)

    def update_cell_alives(self, value):
        cell_alives_text = self.text_font.render(
            f"cell_alives: {value}", True, self.TEXT_COLOR
        )

        cell_alives_text_rect = cell_alives_text.get_rect(topleft=(140, 5))
        cell_alives_text_rect.width += 10
        pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, cell_alives_text_rect)
        self.surface.blit(cell_alives_text, cell_alives_text_rect)

    def update_size(self, width, heigth):
        window_size_text = self.text_font.render(
            f" {width}x{heigth}", True, self.TEXT_COLOR
        )
        window_size_text_rect = window_size_text.get_rect(
            topleft=(self.surface_width - 125, 5)
        )
        window_size_text_rect.width += 10
        pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, window_size_text_rect)
        self.surface.blit(window_size_text, window_size_text_rect)

    def update_speed(self, time):
        speed_text = self.text_font.render(f" speed: {time}X", True, self.TEXT_COLOR)
        speed_text_rect = speed_text.get_rect(topleft=(340, 5))
        speed_text_rect.width += 10
        pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, speed_text_rect)
        self.surface.blit(speed_text, speed_text_rect)

    def update_fps(self, time):
        fps_text = self.text_font.render(f" fps: {time}", True, self.TEXT_COLOR)
        fps_text_rect = fps_text.get_rect(topleft=(self.surface_width - 230, 5))
        fps_text_rect.width += 10
        pygame.draw.rect(self.surface, self.BACKGROUND_COLOR, fps_text_rect)
        self.surface.blit(fps_text, fps_text_rect)
