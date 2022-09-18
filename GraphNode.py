
class GraphNode():

    def __init__(self, label, pos=(0, 0)):
        self.label = label
        self.position = [pos[0], pos[1]]
        self.externalForce = [0, 0]
        
        
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
        
        
    def update_position(self):
        '''Uses the external force acting on the node to update its position.'''
        self.position[0] += self.externalForce[0]
        self.position[1] += self.externalForce[1]