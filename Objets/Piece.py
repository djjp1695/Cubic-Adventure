import pygame

from Utilitaires.ColorSelector import ColorSelector


class Piece:
    def __init__(self, x, y, couleur=None):
        # Si aucune couleur en paramètre Jaune par défaut
        if not couleur:
            self.couleur = ColorSelector.YELLOW.value
        else:
            self.couleur = couleur.value
        self.rect = pygame.Rect(x, y, 20, 20)
        self.recupere = False

    def dessiner(self, surface):
        if not self.recupere:
            pygame.draw.circle(surface, self.couleur, self.rect.center, 10)
