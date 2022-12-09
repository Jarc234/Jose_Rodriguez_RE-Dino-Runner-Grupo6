from dino_runner.components.obstacle.obstacle import obstalce
from dino_runner.utils.constants import BIRD, SCREEN_WIDTH

class Bird(obstalce):
    Y_pocision = 250
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = self.Y_pocision
        self.step_index = 0
    
    def draw(self, screen):
        if self.step_index >= 10:
            self.step_index = 0
        screen.blit(self.image[self.step_index // 5], self.rect)
        self.step_index += 1
        

