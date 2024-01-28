import pygame
import numpy as np


class SandBox:
    fps = 100

    def __init__(self, cols, rows, w):
        self.cols = cols
        self.rows = rows
        self.w = w
        self.gravity = 0.1
        self.hue_value = 200
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((cols * w, rows * w))
        pygame.display.set_caption("SandBox")

        self.grid = self.make_2D_array(cols, rows)
        self.velocity_grid = self.make_2D_array(cols, rows)

        self.running = True

    def color(self, h, s=1, l=1):
        r = (int(max(0, min(255, 255 * abs(h * 6 - 3) - 1))) * l)
        g = (int(max(0, min(255, 255 * (2 - abs(h * 6 - 2)) - 1))) * l)
        b = (int(max(0, min(255, 255 * (2 - abs(h * 6 - 4)) - 1))) * l)
        r = r + (255 - r) * (1 - s)
        g = g + (255 - g) * (1 - s)
        b = b + (255 - b) * (1 - s)
        return r, g, b

    def make_2D_array(self, cols, rows):
        return np.zeros((cols, rows), dtype=int)

    def within_cols(self, i):
        return 0 <= i <= self.cols - 1

    def within_rows(self, j):
        return 0 <= j <= self.rows - 1

    def run_simulation(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))

            if pygame.mouse.get_pressed()[0]:
                mouse_col, mouse_row = pygame.mouse.get_pos()
                mouse_col //= self.w
                mouse_row //= self.w

                matrix_size = 5
                extent = matrix_size // 2
                for i in range(-extent, extent + 1):
                    for j in range(-extent, extent + 1):
                        if np.random.rand() < 0.75:
                            col = mouse_col + i
                            row = mouse_row + j
                            if self.within_cols(col) and self.within_rows(row):
                                self.grid[col][row] = self.hue_value
                                self.velocity_grid[col][row] = 1

                self.hue_value += 0.001
                if self.hue_value > 2:
                    self.hue_value = 1

            for i in range(self.cols):
                for j in range(self.rows):
                    if self.grid[i][j] > 0:
                        color = self.color(h=self.grid[i][j] - 1, s=1, l=1)
                        pygame.draw.rect(self.screen, color,
                                         (i * self.w, j * self.w, self.w, self.w))

            next_grid = self.make_2D_array(self.cols, self.rows)
            next_velocity_grid = self.make_2D_array(self.cols, self.rows)

            for i in range(self.cols):
                for j in range(self.rows):
                    state = self.grid[i][j]
                    velocity = self.velocity_grid[i][j]
                    moved = False

                    if state > 0:
                        new_pos = int(j + velocity)
                        for y in range(min(new_pos, self.rows - 1), j, -1):
                            below = self.grid[i][y]
                            direction = 1 if np.random.rand() < 0.5 else -1
                            below_a = self.grid[i + direction, y] if self.within_cols(i + direction) else -1
                            below_b = self.grid[i - direction, y] if self.within_cols(i - direction) else -1

                            if below == 0:
                                next_grid[i, y] = state
                                next_velocity_grid[i, y] = velocity + self.gravity
                                moved = True
                                break
                            elif below_a == 0:
                                next_grid[i + direction, y] = state
                                next_velocity_grid[i + direction, y] = velocity + self.gravity
                                moved = True
                                break
                            elif below_b == 0:
                                next_grid[i - direction, y] = state
                                next_velocity_grid[i - direction, y] = velocity + self.gravity
                                moved = True
                                break

                    if state > 0 and not moved:
                        next_grid[i, j] = self.grid[i, j]
                        next_velocity_grid[i, j] = self.velocity_grid[i, j] + self.gravity

            self.grid = next_grid
            self.velocity_grid = next_velocity_grid

            pygame.display.flip()
            print(self.clock.tick(self.fps) / 1000)
            print(int(self.clock.get_fps()))

        pygame.quit()
