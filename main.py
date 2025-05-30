import pygame, asyncio

from game.game_manager import GameManager

if __name__ == "__main__":
    pygame.init()

    game_manager = GameManager()
    game_manager.init()

    clock = pygame.time.Clock()

    async def game_loop():
        while game_manager.is_running():
            delta_time = clock.tick(60) / 1000.0

            game_manager.update(delta_time)
            game_manager.render()

            pygame.display.flip()
            await asyncio.sleep(0)

    asyncio.run(game_loop())

    pygame.quit()