
'''
An application for generating and visualising graph structures,
primarily created for use with LINCELLAUT, though my intent is to
make the program flexible enough for any simple graph visualising needs.

Sept 8, 2022
'''

from GraphNode import GraphNode
from GraphManager import GraphManager

import pygame
pygame.init()
pygame.font.init()

FPS = 30
CLOCK = pygame.time.Clock()

windowDimensions = [1280, 720]

windowDisplay = pygame.display.set_mode(windowDimensions)

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

    graphManager.draw_graph()
    pygame.display.update()
    CLOCK.tick(FPS)