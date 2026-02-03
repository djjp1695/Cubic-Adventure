from pygame import mixer
import pygame
import sys

from MusicHandler import MusicHandler
from Objects.Clouds import Cloud
from Objects.Coin import Coin
from Objects.Door import Door
from Objects.Enemy import Enemy
from Objects.Key import Key

class Game:
    def __init__(self):
        self.__musicHandler = MusicHandler()
        self.__musicHandler.__init__()
        # --- Initialization ---
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mario-Style Platformer with Key")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # --- Colors ---
        self.SKY_BLUE = (135, 206, 235)
        self.BLUE = (50, 150, 255)
        self.GREEN = (50, 200, 50)
        self.RED = (220, 60, 60)
        self.YELLOW = (255, 215, 0)
        self.PURPLE = (150, 80, 200)
        self.BROWN = (120, 70, 30)
        self.BLACK = (0, 0, 0)

        # --- Fonts ---
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

        # --- Objects ---
        self.enemies = [
            Enemy(230, 410, 200, 400),
            Enemy(480, 310, 450, 650),
        ]

        self.coins = [
            Coin(260, 410),
            Coin(300, 410),
            Coin(520, 310),
            Coin(580, 310),
            Coin(180, 210),
        ]

        self.key = Key(600, 180)
        self.door = Door(720, self.HEIGHT - 100)
        self.clouds = [Cloud(self.WIDTH) for _ in range(6)]
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
        for enemy in self.enemies:
            enemy.update()
            if enemy.alive and self.player_rect.colliderect(enemy.rect):
                if self.player_vel_y > 0 and self.player_rect.bottom - enemy.rect.top < 15:
                    enemy.alive = False
                    self.player_vel_y = -10
                    self.score += 100
                else:
                    self.lives -= 1
                    self.player_rect.topleft = self.spawn_point
                    if self.lives <= 0:
                        self.game_over = True

    def update_coins(self):
        for coin in self.coins:
            if not coin.collected and self.player_rect.colliderect(coin.rect):
                coin.collected = True
                self.score += 10

    def update_key_and_door(self):
        if not self.key.collected and self.player_rect.colliderect(self.key.rect):
            self.key.collected = True
            self.has_key = True

        if self.has_key and self.player_rect.colliderect(self.door.rect):
            self.game_won = True
    def update_clouds(self):
        for cloud in self.clouds:
            cloud.update()

    def draw(self):
        self.screen.fill(self.SKY_BLUE)

        for cloud in self.clouds:
            cloud.draw(self.screen)

        for platform in self.platforms:
            pygame.draw.rect(self.screen, self.GREEN, platform)

        pygame.draw.rect(self.screen, self.BLUE, self.player_rect)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        self.key.draw(self.screen)
        self.door.draw(self.screen, self.has_key)

        # HUD
        self.screen.blit(self.font.render(f"Score: {self.score}", True, self.BLACK), (10, 10))
        self.screen.blit(self.font.render(f"Lives: {self.lives}", True, self.BLACK), (10, 45))
        self.screen.blit(self.font.render(f"Key: {'Yes' if self.has_key else 'No'}", True, self.BLACK), (10, 80))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.game_over or self.game_won:
                self.screen.fill(self.SKY_BLUE)
                message = "YOU WIN!" if self.game_won else "GAME OVER"
                text = self.big_font.render(message, True, self.GREEN if self.game_won else self.RED)
                score_text = self.font.render(f"Final Score: {self.score}", True, self.BLACK)
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
