from graphicsUtils import *
import math, time
from game import Directions

#Settings for the display
grdi_size = 30.0
info_height = 35
background_color = format_color(0,0,0)
wall_color = format_color(64/255.0, 224/255.0, 208/255.0)
info_color = format_color(.4,.4,0)
score_color = format_color(.9, .9, .9)
pac_outline = 2

#Settings for Ghost
ghost_colors = []
ghost_colors.append(format_color(.9,0,0)) # Red
ghost_colors.append(format_color(0,.3,.9)) # Blue
ghost_colors.append(format_color(.98,.41,.07)) # Orange
ghost_colors.append(format_color(.1,.75,.7)) # Green
ghost_colors.append(format_color(1.0,0.6,0.0)) # Yellow
ghost_colors.append(format_color(.4,0.13,0.91)) # Purple

#colors of all the ghosts
TEAM_COLORS = ghost_colors[:2]

#defines the dimensions of the ghost
GHOST_SHAPE = [
    (0, 1),
    (1, 0),
    (0, - 1),
    (-1, 0),
  ]
GHOST_SIZE = 0.65
SCARED_COLOR = format_color(1,1,1)

GHOST_VEC_COLORS = list(map(color_to_vector, ghost_colors))

#Some attributes of Pacman
PACMAN_COLOR = format_color(255.0/255.0,255.0/255.0,61.0/255)
PACMAN_SCALE = 0.5
#pacman_speed = 0.25

#coin config
coin_COLOR = format_color(0.81,0.7,0.22)
coin_SIZE = 0.1

#bcoin config
CAPSULE_COLOR = format_color(0.9,0,0)
CAPSULE_SIZE = 0.20

#wall config
WALL_RADIUS = 0.05

class InfoPane:
    def __init__(self, layout, gridSize):
        #Starting pane attributes
        self.gridSize = gridSize
        self.width = (layout.width) * gridSize
        self.base = (layout.height + 1) * gridSize
        self.height = info_height
        self.fontSize = 24
        self.textColor = PACMAN_COLOR
        self.drawPane()

    def toScreen(self, coord, y = None): #Maps the positions from layout onto the screen
        if y == None:
            x,y = coord
        else:
            x = coord

        x = self.gridSize + x # Margin
        y = self.base + y
        return x,y

    def drawPane(self):
        self.scoreText = text( self.toScreen(0, 0  ), self.textColor, "SCORE:    0", "Times", self.fontSize, "bold")

    def initializeGhostDistances(self, distances): #initializing ghost onto the screen
        self.ghostDistanceText = []

        size = 20
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = text( self.toScreen(self.width/2 + self.width/8 * i, 0), ghost_colors[i+1], d, "Times", size, "bold")
            self.ghostDistanceText.append(t)

    def updateScore(self, score):
        changeText(self.scoreText, "SCORE: % 4d" % score)

    def updateGhostDistances(self, distances):
        if len(distances) == 0: return
        if 'ghostDistanceText' not in dir(self): self.initializeGhostDistances(distances)
        else:
            for i, d in enumerate(distances):
                changeText(self.ghostDistanceText[i], d)

class PacmanGraphics: #general graphics for pacman
    def __init__(self, frameTime=0.0):
        self.have_window = 0
        self.currentGhostImages = {}
        self.pacmanImage = None
        self.gridSize = grdi_size
        self.frameTime = frameTime

    def checkNullDisplay(self):
        return False

    def initialize(self, state, isBlue = False):
        self.isBlue = isBlue
        self.startGraphics(state)
        self.distributionImages = None  # Initialized lazily
        self.drawStaticObjects(state)
        self.drawAgentObjects(state)

        # Information
        self.previousState = state

    def startGraphics(self, state): #initializing the graphics onto the screen
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPane(layout, self.gridSize)
        self.currentState = layout

    #drawing the walls onto the screen
    def drawDistributions(self, state):
        walls = state.layout.walls
        dist = []
        for x in range(walls.width):
            distx = []
            dist.append(distx)
            for y in range(walls.height):
                ( screen_x, screen_y ) = self.to_screen( (x, y) )
                block = square( (screen_x, screen_y),
                                0.5 * self.gridSize,
                                color = background_color,
                                filled = 1, behind=2)
                distx.append(block)
        self.distributionImages = dist

    #drawing coin and bcoin onto the screen
    def drawStaticObjects(self, state):
        layout = self.layout
        self.drawWalls(layout.walls)
        self.coin = self.drawcoin(layout.coin)
        self.big_coin = self.drawbig_coin(layout.big_coin)
        refresh()

    #drawing the pacman, ghost onto the screen
    def drawAgentObjects(self, state):
        self.agentImages = [] # (agentState, image)
        for index, agent in enumerate(state.agent_states):
            if agent.isPacman:
                image = self.drawPacman(agent, index)
                self.agentImages.append( (agent, image) )
            else:
                image = self.drawGhost(agent, index)
                self.agentImages.append( (agent, image) )
        refresh()

    #updates currentState to the newState recieved
    def update(self, newState):
        #updating the agent moved
        agent_index = newState.agent_moved
        agentState = newState.agent_states[agent_index]

        prevState, prevImage = self.agentImages[agent_index]
        if agentState.isPacman:
            self.animate_pacman_movement(agentState, prevState, prevImage) #moving pacman
        else:
            self.moveGhost(agentState, agent_index, prevState, prevImage) #animating or moving the ghost
        self.agentImages[agent_index] = (agentState, prevImage)

        if newState.coin_eaten != None:
            self.removecoin(newState.coin_eaten, self.coin) #if the coin is eaten, remove it from its position in new state
        if newState.big_food_Eaten != None:
            self.removeCapsule(newState.big_food_Eaten, self.big_coin) #same as coin
        self.infoPane.updateScore(newState.score)
        if 'ghostDistances' in dir(newState):
            self.infoPane.updateGhostDistances(newState.ghostDistances) #updating the ghost distances here

    def make_window(self, width, height): #initializing the screen
        grid_width = (width-1) * self.gridSize
        grid_height = (height-1) * self.gridSize
        screen_width = 2*self.gridSize + grid_width
        screen_height = 2*self.gridSize + grid_height + info_height

        #starting the screen
        begin_graphics(screen_width,
                       screen_height,
                       background_color,
                       "PACMAN MULTI-AGENT SIMULATION")

    #drawing the pacman
    def drawPacman(self, pacman, index):
        position = self.get_coord(pacman)
        screen_point = self.to_screen(position)
        endpoints = self.getEndpoints(self.getDirection(pacman))

        width = pac_outline
        outlineColor = PACMAN_COLOR
        fillColor = PACMAN_COLOR

        return [circle(screen_point, PACMAN_SCALE * self.gridSize,
                       fillColor = fillColor, outlineColor = outlineColor,
                       endpoints = endpoints,
                       width = width)]

    #used for rotating pacman according to direction
    def getEndpoints(self, direction, position=(0, 0)):
        x, y = position
        coord = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi * coord)

        delta = width / 2
        if (direction == 'left'):
            endpoints = (180 + delta, 180 - delta)
        elif (direction == 'up'):
            endpoints = (90 + delta, 90 - delta)
        elif (direction == 'down'):
            endpoints = (270 + delta, 270 - delta)
        else:
            endpoints = (0 + delta, 0 - delta)
        return endpoints

    #for moving the pacman
    def move_pacman(self, position, direction, image):
        screen_coord = self.to_screen(position)
        endpoints = self.getEndpoints( direction, position )
        r = PACMAN_SCALE * self.gridSize
        moveCircle(image[0], screen_coord, r, endpoints)
        refresh()

    #animation of pacman when moving from cell to cell
    def animate_pacman_movement(self, pacman, prevPacman, image):
        if self.frameTime < 0:
            print('Press any key to step forward, "q" to play')
            keys = wait_for_keys()
            if 'q' in keys:
                self.frameTime = 0.1
        if self.frameTime > 0.01 or self.frameTime < 0:
            start = time.time()
            fx, fy = self.get_coord(pacman)
            px, py = self.get_coord(pacman)
            frames = 4.0
            for i in range(1,int(frames) + 1):
                coord = px*i/frames + fx*(frames-i)/frames, py*i/frames + fy*(frames-i)/frames
                self.move_pacman(coord, self.getDirection(pacman), image)
                refresh()
                sleep(abs(self.frameTime) / frames)
        else:
            self.move_pacman(self.get_coord(pacman), self.getDirection(pacman), image)
        refresh()

    #retreiving the ghost color
    def get_ghost_color(self, ghost, ghostIndex):
        if ghost.scared_timer > 0:
            return SCARED_COLOR
        else:
            return ghost_colors[ghostIndex]

    #drawing the ghost
    def drawGhost(self, ghost, agent_index):
        coord = self.get_coord(ghost)
        dir = self.getDirection(ghost)
        (screen_x, screen_y) = (self.to_screen(coord) )
        coords = []
        for (x, y) in GHOST_SHAPE:
            coords.append((x*self.gridSize*GHOST_SIZE + screen_x, y*self.gridSize*GHOST_SIZE + screen_y))

        colour = self.get_ghost_color(ghost, agent_index)
        body = polygon(coords, colour, filled = 1)
        WHITE = format_color(1.0, 1.0, 1.0)
        BLACK = format_color(0.0, 0.0, 0.0)

        dx = 0
        dy = 0
        if dir == 'up':
            dy = -0.2
        if dir == 'down':
            dy = 0.2
        if dir == 'right':
            dx = 0.2
        if dir == 'left':
            dx = -0.2

        ghostImageParts = []
        ghostImageParts.append(body)

        return ghostImageParts

    #moving the ghost
    def moveGhost(self, ghost, ghostIndex, prevGhost, ghostImageParts):
        #animation of ghost movement
        old_x, old_y = self.to_screen(self.get_coord(prevGhost))
        new_x, new_y = self.to_screen(self.get_coord(ghost))
        delta = new_x - old_x, new_y - old_y

        for ghostImagePart in ghostImageParts:
            move_by(ghostImagePart, delta)
        refresh()

        if ghost.scared_timer > 0:
            color = SCARED_COLOR #setting the color of scared state
        else:
            color = ghost_colors[ghostIndex]
        edit(ghostImageParts[0], ('fill', color), ('outline', color))
        refresh()

    #get coords on the screen
    def get_coord(self, agentState):
        if agentState.configuration == None: return (-1000, -1000)
        return agentState.get_coord()

    #get action
    def getDirection(self, agentState):
        if agentState.configuration == None: return Directions.STOP
        return agentState.configuration.getDirection()

    def finish(self):
        end_graphics() #utility function for ending the display

    #converting the point coords to to_screen
    def to_screen(self, point):
        ( x, y ) = point
        x = (x + 1)*self.gridSize
        y = (self.height  - y)*self.gridSize
        return ( x, y )

    #drawing the walls from the wallMatrix
    def drawWalls(self, wallMatrix):
        wallColor = wall_color
        for xNum, x in enumerate(wallMatrix):
            for yNum, cell in enumerate(x):
                if cell: # There's a wall here
                    coord = (xNum, yNum)
                    screen = self.to_screen(coord)

                    # draw each quadrant of the square based on adjacent walls
                    wis_wall = self.is_wall(xNum-1, yNum, wallMatrix)
                    eis_wall = self.is_wall(xNum+1, yNum, wallMatrix)
                    nis_wall = self.is_wall(xNum, yNum+1, wallMatrix)
                    sis_wall = self.is_wall(xNum, yNum-1, wallMatrix)
                    nwis_wall = self.is_wall(xNum-1, yNum+1, wallMatrix)
                    swis_wall = self.is_wall(xNum-1, yNum-1, wallMatrix)
                    neis_wall = self.is_wall(xNum+1, yNum+1, wallMatrix)
                    seis_wall = self.is_wall(xNum+1, yNum-1, wallMatrix)

                    # NE quadrant
                    if (not nis_wall) and (not eis_wall):
                        # inner circle
                        circle(screen, WALL_RADIUS * self.gridSize, wallColor, wallColor, (0,91), 'arc')
                    if (nis_wall) and (not eis_wall):
                        # vertical line
                        line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5)-1)), wallColor)
                    if (not nis_wall) and (eis_wall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                    if (nis_wall) and (eis_wall) and (not neis_wall):
                        # outer circle
                        circle(add(screen, (self.gridSize*2*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (180,271), 'arc')
                        line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                        line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(-0.5))), wallColor)

                    # NW quadrant
                    if (not nis_wall) and (not wis_wall):
                        # inner circle
                        circle(screen, WALL_RADIUS * self.gridSize, wallColor, wallColor, (90,181), 'arc')
                    if (nis_wall) and (not wis_wall):
                        # vertical line
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5)-1)), wallColor)
                    if (not nis_wall) and (wis_wall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                    if (nis_wall) and (wis_wall) and (not nwis_wall):
                        # outer circle
                        circle(add(screen, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (270,361), 'arc')
                        line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(-1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(-1)*WALL_RADIUS)), wallColor)
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-2)*WALL_RADIUS+1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(-0.5))), wallColor)

                    # SE quadrant
                    if (not sis_wall) and (not eis_wall):
                        # inner circle
                        circle(screen, WALL_RADIUS * self.gridSize, wallColor, wallColor, (270,361), 'arc')
                    if (sis_wall) and (not eis_wall):
                        # vertical line
                        line(add(screen, (self.gridSize*WALL_RADIUS, 0)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5)+1)), wallColor)
                    if (not sis_wall) and (eis_wall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5+1, self.gridSize*(1)*WALL_RADIUS)), wallColor)
                    if (sis_wall) and (eis_wall) and (not seis_wall):
                        # outer circle
                        circle(add(screen, (self.gridSize*2*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (90,181), 'arc')
                        line(add(screen, (self.gridSize*2*WALL_RADIUS-1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*0.5, self.gridSize*(1)*WALL_RADIUS)), wallColor)
                        line(add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*WALL_RADIUS, self.gridSize*(0.5))), wallColor)

                    # SW quadrant
                    if (not sis_wall) and (not wis_wall):
                        # inner circle
                        circle(screen, WALL_RADIUS * self.gridSize, wallColor, wallColor, (180,271), 'arc')
                    if (sis_wall) and (not wis_wall):
                        # vertical line
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, 0)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5)+1)), wallColor)
                    if (not sis_wall) and (wis_wall):
                        # horizontal line
                        line(add(screen, (0, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5)-1, self.gridSize*(1)*WALL_RADIUS)), wallColor)
                    if (sis_wall) and (wis_wall) and (not swis_wall):
                        # outer circle
                        circle(add(screen, (self.gridSize*(-2)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS)), WALL_RADIUS * self.gridSize-1, wallColor, wallColor, (0,91), 'arc')
                        line(add(screen, (self.gridSize*(-2)*WALL_RADIUS+1, self.gridSize*(1)*WALL_RADIUS)), add(screen, (self.gridSize*(-0.5), self.gridSize*(1)*WALL_RADIUS)), wallColor)
                        line(add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(2)*WALL_RADIUS-1)), add(screen, (self.gridSize*(-1)*WALL_RADIUS, self.gridSize*(0.5))), wallColor)

    #checking if the coords given are of walls or not
    def is_wall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    #drawing the coin on the layout
    def drawcoin(self, coinMatrix ):
        coinImages = []
        color = coin_COLOR
        for xNum, x in enumerate(coinMatrix):
            imageRow = []
            coinImages.append(imageRow)
            for yNum, cell in enumerate(x):
                if cell: # There's coin here
                    screen = self.to_screen((xNum, yNum ))
                    dot = circle( screen,
                                  coin_SIZE * self.gridSize,
                                  outlineColor = color, fillColor = color,
                                  width = 1)
                    imageRow.append(dot)
                else:
                    imageRow.append(None)
        return coinImages

    #drawing bcoin on the layout
    def drawbig_coin(self, big_coin ):
        capsuleImages = {}
        for capsule in big_coin:
            ( screen_x, screen_y ) = self.to_screen(capsule)
            dot = circle( (screen_x, screen_y),
                              CAPSULE_SIZE * self.gridSize,
                              outlineColor = CAPSULE_COLOR,
                              fillColor = CAPSULE_COLOR,
                              width = 1)
            capsuleImages[capsule] = dot
        return capsuleImages

    #removing the coin from the layout
    def removecoin(self, cell, coinImages ):
        x, y = cell
        remove_from_screen(coinImages[x][y])

    #removing the bcoin from the layout
    def removeCapsule(self, cell, capsuleImages ):
        x, y = cell
        remove_from_screen(capsuleImages[(x, y)])

#Util function for adding the coords
def add(x, y):
    return (x[0] + y[0], x[1] + y[1])
