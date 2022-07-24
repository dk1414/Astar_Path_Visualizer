
# A*_Path_Visualizer

Pygame UI that displays how the A* algorithm navigates an unweighted undirected graph


[![A* Path Visualizer Demo](https://imgur.com/FAoKne5.png)](https://www.youtube.com/watch?v=pQAVXhursHk "A* Path Visualizer Demo")


## Description

This program visualizes the process that the A* algorithm uses to find the shortest path between two nodes.
The model class in viewer.py stores a 2d list of node objects, this represents the unweighted undirected graph.

The user is able to choose a start and end node, drawn in red, as well as add walls to nodes, drawn in black.
The algorithm begins by updating each node's neighbors. If a node is a wall, it will not have any neighbors and it cannot be another node's neighbor.
This updates the graph so that it reflects all the changes that the user may have made.
A* search is then performed using manhattan distance as the heuristic function. (for more details see code comments)
Nodes that the algorithm are done checking are drawn to screen with a color gradient, (the closer the node is to the end, the lighter its color),
and unfinished nodes are drawn in dark blue. When the algorithm is finished, if a path was found, it is drawn in green, and its distance is displayed.
Otherwise, no path is drawn.

### Maze Function

To generate mazes, the randomized DFS algorithm was used. Since the graph is represented as a 2d list of nodes, in order to use DFS to create a maze, the graph must 
be made so that each nodes 4 neighbors,(top, bottom, left, right), are made to be walls. This creates a checkerboard pattern which should look like this 

![Screenshot (105)](https://user-images.githubusercontent.com/90418273/180634205-dfcfbb10-160f-419c-9abd-5664eeecdb9e.png)

Once the graph is in this state, the neighbors for all the white nodes need to be updated where a white node has a neighbor if the node 2 spaces in any direction is not a wall. For example, the top left white node in the image above located at 1,1 has neighbors at 3,1 and 1,3. Now that each node has the correct neighbors, DFS can be used to remove the walls between white nodes in a way that creates a maze pattern.

---

### Installing

* Download zip file and unzip into directory of your choice
* Open the viewer.py file and run

### Executing program

* Once you download all necessary files and run the viewer.py file, the main window should appear
* Click a square to place the start node, and end node. (In the absence of a start node, the next square clicked will become a start node, this is also true for end nodes)
* Once a start and end node are placed, clicking a square will place a wall, which the algorithm must go around
* To revert a square back to a white square, simply right click it
* To start the algorithm hit search
* To create a maze pattern hit the maze button
* To reset every square at any point, hit the reset button
