from util import manhattanDistance
from game import Grid
import os
import random
from functools import reduce

class Layout: #maintains the information regarding the layout
    def __init__(self, layout_text):
        self.width = len(layout_text[0])
        self.height= len(layout_text)
        self.walls = Grid(self.width, self.height, False)
        self.coin = Grid(self.width, self.height, False)
        self.big_coin = []
        self.agent_coord = []
        self.ghosts_count = 0
        self.processlayout_text(layout_text) #taking the layout_text from the file
        self.layout_text = layout_text
        self.totalcoin = len(self.coin.asList()) #total number of coins available

    def get_ghosts_count(self):
        return self.ghosts_count

    def is_wall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def deepCopy(self):
        return Layout(self.layout_text[:])

    def processlayout_text(self, layout_text):
         # % - Wall
         # . - coin
         # o - Capsule
         # G - Ghost
         # P - Pacman
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layout_text[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)
        self.agent_coord.sort()
        self.agent_coord = [ ( i == 0, pos) for i, pos in self.agent_coord]

    #Processing the charactter from the layout
    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.coin[x][y] = True
        elif layoutChar == 'o':
            self.big_coin.append((x, y))
        elif layoutChar == 'P':
            self.agent_coord.append( (0, (x, y) ) )
        elif layoutChar in ['G']:
            self.agent_coord.append( (1, (x, y) ) )
            self.ghosts_count += 1
        elif layoutChar in  ['1', '2', '3', '4']:
            self.agent_coord.append( (int(layoutChar), (x,y)))
            self.ghosts_count += 1

#RETREIVING THE LAYOUT
def getLayout(name, back = 2): #retrieving the layout from the directory
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name)
        if layout == None: layout = tryToLoad(name)
    else:
        layout = tryToLoad('layouts/' + name + '.lay')
        if layout == None: layout = tryToLoad(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back -1)
        os.chdir(curdir)
    return layout

def tryToLoad(fullname):
    if(not os.path.exists(fullname)): return None
    f = open(fullname)
    try: return Layout([line.strip() for line in f])
    finally: f.close()
