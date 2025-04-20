from cell import cell
import pygame
import random
import config


class Maze:

    def __init__(
        self, width, height, cell_size, start_cell=(0, 0), border=100, position=(0, 0)
    ):
        self.start_cell = start_cell
        self.end_cell = (width - 1, height - 1)
        self.current_cell = start_cell
        self.border = border
        self.cell_size = cell_size
        self.position = position
        self.grid = [
            [cell(x * self.cell_size, y * self.cell_size) for x in range(width)]
            for y in range(height)
        ]
        self.visited = []
        self.width = width
        self.height = height
        self.solved_path = []
        self.checked_cells = []
        self.algorithm = None

    def generate(self):
        start = random.choice(self.grid[0])
        start.walls[0] = False
        start.visited = True
        self.visited.append(start)
        while len(self.visited) < len(self.grid) * len(self.grid[0]):
            randomCell = random.choice(self.visited)
            neighbors = self.get_not_visited_neighbors(randomCell)
            if neighbors:
                neighbor = random.choice(neighbors)
                self.remove_walls(randomCell, neighbor)
                neighbor.visited = True
                self.visited.append(neighbor)

    def remove_walls(self, cell_1, cell_2):
        x1, y1 = cell_1.x // self.cell_size, cell_1.y // self.cell_size
        x2, y2 = cell_2.x // self.cell_size, cell_2.y // self.cell_size

        if x1 == x2:
            if y1 == y2 + 1:
                cell_1.walls[0] = False
                cell_2.walls[2] = False
            elif y1 == y2 - 1:
                cell_1.walls[2] = False
                cell_2.walls[0] = False
        elif y1 == y2:
            if x1 == x2 + 1:
                cell_1.walls[3] = False
                cell_2.walls[1] = False
            elif x1 == x2 - 1:
                cell_1.walls[1] = False
                cell_2.walls[3] = False

    def get_not_visited_neighbors(self, cell):
        neighbors = []
        x, y = cell.x // self.cell_size, cell.y // self.cell_size
        if x > 0:
            neighbors.append(self.grid[y][x - 1])
        if x < self.width - 1:
            neighbors.append(self.grid[y][x + 1])
        if y > 0:
            neighbors.append(self.grid[y - 1][x])
        if y < self.height - 1:
            neighbors.append(self.grid[y + 1][x])
        return [n for n in neighbors if n not in self.visited]

    def update_maze(self, event):
        if event.key == pygame.K_UP:
            if (
                self.current_cell[1] > 0
                and not self.grid[self.current_cell[1]][self.current_cell[0]].walls[0]
            ):
                self.current_cell = (self.current_cell[0], self.current_cell[1] - 1)
        elif event.key == pygame.K_DOWN:
            if (
                self.current_cell[1] < self.height - 1
                and not self.grid[self.current_cell[1]][self.current_cell[0]].walls[2]
            ):
                self.current_cell = (self.current_cell[0], self.current_cell[1] + 1)
        elif event.key == pygame.K_LEFT:
            if (
                self.current_cell[0] > 0
                and not self.grid[self.current_cell[1]][self.current_cell[0]].walls[3]
            ):
                self.current_cell = (self.current_cell[0] - 1, self.current_cell[1])
        elif event.key == pygame.K_RIGHT:
            if (
                self.current_cell[0] < self.width - 1
                and not self.grid[self.current_cell[1]][self.current_cell[0]].walls[1]
            ):
                self.current_cell = (self.current_cell[0] + 1, self.current_cell[1])
        self.grid[self.current_cell[1]][self.current_cell[0]].traversed = True

    def solve_maze(self, algorithm="bfs"):
        self.algorithm = algorithm
        if algorithm == "bfs":
            path = self.bfs((0, 0), self.end_cell)
        elif algorithm == "dfs":
            path = self.dfs((0, 0), self.end_cell)
        elif algorithm == "a_star":
            path = self.a_star((0, 0), self.end_cell)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def visuzalize_checked_cells(self, delay):
        for cell in self.checked_cells:
            self.grid[cell[1]][cell[0]].algo_visited = True
            self.draw(config.screen)
            pygame.display.flip()
            pygame.time.delay(delay)

        for cell in self.solved_path:
            self.grid[cell[1]][cell[0]].traversed = True
            self.draw(config.screen)
            pygame.display.flip()
            pygame.time.delay(delay)

    def bfs(self, start, end):
        from collections import deque

        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()
            self.checked_cells.append(current)

            if current == end:
                break

            x, y = current
            neighbors = self.get_neighbors(x, y)
            for neighbor in neighbors:
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        self.solved_path = path
        return path

    def dfs(self, start, end):
        stack = [start]
        came_from = {start: None}

        while stack:
            current = stack.pop()
            self.checked_cells.append(current)

            if current == end:
                break

            x, y = current
            neighbors = self.get_neighbors(x, y)
            for neighbor in neighbors:
                if neighbor not in came_from:
                    stack.append(neighbor)
                    came_from[neighbor] = current

        path = []
        current = end
        while current:
            path.append(current)
            current = came_from[current]
        path.reverse()
        self.solved_path = path
        return path

    def a_star(self, start, end):
        from heapq import heappop, heappush

        open_set = []
        heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_set:
            _, current = heappop(open_set)
            self.checked_cells.append(current)

            if current == end:
                break

            x, y = current
            neighbors = self.get_neighbors(x, y)
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(
                        neighbor, end
                    )
                    heappush(open_set, (f_score[neighbor], neighbor))

        path = []
        current = end
        while current:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        self.solved_path = path
        return path

    def heuristic(self, a, b):
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, x, y):
        neighbors = []
        if y > 0 and not self.grid[y][x].walls[0]:
            neighbors.append((x, y - 1))
        if y < self.height - 1 and not self.grid[y][x].walls[2]:
            neighbors.append((x, y + 1))
        if x > 0 and not self.grid[y][x].walls[3]:
            neighbors.append((x - 1, y))
        if x < self.width - 1 and not self.grid[y][x].walls[1]:
            neighbors.append((x + 1, y))
        return neighbors

    def draw_text(self, screen, text_height=30, color=(255, 255, 255)):
        font = pygame.font.Font(None, 24)
        x, y = self.position
        text_surface = font.render(self.algorithm, True, color)
        screen.blit(text_surface, (x, y - text_height))

    def draw(self, screen):
        offset_x, offset_y = self.position
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                cell_x = cell.x + offset_x
                cell_y = cell.y + offset_y
                if (col_index, row_index) == self.current_cell:
                    pygame.draw.rect(
                        screen,
                        (0, 0, 128),
                        (cell_x, cell_y, self.cell_size, self.cell_size),
                    )
                elif cell.traversed:
                    pygame.draw.rect(
                        screen,
                        (0, 0, 255),
                        (cell_x, cell_y, self.cell_size, self.cell_size),
                    )
                elif cell.algo_visited:
                    pygame.draw.rect(
                        screen,
                        (200, 200, 0),
                        (cell_x, cell_y, self.cell_size, self.cell_size),
                    )
                if (row_index, col_index) == (0, 0):
                    pygame.draw.rect(
                        screen,
                        (0, 255, 0),
                        (cell_x, cell_y, self.cell_size, self.cell_size),
                    )
                if (col_index, row_index) == self.end_cell:
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0),
                        (cell_x, cell_y, self.cell_size, self.cell_size),
                    )
                if cell.walls[0]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell_x, cell_y),
                        (cell_x + self.cell_size, cell_y),
                    )
                if cell.walls[1]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell_x + self.cell_size, cell_y),
                        (cell_x + self.cell_size, cell_y + self.cell_size),
                    )
                if cell.walls[2]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell_x, cell_y + self.cell_size),
                        (cell_x + self.cell_size, cell_y + self.cell_size),
                    )
                if cell.walls[3]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell_x, cell_y),
                        (cell_x, cell_y + self.cell_size),
                    )
