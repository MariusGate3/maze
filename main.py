from maze import Maze
import config
import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Maze")
    running = True
    maze = Maze(30, 20, 30)
    maze.generate()
    maze.draw(config.screen)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        config.screen.fill((0, 0, 0))
        maze.draw(config.screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
