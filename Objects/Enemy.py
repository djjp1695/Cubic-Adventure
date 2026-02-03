import pygame
RED = (255, 0, 0)
class Enemy:
    def __init__(self, x, y, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2
        self.direction = 1
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.speed * self.direction
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.direction *= -1

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, RED, self.rect)