import pygame, sys
# import constants
from settings import *
from level import Level

# Working off of https://www.youtube.com/watch?v=QU1pPzEGrqw&list=PLaypYuEnN7oid8E0lZaB8HDWuXckTcjVP&index=15

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('The Grim Adventures of Drizzt')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update() 
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()