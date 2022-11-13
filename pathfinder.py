import pygame
from math import inf
import time
from queue import PriorityQueue
from random import randint, choice
from typing import List
from pygame.colordict import THECOLORS
from collections import deque
from main import Vertex, pathfinder

SIZE = 600 
WINDOW = pygame.display.set_mode((SIZE, SIZE)) # Window size
pygame.display.set_caption("Pathfinding pathfinder") # Window title

BLACK = (0, 0, 10) #Barrier
WHITE = (248, 248, 255) #Empty
GRAY = (128, 128, 128) #Grid Lines
RED = (220, 20, 60) #Closed
GREEN = (50, 205, 50) #Open
ORANGE = (255, 165, 0) #Start
PURPLE = (128, 0, 128) #End
TURQUOISE = (64, 224, 208) #Path
LIGHT_GREY = (128, 128, 128) #Buttons

def create_random_grid(num_rows: int, grid_width: int) -> List[List[Vertex]]:
    grid = []
    node_width = grid_width // num_rows

    for row in range(num_rows):
        grid.append([])
        for column in range(num_rows):
            node = Vertex(row, column, node_width, num_rows)
            if choice([True, False]):
                node.color = THECOLORS['black']
            grid[row].append(node)

    return grid

def clear_paths(grid: List[List[Vertex]]) -> None: # New maze
    for row in range(len(grid)):
        for column in range(len(grid)):
            if grid[row][column].color == THECOLORS['red'] or \
                    grid[row][column].color == THECOLORS['yellow'] or \
                    grid[row][column].color == THECOLORS['green']:
                grid[row][column].color = THECOLORS['white']

    return grid

class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    #Gets the position of the node
    def get_pos(self):
        return self.row, self.col
    
    #Methods that check the type of node
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    #Methods that set/make nodes 
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE
    
    def make_path(self):
        self.color = TURQUOISE

    #Resets node back to empty/white
    def reset(self):
        self.color = WHITE

    #Draws node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    #Checks and updates neighboring nodes
    def update_neighbors(self, grid):
        self.neighbors = []

        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        #LEFT
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# Defining our heuristic to calculate the distance between two points (p1 and p2)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstructs shortest path between start and end to draw
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

'''
# pathfinder Logic
def pathfinder(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        #Allows user to quit program while pathfinder is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        #Makes path if current node is the end node
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False    '''   


#Makes grid of nodes
def make_grid(rows, size):
    grid = []
    gap = size // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i , j, gap, rows)
            grid[i].append(node)

    return grid

#Draws the grid lines onto the Window
def draw_grid(win, rows, size):
    gap = size // rows
    #For loop draws vertical lines
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (size, i * gap))
        #Draws horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, size))

def draw(win, grid, rows, size):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, size)
    pygame.display.update()

def get_clicked_pos(pos, rows, size):
    gap = size // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

# Set start and end points for the pathfinder
DIAGONALS = False
VISUALISE = True

#MAIN LOOP
def main(win, size):
    ROWS = 50
    grid = make_grid(ROWS, size)

    #Start/End nodes
    start_position = None
    end_position = None

    run = True

    #Algo loop
    while run:
        draw(win, grid, ROWS, size)
        #Checks for different types of events that may happen
        for event in pygame.event.get():
            #Quit Event
            if event.type == pygame.QUIT:
                run = False

            #Left Mouse Click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, size)
                node = grid[row][col]

                #If Start node does not exist, make it
                if not start_position and node != end_position:
                    start_position = node
                    start_position.make_start()

                #If End node does not exist, make it
                elif not end_position and node != start_position:
                    end_position = node
                    end_position.make_end()

                #make barrier nodes
                elif node != end_position and node != start_position:
                    node.make_barrier()

            #Right Mouse Click/Erase
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, size)
                node = grid[row][col]
                node.reset()

                if node == start_position:
                    start_position = None
                elif node == end_position:
                    end_position = None

            if event.type == pygame.KEYDOWN:
                #KEY_A starts the A* pathfinder
                if event.key == pygame.K_a and start_position and end_position:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    pathfinder(lambda: draw(win, grid, ROWS, size), grid, start_position, end_position, 'manhattan')
            
                #KEY_D starts the DFS pathfinder
                elif event.key == pygame.K_d and start_position and end_position:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    pathfinder(lambda: draw(win, grid, ROWS, size), grid, start_position, end_position, 'pythagorean')

                #KEY_W starts the BFS pathfinder
                elif event.key == pygame.K_w and start_position and end_position:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
  
                    pathfinder(lambda: draw(win, grid, ROWS, size), grid, start_position, end_position, 'diagonal')
          
                 
                # Clear path
                elif event.key == pygame.K_c:
                    clear_paths(grid) 
                
                # New maze
                elif event.key == pygame.K_r:
                    grid = create_random_grid(ROWS, size)
                    start_position = grid[randint(0, ROWS - 1)][randint(0, ROWS - 1)]
                    end_position = grid[randint(0, ROWS - 1)][randint(0, ROWS - 1)]
                    start_position.color = THECOLORS['blue']
                    end_position.color = THECOLORS['purple']
                
            

    # Limit to 60 frames per second
    clock.tick(60)
  
    # Close the window and quit.
    pygame.quit()
main(WINDOW, SIZE)
