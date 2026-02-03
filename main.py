from pygame import mixer
import pygame
import sys

from MusicHandler import MusicHandler
from Objets.Nuage import Nuage
from Objets.Piece import Piece
from Objets.Porte import Porte
from Objets.Ennemie import Ennemie
from Objets.Cle import Cle

SKY_BLUE = (135, 206, 235)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (220, 60, 60)
YELLOW = (255, 215, 0)
PURPLE = (150, 80, 200)
BROWN = (120, 70, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


HAUTEUR = 800
LARGEUR = 600
TITRE = 'Cubic Adventure'
FPS = 60

class Game:
    def __init__(self):
        self.__musicHandler = MusicHandler()
        self.__musicHandler.__init__()
        # --- Initialization ---
        pygame.init()
        self.WIDTH, self.HEIGHT = HAUTEUR, LARGEUR
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(TITRE)
        self.clock = pygame.time.Clock()
        self.FPS = FPS

        # --- Couleurs ---


        # --- Polices ---
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 72)

        # --- Score & Lives ---
        self.score = 0
        self.lives = 3
        self.has_key = False
        self.game_won = False
        self.game_over = False

        # --- Player ---
        self.player_rect = pygame.Rect(100, self.HEIGHT - 100, 40, 60)
        self.player_vel_x = 0
        self.player_vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.on_ground = False
        self.spawn_point = (100, self.HEIGHT - 100)

        # --- Platforms ---
        self.platforms = [
            pygame.Rect(0, self.HEIGHT - 40, self.WIDTH, 40),
            pygame.Rect(200, 450, 200, 20),
            pygame.Rect(450, 350, 200, 20),
            pygame.Rect(150, 250, 150, 20),
        ]

        # --- Objets ---
        self.ennemies = [
            Ennemie(230, 410, 200, 400, RED),
            Ennemie(480, 310, 450, 650, RED),
        ]

        self.pieces = [
            Piece(260, 410, YELLOW),
            Piece(300, 410, YELLOW),
            Piece(520, 310, YELLOW),
            Piece(580, 310, YELLOW),
            Piece(180, 210, YELLOW),
        ]

        self.cle = Cle(600, 180, YELLOW)
        self.porte = Porte(720, self.HEIGHT - 100)
        self.nuages = [Nuage(self.WIDTH, WHITE) for _ in range(6)]
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player_vel_x = 0
        if keys[pygame.K_LEFT]:
            self.player_vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.player_vel_x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.player_vel_y = -self.jump_power
            self.on_ground = False
        if keys[pygame.K_ESCAPE]:
            self.game_over = True

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
        for enemy in self.ennemies:
            enemy.mettre_a_jour()
            if enemy.en_vie and self.player_rect.colliderect(enemy.rect):
                if self.player_vel_y > 0 and self.player_rect.bottom - enemy.rect.top < 15:
                    enemy.en_vie = False
                    self.player_vel_y = -10
                    self.score += 100
                else:
                    self.lives -= 1
                    self.player_rect.topleft = self.spawn_point
                    if self.lives <= 0:
                        self.game_over = True

    def update_coins(self):
        for piece in self.pieces:
            if not piece.recupere and self.player_rect.colliderect(piece.rect):
                piece.recupere = True
                self.score += 10

    def update_key_and_door(self):
        if not self.cle.recuperee and self.player_rect.colliderect(self.cle.rect):
            self.cle.recuperee = True
            self.has_key = True

        if self.has_key and self.player_rect.colliderect(self.porte.rect):
            self.game_won = True
    def update_clouds(self):
        for cloud in self.nuages:
            cloud.mettre_a_jour()

    def draw(self):
        self.screen.fill(SKY_BLUE)

        for cloud in self.nuages:
            cloud.dessiner(self.screen)

        for platform in self.platforms:
            pygame.draw.rect(self.screen, GREEN, platform)

        pygame.draw.rect(self.screen, BLUE, self.player_rect)

        for enemy in self.ennemies:
            enemy.dessiner(self.screen)

        for piece in self.pieces:
            piece.draw(self.screen)

        self.cle.dessiner(self.screen)
        self.porte.dessiner(self.screen, self.has_key)

        # HUD
        self.screen.blit(self.font.render(f"Score: {self.score}", True, BLACK), (10, 10))
        self.screen.blit(self.font.render(f"Lives: {self.lives}", True, BLACK), (10, 45))
        self.screen.blit(self.font.render(f"Key: {'Yes' if self.has_key else 'No'}", True, BLACK), (10, 80))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.game_over or self.game_won:
                self.screen.fill(SKY_BLUE)
                message = "YOU WIN!" if self.game_won else "GAME OVER"
                text = self.big_font.render(message, True, GREEN if self.game_won else RED)
                score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
                self.screen.blit(text, (self.WIDTH // 2 - 160, self.HEIGHT // 2 - 60))
                self.screen.blit(score_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2 + 10))
                pygame.display.flip()
                if not self.game_won:
                    self.__musicHandler.play_game_over_sound()
                else :
                    self.__musicHandler.play_win_music()


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
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

# --- Run the Game ---
if __name__ == "__main__":
    game = Game()
    game.run()
