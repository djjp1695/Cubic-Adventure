import pygame

GREEN = (50, 200, 50)
BROWN = (120, 70, 30)

class Porte:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)

    def dessiner(self, surface, deverouillee):
        couleur = GREEN if deverouillee else BROWN
        pygame.draw.rect(surface, couleur, self.rect)