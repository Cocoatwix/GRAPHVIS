
from GraphNode import GraphNode

class GraphConnection():
    
    def __init__(self, n1, n2, weight=0):
        self.start = n1
        self.end = n2
        self.weight = weight
    
    
    def get_start_node(self):
        '''Returns the starting node.'''
        return self.start
    
   
    def get_end_node(self):
        '''Returns the ending node.'''
        return self.end

    
    def get_start_position(self):
        '''Returns the starting position of the connection.'''
        return self.start.get_position()


    def get_end_position(self):
        '''Returns the ending position of the connection.'''
        return self.end.get_position()