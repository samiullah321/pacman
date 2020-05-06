from util import coords_distance
from state import Grid
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
        self.process_layout_text(layout_text) #taking the layout_text from the file
        self.layout_text = layout_text
        self.totalcoin = len(self.coin.as_list()) #total number of coins available

    def get_ghosts_count(self):
        return self.ghosts_count

    def is_wall(self, coord):
        x, col = coord
        return self.walls[x][col]

    def deep_copy(self):
        return Layout(self.layout_text[:])

    def process_layout_text(self, layout_text):
         # % - Wall
         # . - coin
         # o - Capsule
         # G - Ghost
         # P - Pacman
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layout_char = layout_text[maxY - y][x]
                self.process_layout_char(x, y, layout_char)
        self.agent_coord.sort()
        self.agent_coord = [ ( i == 0, coord) for i, coord in self.agent_coord]

    #Processing the charactter from the layout
    def process_layout_char(self, x, y, layout_char):
        if layout_char == '%':
            self.walls[x][y] = True
        elif layout_char == '.':
            self.coin[x][y] = True
        elif layout_char == 'o':
            self.big_coin.append((x, y))
        elif layout_char == 'P':
            self.agent_coord.append( (0, (x, y) ) )
        elif layout_char in ['G']:
            self.agent_coord.append( (1, (x, y) ) )
            self.ghosts_count += 1
        elif layout_char in  ['1', '2', '3', '4']:
            self.agent_coord.append( (int(layout_char), (x,y)))
            self.ghosts_count += 1

#RETREIVING THE LAYOUT
def get_layout(name, back = 2): #retrieving the layout from the directory
    if name.endswith('.lay'):
        layout = load_layout('layouts/' + name)
        if layout == None: layout = load_layout(name)
    else:
        layout = load_layout('layouts/' + name + '.lay')
        if layout == None: layout = load_layout(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = get_layout(name, back -1)
        os.chdir(curdir)
    return layout

def load_layout(layout_name):
    if(not os.path.exists(layout_name)): return None
    f = open(layout_name)
    try: return Layout([line.strip() for line in f])
    finally: f.close()
