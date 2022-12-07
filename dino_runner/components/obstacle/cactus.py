from dino_runner.components.obstacle.obstacle import obstalce
import random

class Cactus(obstalce):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325