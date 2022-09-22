
class GraphNode():

    MINIMUMSPEED = 0.1
    MAXIMUMSPEED = 1000

    def __init__(self, label, pos=(0, 0)):
        self.label = label
        self.position = [pos[0], pos[1]]
        self.velocity = [0, 0]
        self.externalForce = [0, 0]
        
        
    def get_label(self):
        '''Returns the node's label.'''
        return self.label
        
        
    def set_label(self, L):
        '''Sets the node's label.'''
        self.label = L
        
        
    def get_position(self):
        '''Return the position of the node.'''
        return self.position
        
        
    def set_position(self, pos):
        '''Sets the position of the node to the given coordinates in pos.'''
        self.position[0] = pos[0]
        self.position[1] = pos[1]
        
        
    def set_externalForce(self, force):
        '''Set the external force acting on the node.'''
        self.externalForce = force.copy()
        
        
    def distance_to(self, node):
        '''Returns the Euclidian distance between this node and the given node.'''
        return ((self.position[0]-node.get_position()[0])**2 +
                (self.position[1]-node.get_position()[1])**2)**0.5
                
                
    def direction_to(self, node):
        '''Returns a vector representing the direction to a given node from this node.'''
        return (node.get_position()[0] - self.position[0],
                node.get_position()[1] - self.position[1])
                
                
    def apply_friction(self, f):
        '''Applies friction dampening to the node.'''
        self.velocity[0] *= f
        self.velocity[1] *= f
        
        
    def update_position(self, boundingLengths=None, boundingOffset=(0, 0), boundingRadius=0):
        '''Uses the external force acting on the node to update its position.'''
        self.velocity[0] += self.externalForce[0]
        self.velocity[1] += self.externalForce[1]
        
        if abs(self.velocity[0]) < GraphNode.MINIMUMSPEED:
            self.velocity[0] = 0
        elif abs(self.velocity[0]) > GraphNode.MAXIMUMSPEED:
            self.velocity[0] = GraphNode.MAXIMUMSPEED
        if abs(self.velocity[1]) < GraphNode.MINIMUMSPEED:
            self.velocity[1] = 0
        elif abs(self.velocity[1]) > GraphNode.MAXIMUMSPEED:
            self.velocity[1] = GraphNode.MAXIMUMSPEED
        
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        #Keeping nodes within some bounding box, if needed
        if boundingLengths != None:
            if self.position[0] - boundingRadius < boundingOffset[0]:
                self.position[0] = boundingOffset[0] + boundingRadius
            elif self.position[0] + boundingRadius > boundingLengths[0] + boundingOffset[0]:
                self.position[0] = boundingLengths[0] + boundingOffset[0] - boundingRadius
                
            if self.position[1] - boundingRadius < boundingOffset[1]:
                self.position[1] = boundingOffset[1] + boundingRadius
            elif self.position[1] + boundingRadius > boundingLengths[1] + boundingOffset[1]:
                self.position[1] = boundingLengths[1] + boundingOffset[1] - boundingRadius
