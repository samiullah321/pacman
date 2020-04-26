from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):

    # A reflex agent chooses action at each phase by using the evaluation function given below
    def get_move(self, game_state):
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_moves()

        scores = [self.evaluator(game_state, action) for action in
                  legal_moves]  # Choose the best action amongs the list of possible moves
        max_score = max(scores)  # max of the scores array is extracted
        max_score_indexs = [index for index in range(len(scores)) if
                       scores[index] == max_score]  # get indexes of the max_score in the score array
        random_index = random.choice(
            max_score_indexs)  # as there can be multiple max_scores that are the same, hence we chose any one randomly

        return legal_moves[random_index]

    def evaluator(self, current_game_state, action):  # This evaluation function is only for the Reflex agent

        # returns a score,the higher the score from evaluator the better
        # information taken into consideration from current state: remaining coin(new_coin), Pacman position after moving (new_coord), ScaredTimes of the ghosts

        next_game_state = current_game_state.produce_pac_successor(action)
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


def score_evaluator(current_game_state):
    # returns the score of the current game_state
    return current_game_state.getScore()


class MultiAgentSearchAgent(Agent):
    # Some variables and methods that are publically available to all Minimax, AlphaBetaAgent, and ExpectimaxAgent
    def __init__(self, evalFn='score_evaluator', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluator = util.lookup(evalFn, globals())
        self.depth = int(
            depth)  # the depth till which the game_state will be evaluated. The more the depth, the more accurate the result, however, time taken would be greater as more branches would be traversed


class MinimaxAgent(MultiAgentSearchAgent):
    # MINIMAX AGENT
    def get_move(self, game_state):
        # makes use of current game_state to return the proper action, given the depth and the evaluation function to be used.
        # all the agents have been tested without an evaluation function to see how they compare against the reflex agent

        # MAIN CODE
        num_agent = game_state.get_num_agents()  # pacman + ghosts
        # print(num_agent)
        action_score = []  # stores the legal move and their scores

        def remove_stop(List):  # shows the legal moves
            return [x for x in List if x != 'Stop']  # removing the stop action, as the pacman is not allowed to stop

        def miniMax(s, iteration_count):  # default depth is '2'
            # print(iteration_count)
            if iteration_count >= self.depth * num_agent or s.pac_won() or s.pac_lost():  # returning the score in case of agent count exceeding the depth for which the evaluation has to be done.
                return self.evaluator(s)  # using the evaluationFunnction to return the score
            if iteration_count % num_agent != 0:  # Ghost min (e.g 0,5,10 % 5 would be 0 which the index for the Pacman)
                result = 1e10  # +ve infinity

                # get_legal_moves is returning the legal actions for the agent specified. Index 0 represents Pacman and Index 1 onwards represents Ghosts

                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    sdot = s.produce_successor(iteration_count % num_agent,
                                               a)  # generating the successor  game_state for the action specified
                    result = min(result, miniMax(sdot,
                                                  iteration_count + 1))  # as the agent will minimize, hence choses the result with the minimum benefit
                return result
            else:  # Pacman Max
                result = -1e10  # -ve infinity
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    sdot = s.produce_successor(iteration_count % num_agent, a)  # same as above
                    result = max(result, miniMax(sdot,
                                                  iteration_count + 1))  # the pacman will try to maximize the result hence will chose the one with the max benefit
                    if iteration_count == 0:
                        action_score.append(result)
                return result

        result = miniMax(game_state, 0);  # initialiteration_count is 0
        # print (remove_stop(game_state.get_legal_moves(0)), action_score)
        return remove_stop(game_state.get_legal_moves(0))[
            action_score.index(max(action_score))]  # returning the action having the max score


class AlphaBetaAgent(MultiAgentSearchAgent):
    # ALPHA BETA AGENT
    def get_move(self, game_state):
        # Main Code
        num_agent = game_state.get_num_agents()
        action_score = []

        def remove_stop(List):
            return [x for x in List if x != 'Stop']

        # introduced two factor, alpha and beta here, in order to prune and not traverse all gamestates
        def alpha_beta(s, iteration_count, alpha, beta):
            if iteration_count >= self.depth * num_agent or s.pac_won() or s.pac_lost():
                return self.evaluator(s)
            if iteration_count % num_agent != 0:  # Ghost min
                result = 1e10
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    sdot = s.produce_successor(iteration_count % num_agent, a)
                    result = min(result, alpha_beta(sdot, iteration_count + 1, alpha, beta))
                    beta = min(beta, result)  # beta holds the minimum of the path travered till the root
                    if beta < alpha:  # Pruning. If beta is lesser than alpha, then we need not to traverse the other state
                        break
                return result
            else:  # Pacman Max
                result = -1e10
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    sdot = s.produce_successor(iteration_count % num_agent, a)
                    result = max(result, alpha_beta(sdot, iteration_count + 1, alpha, beta))
                    alpha = max(alpha, result)  # alpha holds the maxmimum of the path travered till the root
                    if iteration_count == 0:
                        action_score.append(result)
                    if beta < alpha:  # Prunning
                        break
                return result

        result = alpha_beta(game_state, 0, -1e20, 1e20)  # alpha and beta are set to -ve and +ve infinity as shown
        return remove_stop(game_state.get_legal_moves(0))[action_score.index(max(action_score))]


class ExpectimaxAgent(MultiAgentSearchAgent):
    # EXPECTIMAX AGENT
    def get_move(self, game_state):
        # Main Code
        num_agent = game_state.get_num_agents()
        action_score = []

        def remove_stop(List):
            return [x for x in List if x != 'Stop']

        def _expectMinimax(s, iteration_count):
            if iteration_count >= self.depth * num_agent or s.pac_won() or s.pac_lost():
                return self.evaluator(s)
            if iteration_count % num_agent != 0:  # Ghost min
                successorScore = []
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    sdot = s.produce_successor(iteration_count % num_agent, a)
                    result = _expectMinimax(sdot, iteration_count + 1)
                    successorScore.append(result)
                averageScore = sum([float(x) / len(successorScore) for x in
                                    successorScore])  # maintaing the average of the scores instead of the max or min
                return averageScore
            else:  # Pacman Max
                result = -1e10
                for a in remove_stop(s.get_legal_moves(iteration_count % num_agent)):
                    sdot = s.produce_successor(iteration_count % num_agent, a)
                    result = max(result, _expectMinimax(sdot, iteration_count + 1))
                    if iteration_count == 0:
                        action_score.append(result)
                return result

        result = _expectMinimax(game_state, 0);
        return remove_stop(game_state.get_legal_moves(0))[action_score.index(max(action_score))]
