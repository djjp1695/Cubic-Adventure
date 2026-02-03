import pygame


class Piece:
    def __init__(self, x, y, couleur ):
        self.couleur = couleur
        self.rect = pygame.Rect(x, y, 20, 20)
        self.recupere = False

    def draw(self, surface):
        if not self.recupere:
            pygame.draw.circle(surface, self.couleur, self.rect.center, 10)
