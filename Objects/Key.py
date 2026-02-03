import pygame
PURPLE = (0, 0, 255)
# --- Key class ---
class Key:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 30)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pygame.draw.rect(surface, PURPLE, self.rect)
