
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
    NODEREPULSION = 1/100 #The smaller the number, the greater the repulsion (1/100)
    
    CONNECTIONWIDTH = 2
    CONNECTIONSTRENGTH = 1/60000 #The larger the number, the greater the pull from the strings (1/6000)
    TARGETCONNECTIONSTRENGTH = 1/6000
    
    ARROWHEADEND = NODERADIUS + 10
    ARROWHEADGIRTH = 7
    
    UNITPERPIXEL = 1/496 #Approximately 10cm on my screen
    FRICTION = 0.1 #The lower the number, the 
    
    SCALETICK = 0.9
    
    DEFFONT = pygame.font.SysFont("Courier", 20)
    DEFFONT.set_bold(True)
    
    def __init__(self, surface):
        self.nodes = []
        self.connections = []
        self.surface = surface
        
        self.clickedNode = None #Holds the node the user is currently dragging
        
        self.drawScale = 1
        self.edgeMode = "free"
        self.labelMode = "above"
        self.initialLabelMode = "above"
        self.labelAlignment = "center"
        self.boundingBox = False #Determines whether to keep the graph in a little bounding box
        
        self.easeIntoTension = True
        
    
    @staticmethod
    def lerp(startPos, endPos, p):
        '''Returns a point 100p% of the way between startPos and endPos.'''
        return [(endPos[0]-startPos[0])*p + startPos[0],
                (endPos[1]-startPos[1])*p + startPos[1]]
                
                
    def set_edgeMode(self, mode):
        '''Sets the mode used by the manager to draw graph nodes.'''
        self.edgeMode = mode
        
        
    def set_labelMode(self, mode):
        '''Sets the mode used by the manager to draw labels 
        (also affects how nodes are drawn).'''
        self.labelMode = mode
        self.initialLabelMode = mode
        
        
    def toggle_labels(self):
        '''Toggles labels on/off.'''
        if self.labelMode == "none":
            self.labelMode = self.initialLabelMode
        else:
            self.labelMode = "none"
        
        
    def set_boundingBox(self, mode):
        '''Sets whether the manager should use the bounding box.'''
        self.boundingBox = mode

    
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
        
        
    def scale_position(self, pos):
        '''Returns a properly scaled version of a given list.'''
        scaledPos = pos.copy()
        scaledPos[0] = scaledPos[0]*self.drawScale + self.surface.get_width()*(1 - self.drawScale)/2
        scaledPos[1] = scaledPos[1]*self.drawScale + self.surface.get_height()*(1 - self.drawScale)/2
        return scaledPos
        
        
    def clear_clickedNode(self):
        '''Sets clickedNode to None.'''
        self.clickedNode = None
        
        
    def get_clickedNode(self):
        '''Returns clickedNode.'''
        return self.clickedNode
        
        
    def set_clickedNode(self, rect):
        '''Sets the manager's node to drag around with the mouse.'''
        
        #Creating all these Rects on the fly is probably inefficient. 
        # I'll change it if it becomes a nuisance
        for node in self.nodes:
        
            #Scale nodes to fit current window zoom
            scaledNodePos = self.scale_position(node.get_position())
            
            if pygame.Rect.colliderect(rect, pygame.Rect(scaledNodePos[0]-GraphManager.NODERADIUS*self.drawScale,
                                              scaledNodePos[1]-GraphManager.NODERADIUS*self.drawScale,
                                              GraphManager.NODERADIUS*2*self.drawScale,
                                              GraphManager.NODERADIUS*2*self.drawScale)):
                self.clickedNode = node #Copying address
                return
                
        self.clickedNode = None
        
        
    def move_clickedNode(self, delta):
        '''Move the position of the clicked node by the amounts given.'''
        if self.clickedNode != None:
        
            #These lines map our raw mouse coords to scaled coords,
            # allowing the user to drag the nodes properly in the scaled space
            self.drawScale = 1/self.drawScale
            scaledDelta = self.scale_position(delta)
            self.drawScale = 1/self.drawScale
            
            self.clickedNode.set_position(scaledDelta)
        
 
    def update_graph(self):
        '''Updates the graph's nodes, applying relevant forces to each.'''
        
        #Prevents the graph from immediately shitting itself
        #Should definitely change this to use member variables instead of static variables
        if self.easeIntoTension:
            GraphManager.CONNECTIONSTRENGTH += (GraphManager.TARGETCONNECTIONSTRENGTH - GraphManager.CONNECTIONSTRENGTH)/10
        
        for node in self.nodes:
            tempForce = [0, 0]
            
            #Node repulsion
            for otherNode in self.nodes:
                if otherNode != node: #Using memory addresses
                    try:
                        tempForce[0] -= node.direction_to(otherNode)[0] * GraphManager.UNITPERPIXEL * \
                                        (node.distance_to(otherNode) * GraphManager.NODEREPULSION)**(-2)
                    except ZeroDivisionError: #When a node gets shoved on top of another
                        tempForce[0] -= 0
                                 
                    try:
                        tempForce[1] -= node.direction_to(otherNode)[1] * GraphManager.UNITPERPIXEL * \
                                        (node.distance_to(otherNode) * GraphManager.NODEREPULSION)**(-2)
                    except ZeroDivisionError:
                        tempForce[1] -= 0


            #Connection attraction (elasticity)
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
        #This also keeps nodes within the window
        for node in self.nodes:
            if self.boundingBox:
                node.update_position((self.surface.get_width()*(1/self.drawScale), 
                                      self.surface.get_height()*(1/self.drawScale)), 
                                      (-(self.surface.get_width()*(1/self.drawScale) - self.surface.get_width())/2,
                                      -(self.surface.get_height()*(1/self.drawScale) - self.surface.get_height())/2),
                                      GraphManager.NODERADIUS*self.drawScale)
            else:
                node.update_position()
                
                
    def move_graph(self, delta):
        '''Moves the graph around by however much the mouse moved.'''
        scaledDelta = [delta[0]*(1/self.drawScale), delta[1]*(1/self.drawScale)]
        for node in self.nodes:
            node.set_position((node.get_position()[0] + scaledDelta[0],
                               node.get_position()[1] + scaledDelta[1]))

  
    def draw_graph(self):
        '''Displays the graph to the given surface.'''

        self.surface.fill("black")
        
        for conn in self.connections:
            connStartPos = self.scale_position(conn.get_start_position())
            connEndPos = self.scale_position(conn.get_end_position())
            
            #The length of the edge between nodes
            lineLength = ((connEndPos[0]-connStartPos[0])**2 + (connEndPos[1]-connStartPos[1])**2)**0.5
            
            #Only draw lines as far into the node as needed
            if lineLength != 0 and self.labelMode == "body":
                connStartPosLerp = GraphManager.lerp(connStartPos, connEndPos, GraphManager.NODERADIUS*self.drawScale/lineLength)
                connEndPosLerp = GraphManager.lerp(connStartPos, connEndPos, 1 - GraphManager.NODERADIUS*self.drawScale/lineLength)
                connStartPos = connStartPosLerp.copy()
                connEndPos = connEndPosLerp.copy()
            
            #Draw edges
            pygame.draw.line(self.surface, "grey", connStartPos, connEndPos, 
                             width=max(int(GraphManager.CONNECTIONWIDTH*self.drawScale), 1))
                             
            #Draw arrowhead
            if self.edgeMode == "direction":
                
                if lineLength != 0:
                
                    if self.labelMode == "above" or self.labelMode == "none":
                        arrowStart = GraphManager.lerp(connStartPos, connEndPos, 1 - GraphManager.NODERADIUS*self.drawScale/lineLength)
                    elif self.labelMode == "body":
                        arrowStart = connEndPos.copy()
                        
                    arrowEnd = GraphManager.lerp(connStartPos, connEndPos, 1 - GraphManager.ARROWHEADEND*self.drawScale/lineLength)
                else:
                    arrowStart = None
                    
                try:
                    normalSlope = (connEndPos[1] - connStartPos[1])/(connEndPos[0] - connStartPos[0])
                    normalSlope = -1/normalSlope
                except ZeroDivisionError:
                    normalSlope = None
                    
                if arrowStart != None:
                    if normalSlope == None:
                        arrowPoint1 = [arrowEnd[0], arrowEnd[1] + GraphManager.ARROWHEADGIRTH*self.drawScale]
                        arrowPoint2 = [arrowEnd[0], arrowEnd[1] - GraphManager.ARROWHEADGIRTH*self.drawScale]
                    else:
                        dx = ((GraphManager.ARROWHEADGIRTH*self.drawScale)**2 / (1 + normalSlope**2))**0.5
                        arrowPoint1 = [arrowEnd[0] + dx, arrowEnd[1] + dx*normalSlope]
                        arrowPoint2 = [arrowEnd[0] - dx, arrowEnd[1] - dx*normalSlope]
         
                    pygame.draw.line(self.surface, "grey", arrowStart, arrowPoint1,
                                     width=max(int(GraphManager.CONNECTIONWIDTH*self.drawScale), 1))
                    pygame.draw.line(self.surface, "grey", arrowStart, arrowPoint2,
                                     width=max(int(GraphManager.CONNECTIONWIDTH*self.drawScale), 1))
            
        
        for node in self.nodes:
            nodePos = self.scale_position(node.get_position())
            
            if self.labelMode != "body":
                #Preventing off-screen nodes from being drawn
                if (nodePos[0]+GraphManager.NODERADIUS > 0 and nodePos[0]-GraphManager.NODERADIUS < self.surface.get_width()) and \
                   (nodePos[1]+GraphManager.NODERADIUS > 0 and nodePos[1]-GraphManager.NODERADIUS < self.surface.get_height()):
                    pygame.draw.circle(self.surface, "white", nodePos, GraphManager.NODERADIUS*self.drawScale)
                
            if self.labelMode != "none":
                textSurf = pygame.font.Font.render(GraphManager.DEFFONT, node.get_label(), True, "white")
                
                textLeeway = 15
                textX = 0
                textY = 0
                
                #Will probably have to change if font sizes change
                if self.labelAlignment == "center":
                    textX = nodePos[0] - 5*(1 + len(node.get_label()))
                elif self.labelAlignment == "left":
                    textX = nodePos[0] - 10*(1 + len(node.get_label()))
                elif self.labelAlignment == "right":
                    textX = nodePos[0]
                
                if self.labelMode == "above":
                    textY = nodePos[1] - textLeeway - (GraphManager.NODERADIUS + 5)*self.drawScale
                elif self.labelMode == "body":
                    textY = nodePos[1] - 3*self.drawScale #Need to make this better
                
                if textX < textLeeway:
                    textX = textLeeway
                elif textX > self.surface.get_width() - textLeeway - 20:
                    textX = self.surface.get_width() - textLeeway - 20
                    
                if textY < textLeeway:
                    textY = textLeeway
                elif textY > self.surface.get_height() - textLeeway - 20:
                    textY = self.surface.get_height() - textLeeway - 20
                    
                self.surface.blit(textSurf, (textX, textY))
            
            
    def change_scale(self, delta):
        '''Changes the scale at which the graph is drawn.'''
        for x in range(0, abs(delta)):
            if delta > 0:
                self.drawScale /= GraphManager.SCALETICK
            else:
                self.drawScale *= GraphManager.SCALETICK
