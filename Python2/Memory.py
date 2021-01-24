"""Implementation of card game - Memory."""

LINK = "http://www.codeskulptor.org/#user47_BTNU3MAkCI6X4Ua_6.py"

# importing libraries
import simplegui
import random

# defining global variables
TILE_WIDTH = 100
TILE_HEIGHT = 100
DISTINCT_TILES = 8

# function for starting a new game
def new_game():
    """ Initializes all global variables"""

    global tiles, state, turns
    tile_values = range(DISTINCT_TILES) * 2
    random.shuffle(tile_values)
    tiles = [Tile(tile_values[i * DISTINCT_TILES / 2  + j],
                  False, [i * TILE_WIDTH, j * TILE_HEIGHT])
             for i in range(DISTINCT_TILES / 2)
             for j in range(DISTINCT_TILES / 2)]
    state = 0
    turns = 0
    label.set_text("Turns = 0")

# creating a Tile class
class Tile:

    def __init__(self, val, exposed, loc):
        """ Creates a Tile object"""
        self.value = val
        self.exposed = exposed
        self.location = loc

    def __str__(self):
        s = "Tile's value is " + str(self.value) + "\n"
        s += "Tile's value is shown " + str(self.exposed)

    def get_value(self):
        """ Returns the value of a Tile"""
        return self.value

    def is_exposed(self):
        """ Shows whether or not a Tile is exposed"""
        return self.exposed

    def expose_tile(self):
        """ Exposed the value of a Tile """
        self.exposed = True

    def hide_tile(self):
        """ Hides the value of a Tile """
        self.exposed = False

    def is_selected(self, pos):
        """ Shows whether a Tile is selected with a mouse or not """
        loc = self.location
        is_width = loc[0] <= pos[0] <= loc[0] + TILE_WIDTH
        is_height = loc[1] <= pos[1] <= loc[1] + TILE_HEIGHT
        return is_width and is_height

    def draw_tile(self, canvas):
        """ Draws a Tile given its coordinates and value,
        taking into account whether it's exposed or not """

        loc = self.location
        if self.exposed:
            text_pos = [loc[0] + 0.32 * TILE_WIDTH,
                        loc[1] + 0.75 * TILE_HEIGHT]
            canvas.draw_text(str(self.value), text_pos,
                             TILE_WIDTH * 0.8, "White")
        else:
            tile_corners = [loc,
                            [loc[0], loc[1] + TILE_HEIGHT],
                            [loc[0] + TILE_WIDTH, loc[1] + TILE_HEIGHT],
                            [loc[0] + TILE_WIDTH, loc[1]]]
            canvas.draw_polygon(tile_corners, 5, "Red", "Green")


# mouseclick handler
def mouseclick(pos):
    """ Hides and exposes tiles according to the game's state"""

    global state, first_tile, second_tile, turns
    for tile in tiles:
        if tile.is_selected(pos):
            clicked_tile = tile

    if clicked_tile.is_exposed():
        return

    clicked_tile.expose_tile()

    if state == 0:
        first_tile = clicked_tile
        state = 1
    elif state == 1:
        second_tile = clicked_tile
        state = 2
        turns += 1
        label.set_text("Turns = " + str(turns))
    elif state == 2:
        if first_tile.get_value() != second_tile.get_value():
            first_tile.hide_tile()
            second_tile.hide_tile()

        first_tile = clicked_tile
        state = 1


# draw handler
def draw(canvas):
    for tile in tiles:
        tile.draw_tile(canvas)

# creating a frame and adding a button and labels
frame = simplegui.create_frame("Memory", (DISTINCT_TILES / 2) * TILE_WIDTH,
                               (DISTINCT_TILES / 2) * TILE_HEIGHT)
frame.add_button("Reset", new_game, 100)
label = frame.add_label("Turns = 0")

# registering event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# starting the game
new_game()
frame.start()
