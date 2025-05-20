import pygame

from game.game_manager import GameManager

if __name__ == "__main__":
    pygame.init()

    game_manager = GameManager()

    while game_manager.is_running():
        game_manager.update()
        game_manager.render()

    pygame.quit()