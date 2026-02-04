import pygame

from Utilitaires.ColorSelector import ColorSelector


class Porte:
    def __init__(self, x, y, couleurDeverouille = None, couleurVerrouille = None):
        self.rect = pygame.Rect(x, y, 40, 60)
        if not couleurDeverouille:
            self.couleurDeverouille = ColorSelector.GREEN.value
        else:
            self.couleurDeverouille = couleurDeverouille
        if not couleurVerrouille:
            self.couleurVerrouillee = ColorSelector.BROWN.value
        else:
            self.couleurVerrouillee = couleurVerrouille

    def dessiner(self, surface, deverouillee):
        couleur = self.couleurDeverouille if deverouillee else self.couleurVerrouillee
        pygame.draw.rect(surface, couleur, self.rect)