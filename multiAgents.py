from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):

    # A reflex agent chooses action at each phase by using the evaluation function given below
    def get_move(self, gameState):
        # Collect legal moves and successor states
        legal_moves = gameState.get_legal_moves()

        scores = [self.evaluator(gameState, action) for action in
                  legal_moves]  # Choose the best action amongs the list of possible moves
        max_score = max(scores)  # max of the scores array is extracted
        max_score_indexs = [index for index in range(len(scores)) if
                       scores[index] == max_score]  # get indexes of the max_score in the score array
        random_index = random.choice(
            max_score_indexs)  # as there can be multiple max_scores that are the same, hence we chose any one randomly

        return legal_moves[random_index]

    def evaluator(self, currentGameState, action):  # This evaluation function is only for the Reflex agent

        # returns a score,the higher the score from evaluator the better
        # information taken into consideration from current state: remaining coin(new_coin), Pacman position after moving (new_coord), ScaredTimes of the ghosts

        next_game_state = currentGameState.produce_pac_successor(action)
        new_coord = next_game_state.get_pacman_coord()  # taking the pacman position after moving
        new_coin = next_game_state.get_coin()  # taking the remaining coin
        # taking the remaining scaredtimes of the ghosts
        new_ghost_states = next_game_state.get_ghost_states()
        new_ghost_scrared_timer = [ghostState.scaredTimer for ghostState in new_ghost_states]

        # REFLEX AGENT CODE
        coinPos = new_coin.asList()
        coinCount = len(coinPos)  # number of coin available
        nearest_distance = 1e6  # initially set to infinite
        for i in range(coinCount):
            distance = manhattanDistance(coinPos[i], new_coord) + coinCount * 100
            if distance < nearest_distance:  # find the closest available coin
                nearest_distance = distance
                closestcoin = coinPos
        if coinCount == 0:
            nearest_distance = 0
        score = -nearest_distance  # the step needed to reach the coin are subtracted from the score, predicting the score after pacman tries to eat that coin

        for i in range(len(new_ghost_states)):
            # getting the positions of each ghost and checking whether it has eaten pacman or not
            ghost_coord = next_game_state.get_ghost_coord(i + 1)
            if manhattanDistance(new_coord, ghost_coord) <= 1:  # if pacman dies
                score -= 1e6  # the score when the pacman dies

        return score  # next_game_state.getScore()


def scoreevaluator(currentGameState):
    # returns the score of the current gameState
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    # Some variables and methods that are publically available to all Minimax, AlphaBetaAgent, and ExpectimaxAgent
    def __init__(self, evalFn='scoreevaluator', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluator = util.lookup(evalFn, globals())
        self.depth = int(
            depth)  # the depth till which the gamestate will be evaluated. The more the depth, the more accurate the result, however, time taken would be greater as more branches would be traversed


class MinimaxAgent(MultiAgentSearchAgent):
    # MINIMAX AGENT
    def get_move(self, gameState):
        # makes use of current GameState to return the proper action, given the depth and the evaluation function to be used.
        # all the agents have been tested without an evaluation function to see how they compare against the reflex agent

        # MAIN CODE
        num_agent = gameState.getNumAgents()  # pacman + ghosts
        # print(num_agent)
        ActionScore = []  # stores the legal move and their scores

        def _rmStop(List):  # shows the legal moves
            return [x for x in List if x != 'Stop']  # removing the stop action, as the pacman is not allowed to stop

        def _miniMax(s, iterCount):  # default depth is '2'
            # print(iterCount)
            if iterCount >= self.depth * num_agent or s.isWin() or s.isLose():  # returning the score in case of agent count exceeding the depth for which the evaluation has to be done.
                return self.evaluator(s)  # using the evaluationFunnction to return the score
            if iterCount % num_agent != 0:  # Ghost min (e.g 0,5,10 % 5 would be 0 which the index for the Pacman)
                result = 1e10  # +ve infinity

                # get_legal_moves is returning the legal actions for the agent specified. Index 0 represents Pacman and Index 1 onwards represents Ghosts

                for a in _rmStop(s.get_legal_moves(iterCount % num_agent)):
                    sdot = s.generateSuccessor(iterCount % num_agent,
                                               a)  # generating the successor  gameState for the action specified
                    result = min(result, _miniMax(sdot,
                                                  iterCount + 1))  # as the agent will minimize, hence choses the result with the minimum benefit
                return result
            else:  # Pacman Max
                result = -1e10  # -ve infinity
                for a in _rmStop(s.get_legal_moves(iterCount % num_agent)):
                    sdot = s.generateSuccessor(iterCount % num_agent, a)  # same as above
                    result = max(result, _miniMax(sdot,
                                                  iterCount + 1))  # the pacman will try to maximize the result hence will chose the one with the max benefit
                    if iterCount == 0:
                        ActionScore.append(result)
                return result

        result = _miniMax(gameState, 0);  # initialiterCount is 0
        # print (_rmStop(gameState.get_legal_moves(0)), ActionScore)
        return _rmStop(gameState.get_legal_moves(0))[
            ActionScore.index(max(ActionScore))]  # returning the action having the max score


class AlphaBetaAgent(MultiAgentSearchAgent):
    # ALPHA BETA AGENT
    def get_move(self, gameState):
        # Main Code
        num_agent = gameState.getNumAgents()
        ActionScore = []

        def _rmStop(List):
            return [x for x in List if x != 'Stop']

        # introduced two factor, alpha and beta here, in order to prune and not traverse all gamestates
        def _alphaBeta(s, iterCount, alpha, beta):
            if iterCount >= self.depth * num_agent or s.isWin() or s.isLose():
                return self.evaluator(s)
            if iterCount % num_agent != 0:  # Ghost min
                result = 1e10
                for a in _rmStop(s.get_legal_moves(iterCount % num_agent)):
                    sdot = s.generateSuccessor(iterCount % num_agent, a)
                    result = min(result, _alphaBeta(sdot, iterCount + 1, alpha, beta))
                    beta = min(beta, result)  # beta holds the minimum of the path travered till the root
                    if beta < alpha:  # Pruning. If beta is lesser than alpha, then we need not to traverse the other state
                        break
                return result
            else:  # Pacman Max
                result = -1e10
                for a in _rmStop(s.get_legal_moves(iterCount % num_agent)):
                    sdot = s.generateSuccessor(iterCount % num_agent, a)
                    result = max(result, _alphaBeta(sdot, iterCount + 1, alpha, beta))
                    alpha = max(alpha, result)  # alpha holds the maxmimum of the path travered till the root
                    if iterCount == 0:
                        ActionScore.append(result)
                    if beta < alpha:  # Prunning
                        break
                return result

        result = _alphaBeta(gameState, 0, -1e20, 1e20)  # alpha and beta are set to -ve and +ve infinity as shown
        return _rmStop(gameState.get_legal_moves(0))[ActionScore.index(max(ActionScore))]


class ExpectimaxAgent(MultiAgentSearchAgent):
    # EXPECTIMAX AGENT
    def get_move(self, gameState):
        # Main Code
        num_agent = gameState.getNumAgents()
        ActionScore = []

        def _rmStop(List):
            return [x for x in List if x != 'Stop']

        def _expectMinimax(s, iterCount):
            if iterCount >= self.depth * num_agent or s.isWin() or s.isLose():
                return self.evaluator(s)
            if iterCount % num_agent != 0:  # Ghost min
                successorScore = []
                for a in _rmStop(s.get_legal_moves(iterCount % num_agent)):
                    sdot = s.generateSuccessor(iterCount % num_agent, a)
                    result = _expectMinimax(sdot, iterCount + 1)
                    successorScore.append(result)
                averageScore = sum([float(x) / len(successorScore) for x in
                                    successorScore])  # maintaing the average of the scores instead of the max or min
                return averageScore
            else:  # Pacman Max
                result = -1e10
                for a in _rmStop(s.get_legal_moves(iterCount % num_agent)):
                    sdot = s.generateSuccessor(iterCount % num_agent, a)
                    result = max(result, _expectMinimax(sdot, iterCount + 1))
                    if iterCount == 0:
                        ActionScore.append(result)
                return result

        result = _expectMinimax(gameState, 0);
        return _rmStop(gameState.get_legal_moves(0))[ActionScore.index(max(ActionScore))]
