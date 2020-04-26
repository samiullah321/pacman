from graphicsUtils import *
import math, time
from game import Directions

#Settings for the display
grdi_size = 30.0
info_height = 35
background_c= format_color(0,0,0)
wall_c = format_color(64/255.0, 224/255.0, 208/255.0)
score_c = format_color(.9, .9, .9)
pac_outline = 2

#Settings for Ghost
ghost_c = []
ghost_c.append(format_color(.9,0,0)) # Red
ghost_c.append(format_color(0,.3,.9)) # Blue
ghost_c.append(format_color(.98,.41,.07)) # Orange
ghost_c.append(format_color(.1,.75,.7)) # Green
ghost_c.append(format_color(1.0,0.6,0.0)) # Yellow
ghost_c.append(format_color(.4,0.13,0.91)) # Purple


#defines the dimensions of the ghost
ghost_dimensions = [
    (0, 1),
    (1, 0),
    (0, - 1),
    (-1, 0),
  ]
ghost_s = 0.65
scare_c = format_color(1,1,1)


#Some attributes of Pacman
pac_c = format_color(255.0/255.0,255.0/255.0,61.0/255)
pac_s = 0.5
#pacman_speed = 0.25

#coin config
coin_c = format_color(0.81,0.7,0.22)
coin_s = 0.1

#bcoin config
big_coin_c = format_color(0.9,0,0)
big_coin_s = 0.20

#wall config
wall_r = 0.05

class info_p:
    def __init__(self, layout, grid_size):
        #Starting pane attributes
        self.grid_size = grid_size
        self.width = (layout.width) * grid_size
        self.base = (layout.height + 1) * grid_size
        self.height = info_height
        self.font_size = 24
        self.text_c = pac_c
        self.draw_pane()

    def to_screen(self, coord, y = None): #Maps the positions from layout onto the screen
        if y == None:
            x,y = coord
        else:
            x = coord

        x = self.grid_size + x # Margin
        y = self.base + y
        return x,y

    def draw_pane(self):
        self.score_text = text( self.to_screen(0, 0  ), self.text_c, "SCORE:    0", "Times", self.font_size, "bold")

    def initialize_ghost_dis(self, distances): #initializing ghost onto the screen
        self.ghost_distance_text = []

        size = 20
        if self.width < 240:
            size = 12
        if self.width < 160:
            size = 10

        for i, d in enumerate(distances):
            t = text( self.to_screen(self.width/2 + self.width/8 * i, 0), ghost_c[i+1], d, "Times", size, "bold")
            self.ghost_distance_text.append(t)

    def update_score(self, score):
        change_text(self.score_text, "SCORE: % 4d" % score)

    def update_ghost_distances(self, distances):
        if len(distances) == 0: return
        if 'ghost_distance_text' not in dir(self): self.initialize_ghost_dis(distances)
        else:
            for i, d in enumerate(distances):
                change_text(self.ghost_distance_text[i], d)

class pac_graphic: #general graphics for pacman
    def __init__(self, frame_t=0.0):
        self.have_window = 0
        self.grid_size = grdi_size
        self.frame_t = frame_t

    def initialize(self, state, isBlue = False):
        self.isBlue = isBlue
        self.start_graphic(state)
        self.distributionImages = None  # Initialized lazily
        self.make_static_obj(state)
        self.make_agent_obj(state)

        # Information
        self.previousState = state

    def start_graphic(self, state): #initializing the graphics onto the screen
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.info_p = info_p(layout, self.grid_size)
        self.c_state = layout


    #drawing coin and bcoin onto the screen
    def make_static_obj(self, state):
        layout = self.layout
        self.make_wall(layout.walls)
        self.coin = self.make_coin(layout.coin)
        self.big_coin = self.make_big_coin(layout.big_coin)
        refresh()

    #drawing the pacman, ghost onto the screen
    def make_agent_obj(self, state):
        self.agent_img = [] # (agentState, image)
        for index, agent in enumerate(state.agent_states):
            if agent.is_pac:
                image = self.make_pac(agent, index)
                self.agent_img.append( (agent, image) )
            else:
                image = self.make_ghost(agent, index)
                self.agent_img.append( (agent, image) )
        refresh()

    #updates c_state to the newState recieved
    def update(self, newState):
        #updating the agent moved
        agent_index = newState.agent_moved
        agentState = newState.agent_states[agent_index]

        prevState, prevImage = self.agent_img[agent_index]
        if agentState.is_pac:
            self.animate_pacman_movement(agentState, prevState, prevImage) #moving pacman
        else:
            self.moveGhost(agentState, agent_index, prevState, prevImage) #animating or moving the ghost
        self.agent_img[agent_index] = (agentState, prevImage)

        if newState.coin_eaten != None:
            self.removecoin(newState.coin_eaten, self.coin) #if the coin is eaten, remove it from its position in new state
        if newState.big_food_Eaten != None:
            self.removeCapsule(newState.big_food_Eaten, self.big_coin) #same as coin
        self.info_p.update_score(newState.score)
        if 'ghostDistances' in dir(newState):
            self.info_p.update_ghost_distances(newState.ghostDistances) #updating the ghost distances here

    def make_window(self, width, height): #initializing the screen
        grid_width = (width-1) * self.grid_size
        grid_height = (height-1) * self.grid_size
        screen_width = 2*self.grid_size + grid_width
        screen_height = 2*self.grid_size + grid_height + info_height

        #starting the screen
        begin_graphics(screen_width,
                       screen_height,
                       background_c,
                       "PACMAN MULTI-AGENT SIMULATION")

    #drawing the pacman
    def make_pac(self, pacman, index):
        position = self.get_coord(pacman)
        screen_point = self.to_screen(position)
        endpoints = self.getEndpoints(self.getDirection(pacman))

        width = pac_outline
        outlineColor = pac_c
        fillColor = pac_c

        return [circle(screen_point, pac_s * self.grid_size,
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
        r = pac_s * self.grid_size
        moveCircle(image[0], screen_coord, r, endpoints)
        refresh()

    #animation of pacman when moving from cell to cell
    def animate_pacman_movement(self, pacman, prevPacman, image):
        if self.frame_t < 0:
            print('Press any key to step forward, "q" to play')
            keys = wait_for_keys()
            if 'q' in keys:
                self.frame_t = 0.1
        if self.frame_t > 0.01 or self.frame_t < 0:
            start = time.time()
            fx, fy = self.get_coord(pacman)
            px, py = self.get_coord(pacman)
            frames = 4.0
            for i in range(1,int(frames) + 1):
                coord = px*i/frames + fx*(frames-i)/frames, py*i/frames + fy*(frames-i)/frames
                self.move_pacman(coord, self.getDirection(pacman), image)
                refresh()
                sleep(abs(self.frame_t) / frames)
        else:
            self.move_pacman(self.get_coord(pacman), self.getDirection(pacman), image)
        refresh()

    #retreiving the ghost color
    def get_ghost_color(self, ghost, ghostIndex):
        if ghost.scared_timer > 0:
            return scare_c
        else:
            return ghost_c[ghostIndex]

    #drawing the ghost
    def make_ghost(self, ghost, agent_index):
        coord = self.get_coord(ghost)
        dir = self.getDirection(ghost)
        (screen_x, screen_y) = (self.to_screen(coord) )
        coords = []
        for (x, y) in ghost_dimensions:
            coords.append((x*self.grid_size*ghost_s + screen_x, y*self.grid_size*ghost_s + screen_y))

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
            color = scare_c #setting the color of scared state
        else:
            color = ghost_c[ghostIndex]
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
        x = (x + 1)*self.grid_size
        y = (self.height  - y)*self.grid_size
        return ( x, y )

    #drawing the walls from the wallMatrix
    def make_wall(self, wallMatrix):
        wallColor = wall_c
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
                        circle(screen, wall_r * self.grid_size, wallColor, wallColor, (0,91), 'arc')
                    if (nis_wall) and (not eis_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*wall_r, 0)), add(screen, (self.grid_size*wall_r, self.grid_size*(-0.5)-1)), wallColor)
                    if (not nis_wall) and (eis_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(-1)*wall_r)), add(screen, (self.grid_size*0.5+1, self.grid_size*(-1)*wall_r)), wallColor)
                    if (nis_wall) and (eis_wall) and (not neis_wall):
                        # outer circle
                        circle(add(screen, (self.grid_size*2*wall_r, self.grid_size*(-2)*wall_r)), wall_r * self.grid_size-1, wallColor, wallColor, (180,271), 'arc')
                        line(add(screen, (self.grid_size*2*wall_r-1, self.grid_size*(-1)*wall_r)), add(screen, (self.grid_size*0.5+1, self.grid_size*(-1)*wall_r)), wallColor)
                        line(add(screen, (self.grid_size*wall_r, self.grid_size*(-2)*wall_r+1)), add(screen, (self.grid_size*wall_r, self.grid_size*(-0.5))), wallColor)

                    # NW quadrant
                    if (not nis_wall) and (not wis_wall):
                        # inner circle
                        circle(screen, wall_r * self.grid_size, wallColor, wallColor, (90,181), 'arc')
                    if (nis_wall) and (not wis_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*(-1)*wall_r, 0)), add(screen, (self.grid_size*(-1)*wall_r, self.grid_size*(-0.5)-1)), wallColor)
                    if (not nis_wall) and (wis_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(-1)*wall_r)), add(screen, (self.grid_size*(-0.5)-1, self.grid_size*(-1)*wall_r)), wallColor)
                    if (nis_wall) and (wis_wall) and (not nwis_wall):
                        # outer circle
                        circle(add(screen, (self.grid_size*(-2)*wall_r, self.grid_size*(-2)*wall_r)), wall_r * self.grid_size-1, wallColor, wallColor, (270,361), 'arc')
                        line(add(screen, (self.grid_size*(-2)*wall_r+1, self.grid_size*(-1)*wall_r)), add(screen, (self.grid_size*(-0.5), self.grid_size*(-1)*wall_r)), wallColor)
                        line(add(screen, (self.grid_size*(-1)*wall_r, self.grid_size*(-2)*wall_r+1)), add(screen, (self.grid_size*(-1)*wall_r, self.grid_size*(-0.5))), wallColor)

                    # SE quadrant
                    if (not sis_wall) and (not eis_wall):
                        # inner circle
                        circle(screen, wall_r * self.grid_size, wallColor, wallColor, (270,361), 'arc')
                    if (sis_wall) and (not eis_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*wall_r, 0)), add(screen, (self.grid_size*wall_r, self.grid_size*(0.5)+1)), wallColor)
                    if (not sis_wall) and (eis_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(1)*wall_r)), add(screen, (self.grid_size*0.5+1, self.grid_size*(1)*wall_r)), wallColor)
                    if (sis_wall) and (eis_wall) and (not seis_wall):
                        # outer circle
                        circle(add(screen, (self.grid_size*2*wall_r, self.grid_size*(2)*wall_r)), wall_r * self.grid_size-1, wallColor, wallColor, (90,181), 'arc')
                        line(add(screen, (self.grid_size*2*wall_r-1, self.grid_size*(1)*wall_r)), add(screen, (self.grid_size*0.5, self.grid_size*(1)*wall_r)), wallColor)
                        line(add(screen, (self.grid_size*wall_r, self.grid_size*(2)*wall_r-1)), add(screen, (self.grid_size*wall_r, self.grid_size*(0.5))), wallColor)

                    # SW quadrant
                    if (not sis_wall) and (not wis_wall):
                        # inner circle
                        circle(screen, wall_r * self.grid_size, wallColor, wallColor, (180,271), 'arc')
                    if (sis_wall) and (not wis_wall):
                        # vertical line
                        line(add(screen, (self.grid_size*(-1)*wall_r, 0)), add(screen, (self.grid_size*(-1)*wall_r, self.grid_size*(0.5)+1)), wallColor)
                    if (not sis_wall) and (wis_wall):
                        # horizontal line
                        line(add(screen, (0, self.grid_size*(1)*wall_r)), add(screen, (self.grid_size*(-0.5)-1, self.grid_size*(1)*wall_r)), wallColor)
                    if (sis_wall) and (wis_wall) and (not swis_wall):
                        # outer circle
                        circle(add(screen, (self.grid_size*(-2)*wall_r, self.grid_size*(2)*wall_r)), wall_r * self.grid_size-1, wallColor, wallColor, (0,91), 'arc')
                        line(add(screen, (self.grid_size*(-2)*wall_r+1, self.grid_size*(1)*wall_r)), add(screen, (self.grid_size*(-0.5), self.grid_size*(1)*wall_r)), wallColor)
                        line(add(screen, (self.grid_size*(-1)*wall_r, self.grid_size*(2)*wall_r-1)), add(screen, (self.grid_size*(-1)*wall_r, self.grid_size*(0.5))), wallColor)

    #checking if the coords given are of walls or not
    def is_wall(self, x, y, walls):
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    #drawing the coin on the layout
    def make_coin(self, coinMatrix ):
        coinImages = []
        color = coin_c
        for xNum, x in enumerate(coinMatrix):
            imageRow = []
            coinImages.append(imageRow)
            for yNum, cell in enumerate(x):
                if cell: # There's coin here
                    screen = self.to_screen((xNum, yNum ))
                    dot = circle( screen,
                                  coin_s * self.grid_size,
                                  outlineColor = color, fillColor = color,
                                  width = 1)
                    imageRow.append(dot)
                else:
                    imageRow.append(None)
        return coinImages

    #drawing bcoin on the layout
    def make_big_coin(self, big_coin ):
        capsuleImages = {}
        for capsule in big_coin:
            ( screen_x, screen_y ) = self.to_screen(capsule)
            dot = circle( (screen_x, screen_y),
                              big_coin_s * self.grid_size,
                              outlineColor = big_coin_c,
                              fillColor = big_coin_c,
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
