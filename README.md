# Pathfinding Algorithm

This program calculates the shortest path between two points(source and destination) in Python with 3 different algorithms: breadth-first search, depth-first search and A* search. Currently the program is represented in a graph with the nodes and weight of edges provided on a randomly generated maze visualized with pygame. Various heuristics are used, and if the path is found between the points, it's highlighted in green.

* The create_random_graph function generates a grid of Vertex objects with a random number of barriers (colored black).
* The clear_paths function resets the colors of the Vertex objects to white (empty).
* The Vertex class represents a single node in the grid, and has several methods for updating and drawing the node, as well as checking its type and neighbors.
* The draw function is used to draw the grid and nodes on the Pygame window.
* The draw_grid function is used to draw the lines between the nodes on the Pygame window.
* The get_clicked_pos function gets the position of the mouse click and returns the row and column of the clicked node.
* The main function contains the main loop of the program, which handles user input, updates the graph, and redraws the window.

#### Tips:
* To generate a new random maze, press ’c’
* For A* search, press ’a’
* For Breadth-first search, press ’b’
* For Depth-first search, press ’d’

#### Technology used
* Python for backend

#### Libraries/modules:
* pygame

## Breadth-first search
BFS is an algorithm for traversing a graph in which nodes are visited in the order of their distance from the start node. It works by maintaining a queue of nodes to visit, starting with the start node, and adding the neighbors of each visited node to the end of the queue. BFS returns the shortest path between the start and goal nodes, since it always expands the node that is closest to the start first.
### Screenshots
[update]

## Depth-first search 
DFS is an algorithm for traversing a graph in which nodes are visited in a depth-first manner, meaning that a node is fully explored before its neighbors are explored. It works by maintaining a stack of nodes to visit, starting with the start node, and adding the neighbors of each visited node to the top of the stack. DFS does not necessarily find the shortest path between the start and goal nodes, as it does not prioritize expanding nodes that are closer to the start.
### Screenshots
[update]

## A* search
A* search is an algorithm for finding the shortest path between two nodes in a graph. It combines the strengths of BFS and DFS by using a heuristic function to guide the search towards the goal. The heuristic function estimates the distance from a given node to the goal, and A* expands the node that has the lowest estimated total cost (the sum of the cost of reaching the node and the estimated distance to the goal). A* is guaranteed to find the shortest path if the heuristic function is admissible, meaning that it never overestimates the distance to the goal.
### Screenshots
[update]
