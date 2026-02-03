import pygame

from Utilitaires.ColorSelector import ColorSelector


# --- Key class ---
class Cle:
    def __init__(self, x, y, couleur=None):
        if not couleur:
            self.couleur = ColorSelector.PURPLE.value
        else:
            self.couleur = couleur.value
        self.rect = pygame.Rect(x, y, 20, 30)
        self.recuperee = False

    def dessiner(self, surface):
        if not self.recuperee:
            pygame.draw.rect(surface, self.couleur, self.rect)
