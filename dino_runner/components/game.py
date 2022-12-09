import pygame
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, RUNNING, GAME_OVER, RETRY
from dino_runner.components.dinosaur.dinosaur import Dinosaur
from dino_runner.components.obstacle.obstacleManager import ObstacleManager
from dino_runner.components.score_menu.text_utils import *
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.powerups.power_up_manager import PowerUpManager
from dino_runner.components.cloud import Cloud

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.cloud = Cloud()
        self.points = 0
        self.best_score = 0
        self.running = True
        self.death_count = 0
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()
        self.sound_game = pygame.mixer.music.load('dino_runner/assets/Other/Like A Dino.ogg')

    def run(self):
        self.obstacle_manager.reset_obstacles(self)
        self.player_heart_manager.reset_hearts()
        self.game_speed = 20
        self.points = 0
        self.power_up_manager.reset_power_ups(self.points)
        self.playing = True
        if self.playing:
            self.sound_game = pygame.mixer.music.play(-1)
        while self.playing:
            self.events()
            self.update()
            self.draw()
        if self.playing == False:
            self.sound_game = pygame.mixer.music.stop()
        #pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.cloud.update()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score()
        self.cloud.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
    
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1

        if self.points % 100 == 0:
            self.game_speed += 1

        if self.points > self.best_score:
            self.best_score = self.points
        score, score_rect = get_score_element(self.points)
        self.screen.blit(score, score_rect)
        self.player.check_invincibility(self.screen)

    def show_menu(self):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements(self.death_count)
        pygame.display.update()

        self.handle_key_events_on_menu()

    def print_menu_elements(self, death_count = 0):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if death_count == 0:
            text, text_rect = get_centered_message('Press any Key to Start')
            self.screen.blit(text, text_rect)
            self.screen.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 -140))
        elif death_count > 0:
            text, text_rect = get_centered_message('Press any Key to Restart')
            score, score_rect = get_centered_message('Your Score: '+ str(self.points), height = half_screen_height + 50)
            best_score, best_rect = get_centered_message('You Best Score: '+ str(self.best_score), height = half_screen_height + 100 )
            self.screen.blit(GAME_OVER, (SCREEN_WIDTH // 2 - 185, SCREEN_HEIGHT // 2 - 140))
            self.screen.blit(RETRY, (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 150))
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(best_score, best_rect)

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Dino: Good Bye!!")
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()
                
                
