import pygame
import math
from queue import PriorityQueue
from random import randint, choice
from typing import List
from pygame.colordict import THECOLORS
from collections import deque
from main import Vertex, pathfinder

SIZE = 600 
WINDOW = pygame.display.set_mode((SIZE, SIZE)) # Window size
pygame.display.set_caption("Pathfinding Algorithm") # Window title

BLACK = (0, 0, 10) #Barrier
WHITE = (248, 248, 255) #Empty
GRAY = (128, 128, 128) #graph Lines
RED = (220, 20, 60) #Closed
GREEN = (50, 205, 50) #Open
ORANGE = (255, 165, 0) #Start
PURPLE = (128, 0, 128) #goal
TURQUOISE = (64, 224, 208) #Path
LIGHT_GREY = (128, 128, 128) #Buttons

def create_random_graph(num_rows: int, graph_width: int) -> List[List[Vertex]]:
    graph = []
    node_width = graph_width // num_rows

    for row in range(num_rows):
        graph.append([])
        for column in range(num_rows):
            node = Vertex(row, column, node_width, num_rows)
            if choice([True, False]):
                node.color = THECOLORS['black']
            graph[row].append(node)

    return graph

def clear_paths(graph: List[List[Vertex]]) -> None: # New maze
    for row in range(len(graph)):
        for column in range(len(graph)):
            if graph[row][column].color == THECOLORS['red'] or \
                    graph[row][column].color == THECOLORS['yellow'] or \
                    graph[row][column].color == THECOLORS['green']:
                graph[row][column].color = THECOLORS['white']

    return graph

class Vertex:
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

    def is_goal(self):
        return self.color == PURPLE
        
    #Methods that set/make nodes 
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
        return

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE

    def make_goal(self):
        self.color = PURPLE
    
    def make_path(self):
        self.color = TURQUOISE

    #Resets node back to empty/white
    def reset(self):
        self.color = WHITE

    #Draws node
    def draw(self, win, size):
        pygame.draw.rect(win, self.color, (self.x, self.y, size, size))

    #Checks and updates neighboring nodes
    def update_neighbors(self, graph):
        self.neighbors = []

        #DOWN
        if self.row < self.total_rows - 1 and not graph[self.row + 1][self.col].is_barrier():
            self.neighbors.append(graph[self.row + 1][self.col])

        #UP
        if self.row > 0 and not graph[self.row - 1][self.col].is_barrier():
            self.neighbors.append(graph[self.row - 1][self.col])

        #RIGHT
        if self.col < self.total_rows - 1 and not graph[self.row][self.col + 1].is_barrier():
            self.neighbors.append(graph[self.row][self.col + 1])

        #LEFT
        if self.col > 0 and not graph[self.row][self.col - 1].is_barrier():
            self.neighbors.append(graph[self.row][self.col - 1])

# For A* search
def heuristic(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current_node, draw):
    while current_node in came_from:
        current_node = came_from[current_node]
        current_node.make_path()
        draw()

def a_star(draw, graph, start, goal):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in graph for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in graph for node in row}
    f_score[start] = heuristic(start.get_pos(), goal.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2]
        open_set_hash.remove(current_node)

        if current_node == goal:
            reconstruct_path(came_from, goal, draw)
            goal.make_goal()
            return True

        for neighbor in current_node.neighbors:
            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), goal.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current_node != start:
            current_node.make_closed()

    return None

def depth_first_search(draw, graph, start, goal):
    stack = []
    path = []
    stack.append(start)

    while len(stack) > 0:
        current_node = stack.pop()

        for neighbor in current_node.neighbors:
            if neighbor.is_closed():
                continue
            elif neighbor == goal:
                goal.make_goal()
                path.append(current_node)
                neighbor.make_path()
                path.append(neighbor)
                return path[::-1]
            else:
                if not neighbor.is_open():
                    neighbor.make_open()
                stack.append(neighbor)
                path.append(current_node)
        
        draw()
        
        if current_node != start:
            current_node.make_closed()
   
    return None

def breadth_first_search(draw, graph, start, goal):
    queue = []
    path=[]
    queue.append(start)

    while len(queue) > 0:
        current_node = queue.pop(0)

        for neighbor in current_node.neighbors:
            if neighbor.is_closed():
                continue
            elif neighbor == goal:
                goal.make_goal()
                path.append(current_node)
                neighbor.make_path()
                path.append(neighbor)
                return path[::-1]
            else:
                if not neighbor.is_open():
                    neighbor.make_open()
                queue.append(neighbor)
                path.append(current_node)
        
        draw()

        if current_node != start:
            current_node.make_closed()

    return None

def draw_grid(win, rows, size):
    gap = size // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (size, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, size))

def draw(win, graph, rows, size):
    win.fill(WHITE)

    for row in graph:
        for node in row:
            node.draw(win, size)

    draw_grid(win, rows, size)
    pygame.display.update()

def get_clicked_pos(pos, rows, size):
    gap = size // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    clock = pygame.time.Clock()
    grid = create_random_graph(ROWS, width)

    start = None
    goal = None

    running = True
    while running:
        clock.tick(25)
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != goal:
                    start = node
                    start.make_start()

                elif not goal and node != start:
                    goal = node
                    goal.make_goal()

                elif node != goal and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                #KEY_A starts the A* pathfinder
                if event.key == pygame.K_a and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, goal)
                #KEY_D starts the DFS pathfinder
                if event.key == pygame.K_d and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    depth_first_search(lambda: draw(win, grid, ROWS, width), grid, start, goal)
                #KEY_B starts the BFS pathfinder
                if event.key == pygame.K_b and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    breadth_first_search(lambda: draw(win, grid, ROWS, width), grid, start, goal)
                # New maze
                if event.key == pygame.K_SPACE:
                    start = None
                    goal = None
                    grid = create_random_graph(ROWS, width)

    pygame.quit()

main(WINDOW, SIZE)
