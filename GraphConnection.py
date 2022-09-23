
from GraphNode import GraphNode

class GraphConnection():
    
    def __init__(self, n1, n2, weight=0):
        self.start = n1
        self.end = n2
        self.startID = 0
        self.endID = 0
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


    def get_startID(self):
        '''Returns startID.'''
        return self.startID


    def get_endID(self):
        '''Returns endID.'''
        return self.endID


    def set_startID(self, ID):
        '''Sets start ID so that the manager can more quickly calculate connection forces.'''
        self.startID = ID


    def set_endID(self, ID):
        '''Sets end ID so that the manager can more quickly calculate connection forces.'''
        self.endID = ID
