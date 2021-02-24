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
pygame.display.set_caption("A STAR")

"""----------------------------------------------------------------------------
1. SET UP NODE CLASS
----------------------------------------------------------------------------"""
class Node:

    def __init__(self, row, col, width, height, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * height
        self.color = clr.WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows

    def get_coord(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == clr.RED

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
        self.color = clr.RED

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
                                           self.width, self.height))
    
    def updated_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False

"""----------------------------------------------------------------------------
2. DEFINE HEURISTIC AND METHODS
----------------------------------------------------------------------------"""
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)

def make_grids(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid