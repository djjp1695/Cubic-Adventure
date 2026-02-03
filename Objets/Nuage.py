import random
import pygame

from ColorSelector import ColorSelector


class Nuage:
    def __init__(self, width, couleur=None):
        self.largeur = width
        if not couleur:
            self.couleur = ColorSelector.WHITE.value
        else:
            self.couleur = couleur.value
        self.x = random.randint(0, self.largeur)
        self.y = random.randint(30, 200)
        self.vitesse = random.uniform(0.3, 1.0)

    def mettre_a_jour(self):
        self.x += self.vitesse
        if self.x > self.largeur + 60:
            self.x = -60
            self.y = random.randint(30, 200)

    def dessiner(self, surface):
        pygame.draw.circle(surface, self.couleur, (int(self.x), self.y), 20)
        pygame.draw.circle(surface, self.couleur, (int(self.x + 20), self.y + 10), 25)
        pygame.draw.circle(surface, self.couleur, (int(self.x + 40), self.y), 20)
