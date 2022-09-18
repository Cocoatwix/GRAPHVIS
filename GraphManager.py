
'''
Reference articles:
stackoverflow.com/questions/68645/
pygame.org/docs/
'''

import pygame
from GraphNode import GraphNode
from GraphConnection import GraphConnection

pygame.font.init()

class GraphManager():

    NODERADIUS = 10
    NODEREPULSION = 1/100 #The smaller the number, the greater the repulsion
    
    CONNECTIONWIDTH = 2
    CONNECTIONSTRENGTH = 1/6000 #The larger the number, th greater the pull from the strings
    
    UNITPERPIXEL = 1/496 #Approximately 10cm on my screen
    FRICTION = 0.1 #The lower the number, the 
    
    DEFFONT = pygame.font.SysFont("Times New Roman", 20)
    
    def __init__(self, surface):
        self.nodes = []
        self.connections = []
        self.surface = surface
        
        
    def leaky_ReLU(self, n, gate):
        '''Applies a leaky ReLU to a number.'''
        if (n < gate):
            return 0
        else:
            return n - gate
    
    
    def add_node(self, node):
        '''Appends a new node to the manager's list.'''
        self.nodes.append(node)
     
   
    def get_nodes(self):
        '''Returns the lost of nodes in the graph.'''
        return self.nodes
   
   
    def add_connection(self, n1, n2):
        '''Adds a connection between two nodes. The two nodes must
           already be part of the graph.'''
        self.connections.append(GraphConnection(n1, n2, 0))
        
 
    def update_graph(self):
        '''Updates the graph's nodes, applying relevant forces to each.'''
        
        for node in self.nodes:
            tempForce = [0, 0]
            
            #Node repulsion
            for otherNode in self.nodes:
                if otherNode != node: #Using memory addresses
                    tempForce[0] -= node.direction_to(otherNode)[0] * GraphManager.UNITPERPIXEL * \
                                    (node.distance_to(otherNode) * GraphManager.NODEREPULSION)**(-2)
                                    
                    tempForce[1] -= node.direction_to(otherNode)[1] * GraphManager.UNITPERPIXEL * \
                                    (node.distance_to(otherNode) * GraphManager.NODEREPULSION)**(-2)

                    
            #Connection attraction
            for conn in self.connections:
                if conn.get_start_node() == node: #Using memory addresses
                    tempForce[0] += node.direction_to(conn.get_end_node())[0] * \
                                    node.distance_to(conn.get_end_node()) * GraphManager.CONNECTIONSTRENGTH
 
                    tempForce[1] += node.direction_to(conn.get_end_node())[1] * \
                                    node.distance_to(conn.get_end_node()) * GraphManager.CONNECTIONSTRENGTH
                    
                elif conn.get_end_node() == node: #Using memory addresses
                    tempForce[0] += node.direction_to(conn.get_start_node())[0] * \
                                    node.distance_to(conn.get_start_node()) * GraphManager.CONNECTIONSTRENGTH
                                    
                    tempForce[1] += node.direction_to(conn.get_start_node())[1] * \
                                    node.distance_to(conn.get_start_node()) * GraphManager.CONNECTIONSTRENGTH

            #Update force
            node.set_externalForce(tempForce)
            node.apply_friction(GraphManager.FRICTION)
            
        #Only update nodes after all forces have been calculated
        for node in self.nodes:
            node.update_position()

  
    def draw_graph(self):
        '''Displays the graph to the given surface.'''

        self.surface.fill("black")
        
        self.update_graph()
        
        for connection in self.connections:
            pygame.draw.line(self.surface, "grey", 
                             connection.get_start_position(), connection.get_end_position(),
                             width=GraphManager.CONNECTIONWIDTH)
        
        for node in self.nodes:
            pygame.draw.circle(self.surface, "white", node.get_position(), GraphManager.NODERADIUS)
            textSurf = pygame.font.Font.render(GraphManager.DEFFONT, node.get_label(), True, "white")
            
            textX = 0
            textY = 0
            if node.get_position()[0] > 0 and node.get_position()[0] < self.surface.get_width():
                textX = node.get_position()[0]
                
            if node.get_position()[1]-30 > 0 and node.get_position()[1]-30 < self.surface.get_height():
                textY = node.get_position()[1]-30
                
            self.surface.blit(textSurf, (textX, textY))
            