
'''
An application for generating and visualising graph structures,
primarily created for use with LINCELLAUT, though my intent is to
make the program flexible enough for any simple graph visualising needs.

Sept 8, 2022
'''

from GraphNode import GraphNode
from GraphManager import GraphManager

from random import randrange

import pygame
pygame.init()
#pygame.font.init()

FPS = 30
CLOCK = pygame.time.Clock()

windowDimensions = [1280, 720]

windowDisplay = pygame.display.set_mode(windowDimensions)

#Randomly generate a bunch of nodes and connections to see how the 
# GraphManager behaves

nodesToMake = 20
nodes = []
connections = []

for x in range(0, nodesToMake):
    nodeX = randrange(0, windowDimensions[0])
    nodeY = randrange(0, windowDimensions[1])
    nodes.append(GraphNode(str(x), (nodeX, nodeY)))
    
connectionMarkers = [False for x in range(0, len(nodes))]
    
for x in range(0, nodesToMake):
    node1 = randrange(0, len(nodes))
    node2 = randrange(0, len(nodes))
    connections.append((nodes[node1], nodes[node2]))
    
    if node1 != node2:
        connectionMarkers[node1] = True
        connectionMarkers[node2] = True
    
#Removing nodes that don't have connections
for x in range(len(connectionMarkers)-1, -1, -1):
    if not connectionMarkers[x]:
        del nodes[x]


'''
nodes = [GraphNode("1", (25, 50)),
         GraphNode("2", (1000, 400)),
         GraphNode("3", (600, 600)),
         GraphNode("on3", (400, 100)),
         GraphNode("onon3", (777, 700))]
         
connections = [(nodes[0], nodes[1]),
               (nodes[1], nodes[2]),
               (nodes[2], nodes[0]),
               (nodes[2], nodes[3]),
               (nodes[3], nodes[4])]
'''

graphManager = GraphManager(windowDisplay)

for node in nodes:
    graphManager.add_node(node)

for connection in connections:
    graphManager.add_connection(connection[0], connection[1])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pass
                
        #If the user wants to change the scaling of the graph
        elif event.type == pygame.MOUSEWHEEL:
            graphManager.change_scale(event.y)
        
        #Ensuring we don't accidentally move a node we don't want to
        elif event.type == pygame.MOUSEBUTTONUP:
            graphManager.clear_clickedNode()
               
        #Checking to see if the user wants to drag a node around
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            pygame.mouse.get_rel() #Called so that subsequent drags will work correctly
            graphManager.set_clickedNode(pygame.Rect(mousePos[0], mousePos[1], 2, 2))

            
            
    #Checking to see if the user is dragging around
    if pygame.mouse.get_pressed()[0]:
        if graphManager.get_clickedNode() != None:
            graphManager.move_clickedNode([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
            
        else: #If the user wants to move the view around
            mouseRel = pygame.mouse.get_rel()
            graphManager.move_graph([mouseRel[0], mouseRel[1]])
            

    graphManager.draw_graph()
    pygame.display.update()
    CLOCK.tick(FPS)
