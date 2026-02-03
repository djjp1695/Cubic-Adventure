import pygame

YELLOW = (255, 215, 0)

class Coin:
    def __init__(self, x, y ):
        self.__color = YELLOW
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, self.__color, self.rect.center, 10)
