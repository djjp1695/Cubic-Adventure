import pygame
import sys

from Menus.Menus import PauseMenu, EndMenu
from Objets.Joueur import Joueur
from Utilitaires.ColorSelector import ColorSelector
from Utilitaires.MusicHandler import MusicHandler
from Objets.Nuage import Nuage
from Objets.Piece import Piece
from Objets.Porte import Porte
from Objets.Ennemie import Ennemie
from Objets.Cle import Cle

HAUTEUR = 800
LARGEUR = 600
TITRE = 'Cubic Adventure'
FPS = 60
POINTAGE = 'Pointage'
VIE = 'Vie'
CLE = 'Clé ramasée'
GAMEOVER = 'Vous avez perdu!'
VICTOIRE = "Vous avez gagné!"
SCORE_FINAL = "Score final"
PS5_CONTROLLER_NAME = "DualSense Wireless Controller"
XBOX_CONTROLLER_NAME = "Xbox Series X Controller"


class Game:
    __musicHandler = None
    def __init__(self):
        self.__musicHandler = MusicHandler()
        if len(self.__musicHandler.errorsList) > 0:
            if len(self.__musicHandler.errorsList) == 1:
                print("Problème de musique avec le son suivant : ")
            else :
                print("Problème de musique avec les sons suivants : ")

            [print(e) for e in self.__musicHandler.errorsList]
        self.hat_x = None
        self.joystick_axis_x = None
        self.__musicHandler.__init__()
        # --- Initialization ---
        pygame.init()
        self.initialize_joystick()

        self.HAUTEUR, self.LARGEUR = HAUTEUR, LARGEUR
        self.screen = pygame.display.set_mode((self.HAUTEUR, self.LARGEUR))
        self.pause_menu = PauseMenu(self.screen, self.reset_game)
        self.end_menu = EndMenu(self.screen, self.reset_game)

        pygame.display.set_caption(TITRE)
        self.clock = pygame.time.Clock()
        self.FPS = FPS

        # --- Polices ---
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 72)

        self.game_won = False
        self.game_over = False
        self.joueur = Joueur(self.LARGEUR)
        self.initialiser_les_objets_de_jeu()

    def initialiser_les_objets_de_jeu(self):
        # --- Platformes ---
        self.plateformes = [
            pygame.Rect(0, self.LARGEUR - 40, self.HAUTEUR, 40),
            pygame.Rect(200, 450, 200, 20),
            pygame.Rect(450, 350, 200, 20),
            pygame.Rect(150, 250, 150, 20),
        ]

        # --- Objets ---
        self.ennemies = [
            Ennemie(230, 410, 200, 400),
            Ennemie(480, 310, 450, 650),
        ]

        self.pieces = [
            Piece(260, 410),
            Piece(300, 410),
            Piece(520, 310),
            Piece(580, 310),
            Piece(180, 210),
        ]

        self.cle = Cle(600, 180)
        self.porte = Porte(720, self.LARGEUR - 100)
        self.nuages = [Nuage(self.HAUTEUR) for _ in range(6)]

    """Fonction pour supporter l'utilisation d'une manette"""

    def initialize_joystick(self):
        # Initialise les fonctions de base de Pygame pour une manette
        pygame.joystick.init()
        # Si au moins une manette est trouvée, initialise cette manette pour permettre son utilisation
        if pygame.joystick.get_count() > 0:
            self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in self.joysticks:
                joystick.init()
                print(f"Connected Joystick : {joystick.get_name()}")

    """Remets les paramètres du jeu à leur valeurs initiales, afin de permettre de commencer une nouvelle partie"""

    def reset_game(self):
        self.__musicHandler.__init__()
        # Réinitialiser score et vies
        self.pause_menu.close_menu()
        self.game_won = False
        self.game_over = False
        self.joueur.reset()

        # Réinitialiser pièces, clé et ennemis
        for piece in self.pieces:
            piece.recupere = False

        self.cle.recuperee = False
        for enn in self.ennemies:
            enn.en_vie = True

    """Gère les actions faites sur la manette, Button (si un bouton est pressé), Axis (pour le joystick), Hat pour la croix
    directionnelle"""

    def handle_joystick(self, controller=None, button=None, axis=None, hat=None):
        # Handle buttons
        controllerName = self.joysticks[controller].get_name()

        match button:
            case 0:
                # Vérifie si le joueur est sur le sol, empêche le double saut
                if self.joueur.sur_le_sol:
                    self.__musicHandler.play_jump_sound()
                    self.joueur.vel_y = -self.joueur.force_saut
                    self.joueur.sur_le_sol = False
            case 6:
                if controllerName == PS5_CONTROLLER_NAME:
                    self.pause_menu.show_menu()
            case 7:
                if controllerName == XBOX_CONTROLLER_NAME:
                    self.pause_menu.show_menu()


        # Si un axis est présent associe sa valeur à la variable joystick_axis_x
        if axis is not None and axis.axis == 0:
            if abs(axis.value):
                self.joystick_axis_x = axis.value
        if hat:
            self.hat_x = hat.value[0]

    """Gère les touches du clavier et détecte les demandes de déplacement du personnage"""

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Initialisation à zéro par défaut (aucun déplacement)
        self.joueur.vel_x = 0

        if self.hat_x:
            if self.hat_x == 1:
                # Si plus petit que la largeur de l'écran, permets de se déplacer vers la gauche (pour empêcher de sortir de l'écran)
                if self.joueur.rect.centerx < self.HAUTEUR:
                    self.joueur.vel_x = self.joueur.vitesse
            elif self.hat_x == -1:
                # Si plus grand que 0, permets de se déplacer vers la droite (pour empêcher de sortir de l'écran)
                if self.joueur.rect.centerx > 0:
                    self.joueur.vel_x = -self.joueur.vitesse

        if self.joystick_axis_x:
            if self.joystick_axis_x >= 1:
                if self.joueur.rect.centerx < self.HAUTEUR:
                    self.joueur.vel_x = self.joueur.vitesse
            elif self.joystick_axis_x <= -1:
                if self.joueur.rect.centerx > 0:
                    self.joueur.vel_x = -self.joueur.vitesse
        if keys[pygame.K_LEFT]:
            if self.joueur.rect.centerx > 0:
                self.joueur.vel_x = -self.joueur.vitesse
        if keys[pygame.K_RIGHT]:
            if self.joueur.rect.centerx < self.HAUTEUR:
                self.joueur.vel_x = self.joueur.vitesse
        if keys[pygame.K_SPACE] and self.joueur.sur_le_sol:
            if self.__musicHandler:
                self.__musicHandler.play_jump_sound()
            self.joueur.vel_y = -self.joueur.force_saut
            self.joueur.sur_le_sol = False
        if keys[pygame.K_ESCAPE]:
            self.pause_menu.show_menu()

    """Fonction appelée à chaque secondes (boucle) pour rafraichir l'écran et faire bouger le personnage principal"""

    def update_player(self):
        self.joueur.rect.x += self.joueur.vel_x
        self.joueur.vel_y += self.joueur.gravity
        self.joueur.rect.y += self.joueur.vel_y

        # Détecte si le joueur est sur une plateforme, si oui, mets le statut on_ground à vrai
        self.joueur.sur_le_sol = False
        for plateforme in self.plateformes:
            if self.joueur.rect.colliderect(plateforme) and self.joueur.vel_y > 0:
                self.joueur.rect.bottom = plateforme.top
                self.joueur.vel_y = 0
                self.joueur.sur_le_sol = True

    # Si l'ennemie est touché par un saut sur celui-çi, il est tué, le score est mis à jour et un son est joué.
    # Si l'ennemie nous touche on perd une vie
    def update_enemies(self):
        for ennemie in self.ennemies:
            ennemie.mettre_a_jour()
            if ennemie.en_vie and self.joueur.rect.colliderect(ennemie.rect):
                if self.joueur.vel_y > 0 and self.joueur.rect.bottom - ennemie.rect.top < 15:
                    ennemie.en_vie = False
                    self.joueur.vel_y = -10
                    self.joueur.score += 100
                    self.__musicHandler.play_enemy_kill_sound()
                else:
                    self.joueur.vies -= 1
                    self.joueur.rect.topleft = self.joueur.point_de_reapparition
                    if self.joueur.vies <= 0:
                        self.game_over = True

    # S'il y a une collision entre le personnage et une pièce, la pièce est retirée de l'écran et le pointage est
    # mis à jour avec 10 points de plus
    def update_coins(self):
        for piece in self.pieces:
            if not piece.recupere and self.joueur.rect.colliderect(piece.rect):
                piece.recupere = True
                self.joueur.score += 10

    # Si le personnage entre en collision avec la clé, elle est retirée de l'écran.
    # Le status recupérée est mis à True et la porte est dévérouillée
    def update_key_and_door(self):
        if not self.cle.recuperee and self.joueur.rect.colliderect(self.cle.rect):
            self.cle.recuperee = True
            self.joueur.a_la_cle = True

        if self.joueur.a_la_cle and self.joueur.rect.colliderect(self.porte.rect):
            self.game_won = True

    # Permets au nuages de bouger à l'écran
    def update_clouds(self):
        for nuage in self.nuages:
            nuage.mettre_a_jour()

    """Mets le fond de l'écran en bleu ciel,
    Ajoute les nuages à l'écran
    Ajoute les plateformes et les ennemies sur celles-çi
    Dessine les pièces à l'écran, la clé et la porte
    Affiche le score, le nombre de vie(s), ainsi que si la clé est récupérée
    """

    def draw(self):
        self.screen.fill(ColorSelector.SKY_BLUE.value)

        for nuage in self.nuages:
            nuage.dessiner(self.screen)

        for platform in self.plateformes:
            pygame.draw.rect(self.screen, ColorSelector.GREEN.value, platform)

        pygame.draw.rect(self.screen, ColorSelector.BLUE.value, self.joueur.rect)

        for enemy in self.ennemies:
            enemy.dessiner(self.screen)

        for piece in self.pieces:
            piece.dessiner(self.screen)

        self.cle.dessiner(self.screen)
        self.porte.dessiner(self.screen, self.joueur.a_la_cle)

        # HUD
        self.screen.blit(self.font.render(f"{POINTAGE}: {self.joueur.score}", True, ColorSelector.BLACK.value),
                         (10, 10))
        self.screen.blit(
            self.font.render(f"{VIE + 's' if self.joueur.vies > 1 else VIE}: {self.joueur.vies}", True,
                             ColorSelector.BLACK.value),
            (10, 45))
        self.screen.blit(
            self.font.render(f"{CLE}: {'Oui' if self.joueur.a_la_cle else 'Non'}", True, ColorSelector.BLACK.value),
            (10, 80))

        # Mets à jour l'écran avec les nouvelles valeurs (ex. Score) obtenus
        pygame.display.flip()

    """Fonction en boucle, qui contrôle l'éxécution du jeu"""

    def run(self):
        running = True
        while running:
            # Définis un rafraichissiment de l'écran à toutes les x secondes, dans notre cas 60 FPS
            self.clock.tick(self.FPS)

            # Pygame fonction par évènement, donc si event = QUIT on arrête la boucle
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    # Détecte la pression d'un bouton de la manette
                    case pygame.JOYBUTTONDOWN:
                        print(event)
                        self.handle_joystick(controller=event.joy,button=event.button)
                    # Détecte un mouvement de l'axe de mouvement du Joystick
                    case pygame.JOYAXISMOTION:
                        self.handle_joystick(controller=event.joy,axis=event)
                    # Détecte si la croix directionnelle de la manette est présée
                    case pygame.JOYHATMOTION:
                        self.handle_joystick(controller=event.joy,hat=event)

            # Si la partie est terminée (autant en défaite, que victoire affiche un écran avec le score)
            # et l'état de fin de la partie
            if self.game_over or self.game_won:
                self.display_end_screen()
                # continue
            self.handle_input()
            self.update_player()
            self.update_enemies()
            self.update_coins()
            self.update_key_and_door()
            self.update_clouds()
            self.draw()

        pygame.quit()
        sys.exit()

    # Affiche l'écran de fin de partie avec le score, victoire (joue la musique de victoire)
    # ou défaite (joue la musique de défaite)
    # Si une touche est présée sur la manette ou le clavier, on affiche le menu pour quitter
    # ou recommencer une partie
    def display_end_screen(self):
        self.screen.fill(ColorSelector.SKY_BLUE.value)
        message = VICTOIRE if self.game_won else GAMEOVER
        text = self.big_font.render(message, True,
                                    ColorSelector.GREEN.value if self.game_won else ColorSelector.RED.value)

        score_text = self.font.render(f"{SCORE_FINAL}: {self.joueur.score}", True, ColorSelector.BLACK.value)
        self.screen.blit(text, (self.LARGEUR / 4, self.LARGEUR / 2 - 60))
        self.screen.blit(score_text, (self.LARGEUR / 2, self.LARGEUR / 2))
        pygame.display.flip()
        if not self.game_won:
            self.__musicHandler.play_game_over_sound()
        else:
            self.__musicHandler.play_win_music()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.end_menu.show_menu()
                    waiting = False
                if event.type == pygame.JOYBUTTONDOWN:
                    self.end_menu.show_menu()
                    waiting = False
            self.clock.tick(self.FPS)


# Fonction principale pour l'éxécution du programme (jeu)
if __name__ == "__main__":
    game = Game()
    game.run()
