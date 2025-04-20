from maze import Maze
import config
import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Maze")
    pygame.key.set_repeat(300, 50)
    running = True
    maze_list = []

    maze_count = 3
    cell_size = 20
    text_height = 30

    maze_width, maze_height = calculate_maze_dimensions(
        config.window_x, config.window_y, maze_count, cell_size, text_height
    )

    positions = calculate_maze_positions(
        config.window_x, maze_count, maze_width, maze_height, cell_size, text_height
    )

    for position in positions:
        maze = Maze(maze_width, maze_height, cell_size, position=position)
        maze.generate()
        maze_list.append(maze)

    maze_list[0].solve_maze(algorithm="bfs")
    maze_list[1].solve_maze(algorithm="dfs")
    maze_list[2].solve_maze(algorithm="a_star")

    mazes_visualized = False

    path_traversal_started = False
    pygame.display.flip()

    while running:
        config.screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not mazes_visualized:
                        visualize_mazes(maze_list, 5)
                        mazes_visualized = True
                for maze in maze_list:
                    maze.update_maze(event)

        for maze in maze_list:
            maze.draw_text(config.screen, text_height)
            maze.draw(config.screen)
        pygame.display.flip()


def visualize_mazes(maze_list, delay):
    print("visualizing mazes")
    maze_steps = [0] * len(maze_list)
    maze_path_steps = [0] * len(maze_list)
    completed = [False] * len(maze_list)
    solved_mazes = 0

    while solved_mazes < len(maze_list):
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
                        if not completed[i]:
                            print("Maze solved")
                            solved_mazes += 1
                            print(f"solved_mazes", solved_mazes)
                            print("amount of mazes", len(maze_list))
                            completed[i] = True
            maze.draw_text(config.screen)
            maze.draw(config.screen)
        pygame.display.flip()
        pygame.time.delay(delay)


def calculate_maze_dimensions(
    window_width, window_height, maze_count, cell_size, text_height=30
):
    cols = maze_count
    rows = 1

    available_width = (window_width - (cols + 1) * cell_size) // cols
    available_height = window_height - text_height - 2 * cell_size

    maze_width = (available_width // cell_size) - 1
    maze_height = (available_height // cell_size) - 1

    return maze_width, maze_height


def calculate_maze_positions(
    window_width, maze_count, maze_width, maze_height, cell_size, text_height=30
):
    positions = []
    maze_pixel_width = maze_width * cell_size
    maze_pixel_height = maze_height * cell_size + text_height

    horizontal_spacing = (window_width - maze_count * maze_pixel_width) // (
        maze_count + 1
    )

    for i in range(maze_count):
        x = horizontal_spacing + i * (maze_pixel_width + horizontal_spacing)
        y = text_height + cell_size
        positions.append((x, y))

    return positions


if __name__ == "__main__":
    main()
    pygame.quit()
