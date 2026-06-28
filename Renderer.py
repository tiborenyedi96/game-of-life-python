import math
import pygame


class Button:
    def __init__(self, x, y, w, h, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label

    def draw(self, screen, font):
        pygame.draw.rect(screen, (50, 50, 55), self.rect, border_radius=6)
        pygame.draw.rect(screen, (90, 90, 100), self.rect, width=1, border_radius=6)
        text = font.render(self.label, True, (230, 230, 230))
        screen.blit(text, text.get_rect(center=self.rect.center))

    def hit(self, pos):
        return self.rect.collidepoint(pos)


class Renderer:
    def __init__(self, width=1920, height=1080):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)

        self.cam_row = 0.0
        self.cam_col = 0.0
        self.cell_size = 20.0

        self.bg_color = (16, 16, 18)
        self.alive_color = (90, 220, 120)
        self.grid_color = (38, 38, 42)

        self.buttons = {
            "start": Button(10, 10, 90, 34, "Start"),
            "pause": Button(110, 10, 90, 34, "Pause"),
            "reset": Button(210, 10, 90, 34, "Reset"),
        }

    def screen_to_cell(self, pos):
        x, y = pos
        world_col = self.cam_col + (x - self.width / 2) / self.cell_size
        world_row = self.cam_row + (y - self.height / 2) / self.cell_size
        return math.floor(world_row), math.floor(world_col)

    def cell_to_screen(self, row, col):
        x = (col - self.cam_col) * self.cell_size + self.width / 2
        y = (row - self.cam_row) * self.cell_size + self.height / 2
        return x, y

    def pan(self, dx_pixels, dy_pixels):
        self.cam_col -= dx_pixels / self.cell_size
        self.cam_row -= dy_pixels / self.cell_size

    def zoom(self, factor, mouse_pos):
        mx, my = mouse_pos
        world_col = self.cam_col + (mx - self.width / 2) / self.cell_size
        world_row = self.cam_row + (my - self.height / 2) / self.cell_size
        self.cell_size = max(2.0, min(80.0, self.cell_size * factor))
        self.cam_col = world_col - (mx - self.width / 2) / self.cell_size
        self.cam_row = world_row - (my - self.height / 2) / self.cell_size

    def center_on(self, row, col):
        self.cam_row, self.cam_col = row, col

    def draw(self, board, state):
        self.screen.fill(self.bg_color)
        self._draw_grid()
        size = int(self.cell_size)
        for (row, col) in board.live_cells:
            x, y = self.cell_to_screen(row, col)
            if -size <= x <= self.width and -size <= y <= self.height:
                pygame.draw.rect(self.screen, self.alive_color,
                                 (int(x), int(y), size, size))
        self._draw_toolbar(state)
        pygame.display.flip()

    def _draw_grid(self):
        if self.cell_size < 8:
            return
        first_col = math.floor(self.cam_col - (self.width / 2) / self.cell_size)
        first_row = math.floor(self.cam_row - (self.height / 2) / self.cell_size)
        x0, _ = self.cell_to_screen(0, first_col)
        _, y0 = self.cell_to_screen(first_row, 0)
        x = x0
        while x <= self.width:
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
            x += self.cell_size
        y = y0
        while y <= self.height:
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))
            y += self.cell_size

    def _draw_toolbar(self, state):
        for button in self.buttons.values():
            button.draw(self.screen, self.font)
        label = self.font.render(f"State: {state}", True, (200, 200, 200))
        self.screen.blit(label, (320, 18))

    def button_at(self, pos):
        for name, button in self.buttons.items():
            if button.hit(pos):
                return name
        return None