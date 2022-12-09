import pygame
import random

from dino_runner.components.obstacle.cactus import Cactus
from dino_runner.components.obstacle.cactus_large import LargeCactus
from dino_runner.components.obstacle.enemy import Enemy
from dino_runner.components.obstacle.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, DINO

class ObstacleManager:

    def __init__(self):
        self.obstacles = []
        self.dead = pygame.mixer.Sound('dino_runner/assets/Other/Dead Sound.ogg')
        self.type_obstacle = {1: SMALL_CACTUS, 2: LARGE_CACTUS, 3: DINO, 4: BIRD}

    def update(self, game):
        if len(self.obstacles) == 0:
            self.get_obstacle = random.randint(1, 4)
            if self.get_obstacle == 1:
                self.obstacles.append(Cactus(self.type_obstacle[self.get_obstacle]))
            elif self.get_obstacle == 2:
                self.obstacles.append(LargeCactus(self.type_obstacle[self.get_obstacle]))
            elif self.get_obstacle == 3:
                self.obstacles.append(Enemy(self.type_obstacle[self.get_obstacle]))
            elif self.get_obstacle == 4:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                #pygame.time.delay(500)
                #game.playing = False
                #break
                if not game.player.shield:
                    pygame.time.delay (100)
                    self.obstacles = []

                    game.player_heart_manager.reduce_heart()
                    if game.player_heart_manager.heart_count > 0:
                        game.player.shield = True
                        game.player.show_text = False
                        start_time = pygame.time.get_ticks()
                        game.player.shield_time_up = start_time + 1000
                    else:
                        self.dead.play()
                        pygame.time.delay(2000)
                        game.playing = False
                        game.death_count += 1
                        break
                
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self, self1):
        self.obstacles = []