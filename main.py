import pygame

from game.game_manager import GameManager

if __name__ == "__main__":
    pygame.init()

    game_manager = GameManager()

    clock = pygame.time.Clock()

    while game_manager.is_running():
        game_manager.update()
        game_manager.render()
        clock.tick(60)

    pygame.quit()
