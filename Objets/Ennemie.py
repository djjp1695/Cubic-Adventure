import pygame

from Utilitaires.ColorSelector import ColorSelector


class Ennemie:
    def __init__(self, x, y, bond_gauche, bond_droit, couleur=None):
        # Si aucune couleur en paramètre Rouge par défaut
        if not couleur:
            self.couleur = ColorSelector.RED.value
        else:
            self.couleur = couleur.value
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vitesse = 2
        self.direction = 1
        self.bond_gauche = bond_gauche
        self.bond_droit = bond_droit
        self.en_vie = True

    def mettre_a_jour(self):
        if  self.en_vie:
            self.rect.x += self.vitesse * self.direction
            if self.rect.left <= self.bond_gauche or self.rect.right >= self.bond_droit:
                self.direction *= -1

    def dessiner(self, surface):
        if self.en_vie:
            pygame.draw.rect(surface, self.couleur, self.rect)
