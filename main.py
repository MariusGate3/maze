from maze import Maze
import config
import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Maze")
    pygame.key.set_repeat(300, 50)
    running = True
    maze_list = []

    maze1 = Maze(20, 20, 20, position=(0, 0))  # First maze at (0, 0)
    maze2 = Maze(20, 20, 20, position=(650, 0))  # Second maze at (650, 0)

    maze_list.append(maze1)
    maze_list.append(maze2)

    maze1.generate()
    maze2.generate()

    maze1.solve_maze(algorithm="bfs")
    maze2.solve_maze(algorithm="dfs")

    maze1_visualized = False
    maze2_visualized = False

    path_traversal_started = False
    pygame.display.flip()
    while running:
        config.screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not maze1_visualized:
                        visualize_mazes(maze_list, 5)

                maze1.update_maze(event)
                maze2.update_maze(event)

        maze1.draw(config.screen)
        maze2.draw(config.screen)
        pygame.display.flip()


def visualize_mazes(maze_list, delay):
    maze_steps = [0] * len(maze_list)
    maze_path_steps = [0] * len(maze_list)
    completed = [False] * len(maze_list)
    solved_mazes = 0

    while solved_mazes < len(maze_list):
        config.screen.fill((0, 0, 0))
        for i, maze in enumerate(maze_list):
            if not completed[i]:
                step = maze_steps[i]
                if step < len(maze.checked_cells):
                    cell = maze.checked_cells[step]
                    maze.grid[cell[1]][cell[0]].algo_visited = True
                    maze_steps[i] += 1
                elif step == len(maze.checked_cells):
                    path_step = maze_path_steps[i]
                    if path_step < len(maze.solved_path):
                        cell = maze.solved_path[path_step]
                        maze.grid[cell[1]][cell[0]].traversed = True
                        maze_path_steps[i] += 1
                    else:
                        print("Maze solved")
                        solved_mazes += 1
                        print(f"solved_mazes", solved_mazes)
                        print("amount of mazes", len(maze_list))
                        completed[i] = True
            maze.draw(config.screen)
        pygame.display.flip()
        pygame.time.delay(delay)


if __name__ == "__main__":
    main()
    pygame.quit()
