import pygame
import sys
import pygame_menu
from pygame.examples.cursors import surf

from Menus.Menus import PauseMenu, EndMenu
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


class Game:
    def __init__(self):
        self.__musicHandler = MusicHandler()
        self.__musicHandler.__init__()
        # --- Initialization ---
        pygame.init()
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

        # --- Score & Lives ---
        self.score = 0
        self.vies = 3
        self.a_la_clé = False
        self.game_won = False
        self.game_over = False

        # --- Player ---
        self.player_rect = pygame.Rect(100, self.LARGEUR - 100, 40, 60)
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.vitesse = 5
        self.force_saut = 15
        self.gravity = 0.8
        self.on_ground = False
        self.spawn_point = (100, self.LARGEUR - 100)

        # --- Platforms ---
        self.platforms = [
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

    def reset_game(self):
        self.__musicHandler.__init__()
        # Réinitialiser score et vies
        self.pause_menu.close_menu()

        self.score = 0
        self.vies = 3
        self.a_la_clé = False
        self.game_won = False
        self.game_over = False

        # Réinitialiser position du joueur
        self.player_rect.topleft = self.spawn_point
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.on_ground = False

        # Réinitialiser pièces, clé et ennemis
        for piece in self.pieces:
            piece.recupere = False

        self.cle.recuperee = False
        for enn in self.ennemies:
            enn.en_vie = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player_vel_x = 0
        if keys[pygame.K_LEFT]:
            if self.player_rect.centerx > 0:
                self.player_vel_x = -self.vitesse
        if keys[pygame.K_RIGHT]:
            if self.player_rect.centerx < self.HAUTEUR:
                self.player_vel_x = self.vitesse
        if keys[pygame.K_SPACE] and self.on_ground:
            self.player_vel_y = -self.force_saut
            self.on_ground = False
        if keys[pygame.K_ESCAPE]:
           self.pause_menu.show_menu()
        if keys[pygame.K_r]:
            self.reset_game()

    def update_player(self):
        self.player_rect.x += self.player_vel_x
        self.player_vel_y += self.gravity
        self.player_rect.y += self.player_vel_y

        # Platform collision
        self.on_ground = False
        for platform in self.platforms:
            if self.player_rect.colliderect(platform) and self.player_vel_y > 0:
                self.player_rect.bottom = platform.top
                self.player_vel_y = 0
                self.on_ground = True

    def update_enemies(self):
        for ennemie in self.ennemies:
            ennemie.mettre_a_jour()
            if ennemie.en_vie and self.player_rect.colliderect(ennemie.rect):
                if self.player_vel_y > 0 and self.player_rect.bottom - ennemie.rect.top < 15:
                    ennemie.en_vie = False
                    self.player_vel_y = -10
                    self.score += 100
                else:
                    self.vies -= 1
                    self.player_rect.topleft = self.spawn_point
                    if self.vies <= 0:
                        self.game_over = True

    def update_coins(self):
        for piece in self.pieces:
            if not piece.recupere and self.player_rect.colliderect(piece.rect):
                piece.recupere = True
                self.score += 10

    def update_key_and_door(self):
        if not self.cle.recuperee and self.player_rect.colliderect(self.cle.rect):
            self.cle.recuperee = True
            self.a_la_clé = True

        if self.a_la_clé and self.player_rect.colliderect(self.porte.rect):
            self.game_won = True

    def update_clouds(self):
        for nuage in self.nuages:
            nuage.mettre_a_jour()

    def draw(self):
        self.screen.fill(ColorSelector.SKY_BLUE.value)

        for nuage in self.nuages:
            nuage.dessiner(self.screen)

        for platform in self.platforms:
            pygame.draw.rect(self.screen, ColorSelector.GREEN.value, platform)

        pygame.draw.rect(self.screen, ColorSelector.BLUE.value, self.player_rect)

        for enemy in self.ennemies:
            enemy.dessiner(self.screen)

        for piece in self.pieces:
            piece.draw(self.screen)

        self.cle.dessiner(self.screen)
        self.porte.dessiner(self.screen, self.a_la_clé)

        # HUD
        self.screen.blit(self.font.render(f"{POINTAGE}: {self.score}", True, ColorSelector.BLACK.value), (10, 10))
        self.screen.blit(
            self.font.render(f"{VIE + 's' if self.vies > 1 else VIE}: {self.vies}", True, ColorSelector.BLACK.value),
            (10, 45))
        self.screen.blit(
            self.font.render(f"{CLE}: {'Oui' if self.a_la_clé else 'Non'}", True, ColorSelector.BLACK.value),
            (10, 80))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.game_over or self.game_won:
                self.display_end_screen()
                continue


            self.handle_input()
            self.update_player()
            self.update_enemies()
            self.update_coins()
            self.update_key_and_door()
            self.update_clouds()
            self.draw()

        pygame.quit()
        sys.exit()

    def display_end_screen(self):
        self.screen.fill(ColorSelector.SKY_BLUE.value)
        message = VICTOIRE if self.game_won else GAMEOVER
        text = self.big_font.render(message, True,
                                    ColorSelector.GREEN.value if self.game_won else ColorSelector.RED.value)

        score_text = self.font.render(f"{SCORE_FINAL}: {self.score}", True, ColorSelector.BLACK.value)
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

            self.clock.tick(self.FPS)

# --- Run the Game ---
if __name__ == "__main__":
    game = Game()
    game.run()
