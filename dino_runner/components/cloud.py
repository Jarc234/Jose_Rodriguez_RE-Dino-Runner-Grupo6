from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH
from pygame.sprite import Sprite
import random

class Cloud(Sprite):
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
        self.game_speed = 20
        

    def update(self):
        self.x += self.game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 200) 

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))