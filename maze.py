from cell import cell
import pygame
import random


class Maze:

    def __init__(self, width, height, cell_size, border=100):
        self.border = border
        self.cell_size = cell_size
        self.grid = [
            [cell(x * self.cell_size, y * self.cell_size) for x in range(width)]
            for y in range(height)
        ]
        self.visited = []
        self.width = width
        self.height = height

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

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                # top wall
                if cell.walls[0]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell.x, cell.y),
                        (cell.x + self.cell_size, cell.y),
                    )
                # right wall
                if cell.walls[1]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell.x + self.cell_size, cell.y),
                        (cell.x + self.cell_size, cell.y + self.cell_size),
                    )
                # bottom wall
                if cell.walls[2]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell.x, cell.y + self.cell_size),
                        (cell.x + self.cell_size, cell.y + self.cell_size),
                    )
                # left wall
                if cell.walls[3]:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (cell.x, cell.y),
                        (cell.x, cell.y + self.cell_size),
                    )
