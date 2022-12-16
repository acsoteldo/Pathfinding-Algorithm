# Pathfinding Algorithm

This program calculates the shortest path between two points(source and destination) in Python with 3 different algorithms: breadth-first search, depth-first search and A* search. Currently the program is represented in a graph with the nodes and weight of edges provided on a randomly generated maze visualized with pygame. Various heuristics are used, and if the path is found between the points, it's highlighted in green.

- [ ] Add more maze generation algorithms 
- [ ] Incorporate HTML and CSS

#### Tips:
* To clear all paths, press ’C’.
* To generate a new random maze, press ’R’

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
