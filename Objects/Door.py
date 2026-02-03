import pygame

GREEN = (50, 200, 50)
BROWN = (120, 70, 30)

class Door:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)

    def draw(self, surface, unlocked):
        color = GREEN if unlocked else BROWN
        pygame.draw.rect(surface, color, self.rect)