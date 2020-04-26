from game import Agent
from game import Directions
import random

#Keys for the controlling the pacman by the user
class KeyboardAgent(Agent):
    # NOTE: Arrow keys also work.
    left_key  = 'a'
    right_key  = 'd'
    up_key = 'w'
    down_key = 's'
    end = 'q'

    def __init__( self, index = 0 ):

        self.last_move = Directions.STOP
        self.index = index
        self.keys = []

    def get_move( self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.get_legal_moves(self.index)
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.last_move in legal:
                move = self.last_move

        if (self.end in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.last_move = move
        return move

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.left_key in self.keys or 'Left' in self.keys) and Directions.left in legal:  move = Directions.left
        if   (self.right_key in self.keys or 'Right' in self.keys) and Directions.right in legal: move = Directions.right
        if   (self.up_key in self.keys or 'Up' in self.keys) and Directions.up in legal:   move = Directions.up
        if   (self.down_key in self.keys or 'Down' in self.keys) and Directions.down in legal: move = Directions.down
        return move
