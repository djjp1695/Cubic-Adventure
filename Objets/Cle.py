import os

import pygame

from Utilitaires.ColorSelector import ColorSelector

IMAGE = os.path.join("Assets", "Images/—Pngtree—key icon is part of_7513131.png")
# --- Key class ---
class Cle:
    def __init__(self, x, y, couleur=None):
        #Si aucune couleur en paramètre Mauve par défaut
        if not couleur:
            self.couleur = ColorSelector.PURPLE.value
        else:
            self.couleur = couleur.value
        self.rect = pygame.Rect(x, y, 20, 30)
        self.recuperee = False

    def dessiner(self, surface):
        if not self.recuperee:
            pygame.draw.rect(surface, self.couleur, self.rect)
