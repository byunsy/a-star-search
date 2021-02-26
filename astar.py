"""============================================================================
TITLE      : astar.py
AUTHOR     : Sang Yoon Byun
DESCRIPTION: Visualizes the A* search algorithm finding the shortest path, 
             in terms of Manhattan Distance, from a start node to an end node
             within a confined grid. 
============================================================================"""

import pygame
import math
from queue import PriorityQueue

import astar_colors as clr

"""----------------------------------------------------------------------------
0. SET UP REQUIREMENTS
----------------------------------------------------------------------------"""

# Initialize first
pygame.init()

# Set screen size
screen_width  = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set screen title
pygame.display.set_caption("A STAR PATHFINDER")

"""----------------------------------------------------------------------------
1. SET UP NODE CLASS
----------------------------------------------------------------------------"""
class Node:

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = clr.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_coord(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == clr.YELLOW

    def is_open(self):
        return self.color == clr.GREEN

    def is_barrier(self):
        return self.color == clr.BLACK

    def is_start(self):
        return self.color == clr.ORANGE

    def is_end(self):
        return self.color == clr.CYAN

    def reset(self):
        self.color = clr.WHITE

    def make_closed(self):
        self.color = clr.YELLOW

    def make_open(self):
        self.color = clr.GREEN
    
    def make_barrier(self):
        self.color = clr.BLACK

    def make_start(self):
        self.color = clr.ORANGE

    def make_end(self):
        self.color = clr.CYAN

    def make_path(self):
        self.color = clr.MAGENTA

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 
                                           self.width, self.width))
    
    def update_neighbors(self, grid):

        self.neighbors = []

        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): 
            self.neighbors.append(grid[self.row+1][self.col])

        # UP
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False

"""----------------------------------------------------------------------------
PROCEDURE:
    h(p1, p2)
PARAMETERS:
    p1, coordinate point 1 as a tuple (x1, y1)
    p2, coordinate point 2 as a tuple (x2, y2)
PURPOSE:
    Calculates the heuristic function (Manhattan distance).
PRODUCES:
    distance, the Manhattan distance between two points, p1 and p2.
----------------------------------------------------------------------------"""
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


"""----------------------------------------------------------------------------
PROCEDURE:
    reconstruct_path(origin, current, draw)
PARAMETERS:
    origin, a dict containing which previous node the current node came from 
    current, the current node
    draw, a lambda function explained in draw() function
PURPOSE:
    Draws (in magenta) the final path calculated by the pathfinding algorithm
PRODUCES:
    none, a void function
----------------------------------------------------------------------------"""
def reconstruct_path(origin, current, draw):
    while current in origin:
        current = origin[current]
        current.make_path()

        draw()


"""----------------------------------------------------------------------------
PROCEDURE:
    algorithm(draw, grid, start, end)
PARAMETERS:
    draw, a lambda function explained in draw() function
    grid, a grid composed of nodes (2d-array of nodes)
    start, the start node
    end, the end node
PURPOSE:
    This is the main A* search algorithm that uses the f() and g() functions 
    to calculate cheapest path from the start node to end node.
PRODUCES:
    bool, return True if path found and False if not found.
----------------------------------------------------------------------------"""
def algorithm(draw, grid, start, end):

    count = 0

    open_set = PriorityQueue()
    open_set.put((0, count, start))

    origin = dict()

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_coord(), end.get_coord())

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash_table = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash_table.remove(current)

        if current == end:
            reconstruct_path(origin, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                origin[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_coord(), end.get_coord())

                if neighbor not in open_set_hash_table:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash_table.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False


"""----------------------------------------------------------------------------
PROCEDURE:
    make_grid(rows, width)
PARAMETERS:
    rows, an integer representing the number of rows to create
    width, the width of the screen
PURPOSE:
    Creates the underlying grid for the users to interact with
PRODUCES:
    grid, a 2d-array of nodes
----------------------------------------------------------------------------"""
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


"""----------------------------------------------------------------------------
PROCEDURE:
    draw_grid_lines(win, rows, width)
PARAMETERS:
    win, the main pygame screen
    rows, an integer representing the number of rows to create
    width, the width of the screen
PURPOSE:
    Draws the grey grid lines based on the width and number of rows
PRODUCES:
    none, a void function (grey grid lines drawn on the grid)
----------------------------------------------------------------------------"""
def draw_grid_lines(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, clr.GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, clr.GREY, (j * gap, 0), (j * gap, width))


"""----------------------------------------------------------------------------
PROCEDURE:
    draw(win, grid, rows, width)
PARAMETERS:
    win, the main pygame screen
    grid, a grid composed of nodes (2d-array of nodes)
    rows, an integer representing the number of rows to create
    width, the width of the screen
PURPOSE:
    Draws the grid based on the settings configured by the user
PRODUCES:
    none, a void function (white grid drawn on the screen)
----------------------------------------------------------------------------"""
def draw(win, grid, rows, width):
    win.fill(clr.WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid_lines(win, rows, width)

    pygame.display.update()


"""----------------------------------------------------------------------------
PROCEDURE:
    get_clicked_coord(coord, rows, width)
PARAMETERS:
    coord, the current cursor position (coordinates) on the screen
    rows, an integer representing the number of rows to create
    width, the width of the screen
PURPOSE:
    Computes the current position within the grid. 
PRODUCES:
    pos, (row, col) which contains the current position within the grid 
----------------------------------------------------------------------------"""
def get_clicked_coord(coord, rows, width):
    gap = width // rows
    y, x = coord

    row = y // gap
    col = x // gap

    return row, col


"""----------------------------------------------------------------------------
                                     MAIN
----------------------------------------------------------------------------"""
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:   # LEFT CLICK

                coord = pygame.mouse.get_pos()
                row, col = get_clicked_coord(coord, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK

                coord = pygame.mouse.get_pos()
                row, col = get_clicked_coord(coord, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None

                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(screen, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == '__main__':
    main(screen, screen_width)