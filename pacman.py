from game import GameStateData
from game import Directions
from game import Actions
from util import nearestPoint
from util import manhattanDistance
import util, layout
import sys, types, time, random, os
from GameLib import *
from datetime import datetime

class GameState: #has accessor methods for accessing variables of GameStateData object

    #specifies the full game state, including the coin, capsules, agent configurations and score changes.
    #used by the Game object to capture the actual state of the game and can be used by agents to reason about the game.

    # Accessor methods
    explored = set() #keeps track of which states have had get_legal_moves called

    def get_legal_moves( self, agentIndex=0 ): #can help in assessing the actions that will help maximize or mimimize agents chances of winning

        if self.isWin() or self.isLose(): return [] #we can have no legal actions for terminal state

        if agentIndex == 0: #if it is pacman then
            return PacmanRules.get_legal_moves( self ) #getting the legal actions for the PACMAN
        else:
            return GhostRules.get_legal_moves( self, agentIndex ) #getting the legal actions for the Ghost

    def generateSuccessor( self, agentIndex, action): #Returns the successor game state after an agent takes an action (predicted gameState)
        #checking that action can be applied or not
        if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

        #copying the current state
        state = GameState(self)

        if agentIndex == 0: #if the agent is Pacman then...
            state.data._eaten = [False for i in range(state.getNumAgents())] #maintains which agent has been eaten. In case of pacman, only the ghosts will be set to true if eaten
            PacmanRules.applyAction( state, action ) #apply the action on the pacman
        else:
            GhostRules.applyAction( state, action, agentIndex )

        #penalty being incurred per unit time
        if agentIndex == 0:
            state.data.scoreChange += -TIME_PENALTY # decreasing score on wasting time
        else:
            GhostRules.decrementTimer( state.data.agentStates[agentIndex] ) #the timer for the ghost's scared state to finish

        #checking whehter
        GhostRules.checkDeath( state, agentIndex ) #checks pacman's death

        #setting which agent has moved and the score state
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        #adding the state to already explored state
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getLegalPacmanActions( self ):
        return self.get_legal_moves( 0 )

    def generatePacmanSuccessor( self, action ):
        return self.generateSuccessor( 0, action ) #applying the action on the pacman

    def getPacmanState( self ):
        #returns the current state of Pacman (pos, direction)
        return self.data.agentStates[0].copy()

    def get_pacman_coord( self ):
        return self.data.agentStates[0].getPosition() #return the pacman's current position

    def getGhostStates( self ):
        return self.data.agentStates[1:] #getting the states for all the ghosts

    def getGhostState( self, agentIndex ):
        if agentIndex == 0 or agentIndex >= self.getNumAgents():
            raise Exception("Invalid index passed to getGhostState")
        return self.data.agentStates[agentIndex]

    def getGhostPosition( self, agentIndex ):
        if agentIndex == 0:
            raise Exception("Pacman's index passed to getGhostPosition")
        return self.data.agentStates[agentIndex].getPosition()

    def getGhostPositions(self):
        return [s.getPosition() for s in self.getGhostStates()]

    def getNumAgents( self ):
        return len( self.data.agentStates )

    def getScore( self ):
        return float(self.data.score)

    def getCapsules(self):
        return self.data.capsules #returning the remaining capsule positions

    def getNumcoin( self ):
        return self.data.coin.count() #getting the remaining coin on the maze

    def get_coin(self):
        return self.data.coin #return a 2d array of boolean indicating presence of coin on each location

    def getWalls(self):
        return self.data.layout.walls #return a 2d array of boolean indicating presence of wall on each location

    def hascoin(self, x, y):
        return self.data.coin[x][y] #checking whether the index specified has the coin or not

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y] #checking whether the index specified is a wall or not

    def isLose( self ):
        return self.data._lose

    def isWin( self ):
        return self.data._win

    def __init__( self, prevState = None ):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None: # Initial state
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def deepCopy( self ): #allowing for deep copy of the data attribute of the GameState
        state = GameState( self )
        state.data = self.data.deepCopy()
        return state

    def initialize( self, layout, numGhostAgents=1000 ):
        self.data.initialize(layout, numGhostAgents) #used to create the initial layout of the maze

SCARED_TIME = 40    # time till which ghosts are scared
COLLISION_TOLERANCE = 0.7 # How close ghosts must be to Pacman to kill
TIME_PENALTY = 1 # Number of points lost when pacman not eating coin

class ClassicGameRules:

    def newGame( self, layout, pacmanAgent, ghostAgents, display, quiet = False):
        #taking all the state values for the new game
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize( layout, len(ghostAgents) )
        game = Game(agents, display, self)
        game.state = initState
        self.initialState = initState.deepCopy()
        self.quiet = quiet
        return game

    def process(self, state, game): #checking whether game state is a win or a loss
        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)

    def win( self, state, game ): #printing win
        if not self.quiet: print("Pacman emerges victorious! Score: %d" % state.data.score)
        game.gameOver = True

    def lose( self, state, game ): # printing loss
        if not self.quiet: print("Pacman died! Score: %d" % state.data.score)
        game.gameOver = True

    def getProgress(self, game): #returning how much coin eaten from the start
        return float(game.state.getNumcoin()) / self.initialState.getNumcoin()

    def agentCrash(self, game, agentIndex):
        if agentIndex == 0:
            print("Pacman crashed")
        else:
            print("A ghost crashed")

    def getMaxTimeWarnings(self, agentIndex):
        return 0

class PacmanRules:
    #functions for the pacman
    PACMAN_SPEED=1 #speed of the pacman has been set to one (same as that for the ghosts)

    def get_legal_moves( state ):
        return Actions.getPossibleActions( state.getPacmanState().configuration, state.data.layout.walls ) #returns the possible directions for pacman to move
    get_legal_moves = staticmethod( get_legal_moves )

    def applyAction( state, action ): # applying the action received on the pacman
        legal = PacmanRules.get_legal_moves( state )
        if action not in legal:
            raise Exception("Illegal action " + str(action))
        pacmanState = state.data.agentStates[0]
        vector = Actions.directionToVector( action, PacmanRules.PACMAN_SPEED ) #updating the pacman config
        pacmanState.configuration = pacmanState.configuration.generateSuccessor( vector )
        #eating coin
        next = pacmanState.configuration.getPosition()
        nearest = nearestPoint( next )
        if manhattanDistance( nearest, next ) <= 0.5 :#remove the coin when eaten
            PacmanRules.consume( nearest, state )
    applyAction = staticmethod( applyAction )

    def consume( position, state ):
        x,y = position
        if state.data.coin[x][y]: #consuming the coin
            state.data.scoreChange += 10 #incrementing the score on consuming
            state.data.coin = state.data.coin.copy()
            state.data.coin[x][y] = False #the item is now removed from its position
            state.data._coinEaten = position
            #checking whether all the coin has been eaten or not
            numcoin = state.getNumcoin()
            if numcoin == 0 and not state.data._lose:
                state.data.scoreChange += 500
                state.data._win = True
        #eating the bcoin
        if( position in state.getCapsules() ): #now all ghost agents are eatable
            state.data.capsules.remove( position )
            state.data._capsuleEaten = position
            #Reset all ghosts' scared timers
            for index in range( 1, len( state.data.agentStates ) ):
                state.data.agentStates[index].scaredTimer = SCARED_TIME #all the ghosts are now in scared mode once the coin has been eaten
    consume = staticmethod( consume )

class GhostRules:
    #functions for the ghost interacting with the enviroment
    GHOST_SPEED=1.0 # speed of ghost and pacman is same
    def get_legal_moves( state, ghostIndex ): #getting the LegalActions for the ghost
        conf = state.getGhostState( ghostIndex ).configuration
        possibleActions = Actions.getPossibleActions( conf, state.data.layout.walls )
        reverse = Actions.reverseDirection( conf.direction )
        if Directions.STOP in possibleActions:
            possibleActions.remove( Directions.STOP ) #the ghost should not stop
        if reverse in possibleActions and len( possibleActions ) > 1: #if there is any other legal action except reversing the direction then remove reverse (cannot remove until dead end)
            possibleActions.remove( reverse )
        return possibleActions
    get_legal_moves = staticmethod( get_legal_moves )

    def applyAction( state, action, ghostIndex): #applying the action by getting the LegalActions possible

        legal = GhostRules.get_legal_moves( state, ghostIndex )
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0: speed /= 2.0 #decreasing the speed of the ghost in scared state
        vector = Actions.directionToVector( action, speed )
        ghostState.configuration = ghostState.configuration.generateSuccessor( vector ) #applying the action to the ghostState
    applyAction = staticmethod( applyAction )

    def decrementTimer( ghostState): #this will decrerement the timer for the ghost being scared
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint( ghostState.configuration.pos )
        ghostState.scaredTimer = max( 0, timer - 1 ) #the timer cannot be below zero
    decrementTimer = staticmethod( decrementTimer )

    def checkDeath( state, agentIndex): #checking whether the pacman and the ghost has collided or not
        pacmanPosition = state.get_pacman_coord()
        if agentIndex == 0: # Pacman just moved; Anyone can kill him
            for index in range( 1, len( state.data.agentStates ) ): #checking pacman has been killed by which ghost hence using a loop to check
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                if GhostRules.canKill( pacmanPosition, ghostPosition ):
                    GhostRules.collide( state, ghostState, index )
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill( pacmanPosition, ghostPosition ):
                GhostRules.collide( state, ghostState, agentIndex ) # setting the index of the ghost that killed the pacman
    checkDeath = staticmethod( checkDeath )

    def collide( state, ghostState, agentIndex): #sets the state on collision of pacman and the ghost
        if ghostState.scaredTimer > 0: #if the ghost is scared and still collides
            state.data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            # Added for first-person
            state.data._eaten[agentIndex] = True # the agent is now eaten
        else:
            if not state.data._win:
                state.data.scoreChange -= 500
                state.data._lose = True #the game is lost as pacman is eaten
    collide = staticmethod( collide )

    def canKill( pacmanPosition, ghostPosition ):
        #ghost and pacman distance is less that than the tolerance defined than its a kill
        return manhattanDistance( ghostPosition, pacmanPosition ) <= COLLISION_TOLERANCE
    canKill = staticmethod( canKill )

    def placeGhost(state, ghostState): #placing ghost agents at their proper positions
        ghostState.configuration = ghostState.start
    placeGhost = staticmethod( placeGhost )

#STARTING THE GAME

def default(str):
    return str + ' [Default: %default]'

def parseAgentArgs(str):
    if str == None: return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key,val = p, 1
        opts[key] = val
    return opts

def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = ""

    parser = OptionParser(usageStr)

    #ADDING THE PARSING OPTIONS
    parser.add_option('-n', '--numGames', dest='numGames', type='int',
                      help=default('the number of GAMES to play'), metavar='GAMES', default=1)
    parser.add_option('-l', '--layout', dest='layout',
                      help=default('the LAYOUT_FILE from which to load the map layout'),
                      metavar='LAYOUT_FILE', default='mediumClassic')
    parser.add_option('-p', '--pacman', dest='pacman',
                      help=default('the agent TYPE in the pacmanAgents module to use'),
                      metavar='TYPE', default='KeyboardAgent')
    parser.add_option('-q', '--quietTextGraphics', action='store_true', dest='quietGraphics',
                      help='Generate minimal output and no graphics', default=False)
    parser.add_option('-g', '--ghosts', dest='ghost',
                      help=default('the ghost agent TYPE in the ghostAgents module to use'),
                      metavar = 'TYPE', default='RandomGhost')
    parser.add_option('-k', '--numghosts', type='int', dest='numGhosts',
                      help=default('The maximum number of ghosts to use'), default=4)
    parser.add_option('-a','--agentArgs',dest='agentArgs',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('--frameTime', dest='frameTime', type='float',
                      help=default('Time to delay between frames; <0 means keyboard'), default=0.1)

    options, otherjunk = parser.parse_args(argv)
    #error command generated
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    #setting the layout
    args['layout'] = layout.getLayout( options.layout )
    if args['layout'] == None: raise Exception("The layout " + options.layout + " cannot be found") #in case of the layout not being found

    # Choose a Pacman agent
    noKeyboard = False
    pacmanType = loadAgent(options.pacman, noKeyboard)
    agentOpts = parseAgentArgs(options.agentArgs)
    pacman = pacmanType(**agentOpts) # Instantiate Pacman with agentArgs
    args['pacman'] = pacman

    # Choose a ghost agent
    ghostType = loadAgent(options.ghost, noKeyboard)
    args['ghosts'] = [ghostType( i+1 ) for i in range( options.numGhosts )]

    # Choose a display format
    if options.quietGraphics:
        import textDisplay
        args['display'] = textDisplay.NullGraphics()
    else:
        import graphicsDisplay
        args['display'] = graphicsDisplay.PacmanGraphics(frameTime = options.frameTime)
    args['numGames'] = options.numGames

    return args

def loadAgent(pacman, nographics):
    # Looks through all pythonPath Directories for the right module,
    pythonPathStr = os.path.expandvars("$PYTHONPATH")
    if pythonPathStr.find(';') == -1:
        pythonPathDirs = pythonPathStr.split(':')
    else:
        pythonPathDirs = pythonPathStr.split(';')
    pythonPathDirs.append('.')

    for moduleDir in pythonPathDirs:
        if not os.path.isdir(moduleDir): continue
        moduleNames = [f for f in os.listdir(moduleDir) if f.endswith('gents.py')]
        for modulename in moduleNames:
            try:
                module = __import__(modulename[:-3])
            except ImportError:
                continue
            if pacman in dir(module):
                if nographics and modulename == 'keyboardAgents.py':
                    raise Exception('Using the keyboard requires graphics (not text display)')
                return getattr(module, pacman)
    raise Exception('The agent ' + pacman + ' is not specified in any *Agents.py.')

def runGames( layout, pacman, ghosts, display, numGames):
    import __main__
    __main__.__dict__['_display'] = display

    rules = ClassicGameRules()
    games = []

    for i in range( numGames ):
        beQuiet = i < 0
        if beQuiet:
                # Suppress output and graphics
            import textDisplay
            gameDisplay = textDisplay.NullGraphics()
            rules.quiet = True
        else:
            gameDisplay = display
            rules.quiet = False
        game = rules.newGame( layout, pacman, ghosts, gameDisplay, beQuiet)
        game.run()
        if not beQuiet: games.append(game)

    if (numGames) > 0:
        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]
        winRate = wins.count(True)/ float(len(wins))

        AvgWin = []
        CapCount = 0
        for game in games:
            if game.state.isWin():
                AvgWin.append(game.state.getScore())
            if len(game.state.getCapsules())==0:
                CapCount += 1

        print('The game finished all capsules', float(CapCount)/float(numGames))
        print('Average Score:', sum(scores) / float(len(scores)))
        if(len(AvgWin) != 0):
            print('Average Win Score', float(sum(AvgWin))/float(len(AvgWin)))
        else:
            print('No games won!')
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate))
        print('Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins]))

    return games

if __name__ == '__main__':
    args = readCommand( sys.argv[1:] ) # Get game components based on input
    runGames( **args )
    pass
