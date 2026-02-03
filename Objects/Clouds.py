import random
import pygame
WHITE = (255, 255, 255)



class Cloud:
    def __init__(self, width):
        self.__width = width
        self.__color = WHITE
        self.x = random.randint(0, self.__width)
        self.y = random.randint(30, 200)
        self.speed = random.uniform(0.3, 1.0)

    def update(self):
        self.x += self.speed
        if self.x > self.__width + 60:
            self.x = -60
            self.y = random.randint(30, 200)

    def draw(self, surface):
        pygame.draw.circle(surface, self.__color, (int(self.x), self.y), 20)
        pygame.draw.circle(surface, self.__color, (int(self.x + 20), self.y + 10), 25)
        pygame.draw.circle(surface, self.__color, (int(self.x + 40), self.y), 20)