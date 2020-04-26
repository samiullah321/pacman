from util import *
import time, os
import traceback
import sys
from GameLib import *

class Agent:
    #returns the index of the agent if any.
    def __init__(self, index=0):
        self.index = index

class Directions:
    #Strings defined for the direction (POLES)
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    #In case, pacman is going in a certain direction, its poles relative to it are defined below:

    LEFT =       {NORTH: WEST,
                   SOUTH: EAST,
                   EAST:  NORTH,
                   WEST:  SOUTH,
                   STOP:  STOP}

    RIGHT =      dict([(y,x) for x, y in list(LEFT.items())]) #right is the reverse of left

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}

class Configuration:

#takes in the initial position of the Pacman and its initial direction as the argument
    def __init__(self, coord, direction):
        self.coord = coord #coords
        self.direction = direction #direction of movement

    #UTILITY FUNCTIONS
    def get_coord(self):
        return (self.coord)

    def getDirection(self):
        return self.direction

    def isInteger(self):
        x,y = self.coord
        return x == int(x) and y == int(y)

    #converts position to direction vector to implement position on the pacman graph
    def produce_successor(self, vector):

        x, y= self.coord
        dx, dy = vector
        direction = Actions.vectorToDirection(vector)
        if direction == Directions.STOP:
            direction = self.direction # There is no stop direction
        return Configuration((x + dx, y+dy), direction)

class AgentState:

    #agent_states hold the state of an agent (configuration, speed, scared, etc).
    def __init__( self, startConfiguration, isPacman ):
        self.start = startConfiguration
        self.configuration = startConfiguration
        self.isPacman = isPacman #is the agent Pacman or ghost?
        self.scaredTimer = 0 #time until the ghost can be eaten

    def copy( self ):
        state = AgentState( self.start, self.isPacman )
        state.configuration = self.configuration
        state.scaredTimer = self.scaredTimer #time until which the agent would be eatable
        return state

    #UTILITY FUNCTIONS
    def get_coord(self):
        if self.configuration == None: return None
        return self.configuration.get_coord()

    def getDirection(self):
        return self.configuration.getDirection()

class Grid:

    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30 #cells per pixel
        #dimensions of the maze
        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)] #initializing array for the maze
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def copy(self): #returns a copy of the grid (deepcopy)
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self): #pointers to the grid passed
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item =True ): #returns number of items in the data
        return sum([x.count(item) for x in self.data])

    def asList(self, key = True): #return the Grid as a list
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key: list.append( (x,y) )
        return list

    def cell_index_to_coord(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def _unpackBits(self, bits):
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height: break
                x, y = self.cell_index_to_coord(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0: raise ValueError("must be a positive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools

def reconstituteGrid(bitRep):
    if type(bitRep) is not type((1,2)):
        return bitRep
    width, height = bitRep[:2]
    return Grid(width, height, bitRepresentation= bitRep[2:])

####################################
# Parts you shouldn't have to read #
####################################

class Actions:
    # Directions
    _directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0),
                   Directions.STOP:  (0, 0)}

    _directionsAsList = list(_directions.items())

    TOLERANCE = .001 #for transition of pacman between the grids

    def reverseDirection(action):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST
        return action
    reverseDirection = staticmethod(reverseDirection)

    def vectorToDirection(vector):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST
        return Directions.STOP
    vectorToDirection = staticmethod(vectorToDirection)

   #returning the direction as a vector, incorporated with the speed
    def direction_from_vector(direction, speed = 1.0):
        dx, dy =  Actions._directions[direction]
        return (dx * speed, dy * speed)
    direction_from_vector = staticmethod(direction_from_vector)

    #config is the current game_state of an agent
    def get_possible_moves(config, walls):
        possible = [] #initialized empty
        x, y = config.coord #gets the current coord of Pacman
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int)  > Actions.TOLERANCE):
            return [config.getDirection()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            #if the coords are not of the walls, then append to possible
            if not walls[next_x][next_y]: possible.append(dir)

        return possible

    get_possible_moves = staticmethod(get_possible_moves)

class game_state_data: #data pertaining to each state of the game

    def __init__( self, prevState = None ):
        if prevState != None:
            #MAINTAINING THE PREVIOUS STATE IN ORDER TO COMPARE
            self.coin = prevState.coin.shallowCopy()
            self.big_coin = prevState.big_coin[:]
            self.agent_states = self.copyagent_states( prevState.agent_states )
            self.layout = prevState.layout #previous maze layout
            self._eaten = prevState._eaten
            self.score = prevState.score

        #MAINTAINING STATES FOR THE AGENT
        self._coinEaten = None
        self._coinAdded = None
        self._capsuleEaten = None
        self._agentMoved = None #checking if the agent has moved from previous position
        self._lose = False #game lost
        self._win = False #game won
        self.scoreChange = 0

    def deepCopy( self ): #DEEP COPYING
        state = game_state_data( self )
        state.coin = self.coin.deepCopy()
        state.layout = self.layout.deepCopy()
        state._agentMoved = self._agentMoved
        state._coinEaten = self._coinEaten
        state._coinAdded = self._coinAdded
        state._capsuleEaten = self._capsuleEaten
        return state

    def copyagent_states( self, agent_states ):
        copiedStates = []
        for agentState in agent_states:
            copiedStates.append( agentState.copy() )
        return copiedStates

    def initialize( self, layout, numGhostAgents ):
        #creating the game_state from the layout (INITIAL STATE)
        self.coin = layout.coin.copy()
        #self.big_coin = []
        self.big_coin = layout.big_coin[:]
        self.layout = layout
        self.score = 0
        self.scoreChange = 0

        self.agent_states = []
        ghosts_count = 0
        for isPacman, coord in layout.agent_coord:
            if not isPacman:
                if ghosts_count == numGhostAgents: continue # Max ghosts reached already
                else: ghosts_count += 1
            self.agent_states.append( AgentState( Configuration( coord, Directions.STOP), isPacman) )
        self._eaten = [False for a in self.agent_states] #Checking that agent is eaten or not (as pacman can eat the agents)
