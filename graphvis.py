
'''
An application for generating and visualising graph structures,
primarily created for use with LINCELLAUT, though my intent is to
make the program flexible enough for any simple graph visualising needs.

Sept 8, 2022
'''

'''
Reference articles:
tutorialspoint.com/python/python_command_line_arguments.htm
'''

from GraphNode import GraphNode
from GraphManager import GraphManager

from random import randrange
from sys import argv

import pygame
pygame.init()
#pygame.font.init()

FPS = 30
CLOCK = pygame.time.Clock()
isPaused = False

windowDimensions = [1280, 720]

windowDisplay = pygame.display.set_mode(windowDimensions)

nodesToMake = 20
nodes = []
connections = []

graphManager = GraphManager(windowDisplay)

#If user passes in a filename on command line
#THIS CURRENTLY DOESN'T CHECK FOR MALFORMED DATA
if len(argv) > 1:
    try:
        graphFile = open(argv[1], "r")
        readMode = "" #Says how to interpret the lines we're reading
        for line in graphFile:
        
            if line[0] == "~":
                if line[1] == "b": #Bounding box
                    parsedLine = line.split(":")
                    if parsedLine[1][:-1] == "True":
                        graphManager.set_boundingBox(True)
                    
                if line[1] == "n": #Number of nodes
                    for n in range(0, int(line[3:])):
                        nodes.append(GraphNode("", (randrange(0, windowDimensions[0]), randrange(0, windowDimensions[1]))))
                        
                elif line[1] == "l": #Labels
                    parsedLine = line.split(":")
                    if len(parsedLine) > 1:
                        if parsedLine[1][:-1] == "body":
                            graphManager.set_labelMode("body")
                            GraphManager.NODERADIUS = 20
                        elif parsedLine[1][:-1] == "none":
                            graphManager.set_labelMode("none")
                            
                    readMode = "labels"
                    
                elif line[1] == "c": #Connections
                    parsedLine = line.split(":")
                    if len(parsedLine) > 1:
                        if parsedLine[1][:-1] == "direction":
                            graphManager.set_edgeMode("direction")
                    
                    readMode = "connections"
                    
            elif readMode == "labels": #If we're reading in node labels
                parsedLine = line.split(":")
                nodes[int(parsedLine[0])].set_label(parsedLine[1][:-1]) #:-1 removes newline
                
            elif readMode == "connections": #If we're reading connection data
                parsedLine = line.split(",")
                connections.append((nodes[int(parsedLine[0])], nodes[int(parsedLine[1])]))
                
        graphFile.close()
                
    except:
        print("Unable to open \"" + argv[1] + "\".")
        
   
#Launching program without a file; randomly generate some nodes
else:
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
            if event.key == pygame.K_p:
                isPaused = not isPaused
                
            elif event.key == pygame.K_l:
                graphManager.toggle_labels()
                
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
            

    if not isPaused:
        graphManager.update_graph()

    graphManager.draw_graph()
    pygame.display.update()
    CLOCK.tick(FPS)
