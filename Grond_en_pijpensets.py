import pygame
import random

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        self.x, self.y = 0, self.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 15)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)


class Pipes:
    width = 25
    opening = 175
    pipe_image = None

    def __init__(self, win_width):
        if Pipes.pipe_image is None:
            Pipes.pipe_image = pygame.image.load("pipe.png")
        self.x = win_width + self.opening
        self.bottom_height = random.randint(35, 220)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        # Scale and draw bottom pipe
        bottom_pipe = pygame.transform.scale(Pipes.pipe_image, (self.width, self.bottom_height))
        window.blit(bottom_pipe, (self.x, Ground.ground_level - self.bottom_height))

        # Scale, flip, and draw top pipe (upside down)
        top_pipe = pygame.transform.scale(Pipes.pipe_image, (self.width, self.top_height))
        top_pipe = pygame.transform.flip(top_pipe, False, True)  # Flip vertically
        window.blit(top_pipe, (self.x, 0))

    def update(self):
        self.x -= 1
        if self.x + Pipes.width <=  50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True