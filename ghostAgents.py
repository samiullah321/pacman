from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def get_move( self, state ): #return an action
        dist = self.getDistribution(state) #evaluating the probabilities of attacking or fleeing using factors as distance from pacman etc.
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

#GHOST THAT CHOOSES AN ACTION RANDOMLY
class RandomGhost( GhostAgent ):
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.get_legal_moves( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist

#GHOST THAT CHOOSES AN ACTION SMARTLY
class DirectionalGhost( GhostAgent ):
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
         #setting the probabilities for the ghost to flee or attack
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.get_legal_moves( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors] #ghost positions
        pacmanPosition = state.get_pacman_coord() #pacman positions

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared: #chooose the position with the max distance from pacman and start to flee there
            max_score = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else: #choose the positions with the min distance from pacman and start to attack there
            max_score = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == max_score]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist
