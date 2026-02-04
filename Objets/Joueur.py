import pygame

NB_VIES = 3
SCORE = 0
VEL_X =0
VEL_Y = 0
VITESSE = 5
FORCE_SAUT = 15
GRAVITE = 0.8

"""Classe qui initialise le joueur à l'écran et offre l'option de réinitialiser le status pour une nouvelle partie"""
class Joueur:
    def __init__(self, largeur):
        self.vies = NB_VIES
        self.a_la_cle = False
        self.score = SCORE
        self.rect = pygame.Rect(100, largeur - 100, 40, 60)
        self.vel_x = VEL_X
        self.vel_y = VEL_Y
        self.vitesse = VITESSE
        self.force_saut = FORCE_SAUT
        self.gravity = GRAVITE
        self.sur_le_sol = False
        self.point_de_reapparition = (100, largeur - 100)

    def reset(self):
        self.score = SCORE
        self.vies = NB_VIES
        self.a_la_cle = False
        self.rect.topleft = self.point_de_reapparition
        self.vel_x = VEL_X
        self.vel_y = VEL_Y
        self.sur_le_sol = False
