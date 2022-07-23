

# Import standard modules.
import sys

# Import non-standard modules.
import pygame
from pygame.locals import *


from queue import PriorityQueue
import random

from Button import Button

#some colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)



#some constants used for drawing

top_pad = 200
side_pad = 200

vert_shift = 100
horz_shift = 18

box_pad = 1

width, height = 1000, 1000

#used to generate border radius for drawing nodes
#the effect is drawn nodes will start as a circle, and grow to fill their area
def animate_generator():
        rad = 5
        while rad > 0:
            rad = rad - 0.05
            yield rad



# a node object will represent one node in our model's graph
#update maze neighbors is present because when creating a maze, I leave certain nodes out of the graph as they only represent walls, which DFS removes later on
class Node:
    def __init__(self,row,col,total):
        self.row = row
        self.col = col
        self.total = total
        self.color = WHITE
        self.wall = False
        self.neighbors = []
        self.border = 0
        self.gen = animate_generator()
        self.animating = False


    def get_pos(self):
        return self.row,self.col


    def animate(self):

        if self.animating:

            try:
                self.border = next(self.gen)

            except StopIteration:
                self.gen = animate_generator()
                self.animating = False



    def update_neighbors(self,map):
        self.neighbors = []

        if self.row < self.total - 1 and not (map[self.row + 1][self.col]).wall:
            self.neighbors.append(map[self.row + 1][self.col])

        if self.row > 0 and not (map[self.row - 1][self.col]).wall:
            self.neighbors.append(map[self.row - 1][self.col])

        if self.col > 0 and not (map[self.row][self.col - 1]).wall:
            self.neighbors.append(map[self.row][self.col - 1])

        if self.col < self.total - 1 and not (map[self.row][self.col + 1]).wall:
            self.neighbors.append(map[self.row][self.col + 1])

    def update_maze_neighbors(self,map):
        self.neighbors = []

        if self.row < self.total - 2 and not (map[self.row + 2][self.col]).wall:
            self.neighbors.append(map[self.row + 2][self.col])

        if self.row > 1 and not (map[self.row - 2][self.col]).wall:
            self.neighbors.append(map[self.row - 2][self.col])

        if self.col > 1 and not (map[self.row][self.col - 2]).wall:
            self.neighbors.append(map[self.row][self.col - 2])

        if self.col < self.total - 2 and not (map[self.row][self.col + 2]).wall:
            self.neighbors.append(map[self.row][self.col + 2])

#model that will keep track of the state of the program
class Model:
    def __init__(self,grid_size):
        self.grid_size = grid_size
        self.search = False
        self.maze = False
        self.path_length = " "

        self.start_node = None
        self.end_node = None

        self.map = []
        for i in range(grid_size):
            column = []
            for j in range(grid_size):
                column.append(Node(i,j,self.grid_size))

            self.map.append(column)

        self.started = False

    def set_search(self,bool):
        self.search = bool

    def set_maze(self,bool):
        self.maze = bool

    def reset(self):
        self.start_node = None
        self.end_node = None
        self.search = False
        self.maze = False
        self.path_length = " "

        self.map = []
        for i in range(self.grid_size):
            column = []
            for j in range(self.grid_size):
                column.append(Node(i, j,self.grid_size))

            self.map.append(column)

        self.started = False

#heuristic function for A*, using rise + run
def h(s,f):
    x1,y1 = s
    x2,y2 = f

    return abs(x1-x2) + abs(y1-y2)


#given a posistion and the size of our nodes, returns the corresponding node row and col
def mouse_to_grid(pos,size):
    i,j = None,None


    x,y = pos
    if x >= side_pad/2 + horz_shift and x <= width - side_pad/2 + horz_shift:
        if y >= top_pad/2 + vert_shift and y <= height - top_pad/2 + vert_shift:
            i = (x-side_pad/2 - horz_shift)//(size+box_pad)
            j = (y-top_pad/2 - vert_shift)//(size+box_pad)

    return i,j


def update(screen,model:Model,size,buttons_list):
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary."""

    # Go through events that are passed to the script by the window.
    for event in pygame.event.get():
        # We need to handle these events. Initially the only one you'll want to care
        # about is the QUIT event, because if you don't handle it, your game will crash
        # whenever someone tries to exit.
        if event.type == QUIT:
            pygame.quit()  # Opposite of pygame.init
            sys.exit()  # Not including this line crashes the script on Windows. Possibly
            # on other operating systems too, but I don't know for sure.
        # Handle other events as you wish.


        #if we started drawing the algorithm already, the user should not be able to change the model
        if model.started:
            continue

        #if the user left clicks, get the mouse pos, check if it is within a node's area
        #if there is no start or end node yet, the first two nodes clicked will become start and end nodes
        #otherwise the clicked node will become a wall
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            r,c = mouse_to_grid(pos,size)

            if r != None and c != None:
                if r < model.grid_size and c < model.grid_size:

                    clicked_node = model.map[int(r)][int(c)]


                    if model.start_node == None and clicked_node != model.end_node:
                        model.start_node = clicked_node
                        clicked_node.color = RED
                        clicked_node.wall = False
                        clicked_node.animating = True
                    elif model.end_node == None and clicked_node != model.start_node:
                        model.end_node = clicked_node
                        clicked_node.color = RED
                        clicked_node.wall = False
                        clicked_node.animating = True
                    elif clicked_node != model.start_node and clicked_node != model.end_node:
                        clicked_node.color = BLACK
                        clicked_node.wall = True
                        clicked_node.animating = True

        #if the user right clicks a node, reset the node
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            r, c = mouse_to_grid(pos, size)

            if r != None and c != None:
                if r < model.grid_size and c < model.grid_size:

                    clicked_node = model.map[int(r)][int(c)]

                    if clicked_node == model.start_node:
                        model.start_node = None

                    elif clicked_node == model.end_node:
                        model.end_node = None

                    clicked_node.color = WHITE
                    clicked_node.wall = False

    # if the user hits the search button and the user has selected a start and end node, update every nodes neighbors
    #then run the pathfinding algo

    if model.search and model.start_node != None and model.end_node != None:
        for lst in model.map:
            for node in lst:
                node.update_neighbors(model.map)

        find_path(model,lambda:draw(screen,model,buttons_list,size))
        model.set_search(False)




    #if the user hits the maze button, we reset the model, then create a maze using DFS

    if model.maze:

        #create a checkerboard pattern suitable for depth first search maze creation algorithm
        #I loop twice here to make creating the pattern simpler

        model.reset()
        model.maze = True

        for lst in model.map:
            for node in lst:
                node.color = BLACK
                node.wall = True


        for i,lst in enumerate(model.map):
            for j,node in enumerate(lst):

                if not(i % 2 == 0) and not(j % 2 == 0):
                    node.color = WHITE
                    node.wall = False



        for lst in model.map:
            for node in lst:
                node.update_maze_neighbors(model.map)

        draw(screen, model, buttons_list, size)




        stack = []
        visited = set()

        start_node = model.map[1][1]

        #add start node to stack and mark as visited
        stack.append(start_node)
        visited.add(start_node)

        while len(stack) > 0:
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if not(model.maze):
                return

            curr = stack.pop()

            unvisited = []
            for neighbor in curr.neighbors:
                if neighbor not in visited:
                    unvisited.append(neighbor)

            if len(unvisited) > 0:
                stack.append(curr)

                n = unvisited[random.randrange(0,len(unvisited),1)]


                row_diff = curr.row - n.row
                col_diff = curr.col - n.col

                wall_to_replace = model.map[int(curr.row - row_diff/2)][int(curr.col - col_diff/2)]
                wall_to_replace.color = WHITE
                wall_to_replace.wall = False
                wall_to_replace.animating = True



                visited.add(n)
                stack.append(n)

            draw(screen, model, buttons_list, size)



        model.maze = False
        model.started = False






def draw(screen,model:Model,buttons_list,box_size):
    """
    Draw things to the window. Called once per frame.
    """

    #refresh screen
    screen.fill((145, 210, 242))        #(162, 210, 245))

    #drawing all text
    medium_font = pygame.font.SysFont('georgia', 20)
    large_font = pygame.font.SysFont('georgia', 32)

    title_text = large_font.render("Path Visualizer",True,(0,0,0))
    title_text_rect = title_text.get_rect()
    title_text_rect.center = (screen.get_width()/2,25)
    screen.blit(title_text,title_text_rect)


    size_text = medium_font.render(f"Path Length: {model.path_length}", True, (0, 0, 0))
    size_text_rect = size_text.get_rect()
    size_text_rect.topleft = (screen.get_width() / 2 - 385, 150)
    screen.blit(size_text, size_text_rect)

    if not(model.start_node):
        row_text = "-"
        col_text = "-"
    else:
        row_text = model.start_node.row
        col_text = model.start_node.col

    start_node_text = medium_font.render(f"Start: {row_text} , {col_text}", True, (0, 0, 0))
    start_node_text_rect = start_node_text.get_rect()
    start_node_text_rect.topleft = (screen.get_width()/2 - 385, 100)
    screen.blit(start_node_text,start_node_text_rect)


    if not(model.end_node):
        row_text2 = "-"
        col_text2 = "-"
    else:
        row_text2 = model.end_node.row
        col_text2 = model.end_node.col

    end_node_text = medium_font.render(f"End: {row_text2} , {col_text2}", True, (0, 0, 0))
    end_node_text_rect = end_node_text.get_rect()
    end_node_text_rect.topleft = (screen.get_width()/2 - 385, 125)
    screen.blit(end_node_text,end_node_text_rect)


    #draws every node in our model

    for lst in model.map:
        for node in lst:
            node.animate()
            pygame.draw.rect(screen,node.color,((side_pad/2 + box_size*node.row + box_pad*node.row + horz_shift),((top_pad/2 + box_size*node.col + box_pad*node.col) + vert_shift),box_size,box_size),border_radius=int(node.border))


    #draws every button
    for b in buttons_list:
        b.draw()

    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


#pathfinding fundction that uses A*
def find_path(model:Model,draw):

    #initializing vars, PQ, predecessor dict, g score and f score dicts, and set to check whether node is in the PQ
    start = model.start_node
    end = model.end_node

    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    preds = {}

    g = {node:float("inf") for lst in model.map for node in lst}
    g[start] = 0

    f = {node:float("inf") for lst in model.map for node in lst}
    f[start] = h(start.get_pos(),end.get_pos())

    open_hash = {start}

    #while there a still nodes to explore
    while not open_set.empty():
        #checks if user quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #ends if the user hits reset or maze button
        if not(model.started) or model.maze:
            return

        #remove start node from PQ
        current = open_set.get()[2]
        open_hash.remove(current)

        #if we get to the end node, traverse through the preds dict and draw the path
        if current == end:
            temp = 0
            while current in preds:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                temp += 1
                current = preds[current]
                current.color = 27, 242, 88
                current.animating = True
                end.color = RED
                draw()
            start.color = RED

            model.path_length = temp


            return True

        #get the current nodes neighbors and adjust g and f scores
        for neighbor in current.neighbors:
            temp_g = g[current] + 1

            if temp_g < g[neighbor]:
                preds[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(),end.get_pos())

                #if we havent checked the neighbors neighbors yet, add neighbor to the PQ
                if neighbor not in open_hash:
                    count += 1
                    open_set.put((f[neighbor],count,neighbor))
                    open_hash.add(neighbor)
                    neighbor.color = (22,50,242)
                    neighbor.animating = True



        #creates color gradient
        if current != start:
            color_shift = 255*(1/(h(current.get_pos(),end.get_pos())/50 + 1))
            current.color = (22,color_shift,255)
            current.animating = True

        #draw to the screen
        draw()

    #if we get this far there is no path
    model.path_length = "No Path"




def runPyGame():
    # Initialise PyGame.
    pygame.init()

    pygame.display.set_caption("Path Visualizer")
    pygame_icon = pygame.image.load('maze.png')
    pygame.display.set_icon(pygame_icon)

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 150
    fpsClock = pygame.time.Clock()

    # Set up the window.
    screen = pygame.display.set_mode((width, height))

    size = 51

    box_size = (screen.get_width() - side_pad - (size * box_pad)) // size



    #initialize model
    m = Model(size)

    #create button list to be passed to draw and create all buttons

    buttons = []

    buttons.append(Button(screen,"Reset",100,50,(screen.get_width()/2 + 35, 100),lambda:m.reset()))

    def search_button():
        m.set_search(True)
        m.started = True

    buttons.append(Button(screen, "Search", 100, 50, (screen.get_width() / 2 + 160, 100), lambda: search_button()))

    buttons.append(Button(screen, "Maze", 100, 50, (screen.get_width() / 2 + 285, 100), lambda: m.set_maze(True)))




    # Main loop.

    while True:  # Loop forever
        update(screen,m,box_size,buttons)
        draw(screen,m,buttons,box_size)

        fpsClock.tick(fps)


if __name__ == "__main__":
    runPyGame()
