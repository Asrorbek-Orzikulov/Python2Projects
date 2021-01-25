"""Implementation of classic arcade game Pong."""

LINK = "http://www.codeskulptor.org/#user47_2HxT8SEaWe_8.py"

import simplegui
import random

# Constants
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_LENGTH = 80
PAD_VEL = 4

# helper functions
def add_vec(first_vector, second_vector, dimensions = 2, wrap_frame = False):
    """ Adds the second vector to the first vector. If
    wrap_frame is True, uses the modular arithmetic """
    sum_vector = []
    for d in range(dimensions):
        if wrap_frame:
            sum_vector.append((first_vector[d] + second_vector[d]) % FRAME_SIZE[d])
        else:
            sum_vector.append(first_vector[d] + second_vector[d])
    return sum_vector

def scale_vec(vec, scale = 0.1, dimensions = 2):
    """ Performs a scalar multiplication of a vector """
    scaled_vector = []
    for d in range(dimensions):
            scaled_vector.append(vec[d] * scale)
    return scaled_vector

def process_group(object_lst, canvas):
    """ Draws and updates the position of each object in the list """
    for object in object_lst:
        object.draw(canvas)
        object.update()

# classes
class Ball:
    """ Creates a ball object """

    def __init__(self, pos, vel, radius):
        self.pos = list(pos)
        self.vel = list(vel)
        self.radius = radius

    def __str__(self):
        s = "Ball pos " + str(self.pos)
        s += ". Ball vel " + str(self.vel)
        return s

    def get_position(self):
        """ Returns the position of the ball """
        return self.pos

    def get_radius(self):
        """ Returns the radius of the ball """
        return self.radius

    def reflect(self, direction):
        """ Reflects the ball horizontally """
        if direction == "horizontal":
            self.vel[0] = - self.vel[0]
        elif direction == "vertical":
            self.vel[1] = - self.vel[1]

    def accelerate(self):
        """ Accelerates the ball """
        self.vel = scale_vec(self.vel, scale = 1.1)

    def update(self):
        """ Moves the ball using its velocity """
        self.pos = add_vec(self.pos, self.vel)

    def draw(self, canvas):
        """ Draws the ball """
        canvas.draw_circle(self.pos, self.radius, 1,
                           "White", "White")

class Paddle:
    """ Creates a new paddle, where pos is the
    top-left corner """

    def __init__(self, pos, width, length):
        self.pos = pos
        self.width = width
        self.length = length
        self.vel = [0, 0]

    def __str__(self):
        s = "Paddle pos " + str(self.pos)
        s += ". Paddle vel " + str(self.vel)
        return s

    def is_collide(self, pos, radius):
        """ Returns True if a ball collides with the
        paddle, allowing the ball center to be within
        half ball radius from the edges of the paddle"""
        paddle_top = self.pos[1]
        paddle_bottom = self.pos[1] + self.length
        if paddle_top - radius / 2 < pos[1] < paddle_bottom + radius / 2:
            return True
        else:
            return False

    def update(self):
        """ Moves the paddle along the gutters """
        if 0 <= add_vec(self.pos, self.vel)[1] <= HEIGHT - PAD_LENGTH:
            self.pos = add_vec(self.pos, self.vel)

    def set_vel(self, vertical_vel):
        """ Sets the velocity of the paddle """
        self.vel[1] = vertical_vel

    def draw(self, canvas):
        """ Draws the paddle """
        corners = [self.pos,
                   [self.pos[0] + self.width, self.pos[1]],
                   [self.pos[0] + self.width, self.pos[1] + self.length],
                   [self.pos[0], self.pos[1] + self.length]]
        canvas.draw_polygon(corners, 1, "White", "White")

class GameState:
    """ Encapsulates all global variables and objects """
    def __init__(self):
        self.score_1 = 0
        self.score_2 = 0
        self.spawn_ball(random.choice(["Right", "Left"]))
        self.create_paddles()

    def get_score(self, num):
        """ Gets the score_1 or score_2 """
        if num == 1:
            return str(self.score_1)
        elif num == 2:
            return str(self.score_2)

    def increment_score(self, num):
        """ Increments the score_1 or score_2 """
        if num == 1:
            self.score_1 += 1
        elif num == 2:
            self.score_2 += 1

    def spawn_ball(self, direction):
        """ Spawns a new ball """
        global ball
        x_vel = random.randrange(2, 4)
        y_vel = random.choice([-1, 1]) * random.randrange(1, 3)
        if direction == "Left":
            x_vel = - x_vel

        ball = Ball([WIDTH / 2, HEIGHT / 2],
                    [x_vel, y_vel ],
                    BALL_RADIUS)

    def create_paddles(self):
        """ Creates two paddles """
        global paddle_1, paddle_2
        paddle_1 = Paddle([0, HEIGHT / 2 - PAD_LENGTH / 2],
                          PAD_WIDTH, PAD_LENGTH)
        paddle_2 = Paddle([WIDTH - PAD_WIDTH, HEIGHT / 2 - PAD_LENGTH / 2],
                          PAD_WIDTH, PAD_LENGTH)

# event handlers
def keydown(key):
    """ Keydown handler """
    for move in move_dict:
        if key == simplegui.KEY_MAP[move]:
            move_dict[move][0].set_vel(move_dict[move][1])

def keyup(key):
    """ Keyup handler """
    for move in move_dict:
        if key == simplegui.KEY_MAP[move]:
            move_dict[move][0].set_vel(0)

def draw(canvas):
    """ Draws the ball, paddles, and field """
    # reflecting the ball
    ball_pos = ball.get_position()
    ball_radius = ball.get_radius()

    if (ball_pos[1] <= 0 + ball_radius) or (
        ball_pos[1] >= HEIGHT - ball_radius):
        ball.reflect("vertical")

    elif ball_pos[0] <= 0 + ball_radius + PAD_WIDTH:
        if paddle_1.is_collide(ball_pos, ball_radius):
            ball.reflect("horizontal")
            ball.accelerate()
        else:
            game.increment_score(2)
            game.spawn_ball("Right")

    elif ball_pos[0] >= WIDTH - ball_radius - PAD_WIDTH:
        if paddle_2.is_collide(ball_pos, ball_radius):
            ball.reflect("horizontal")
            ball.accelerate()
        else:
            game.increment_score(1)
            game.spawn_ball("Left")

    # drawing and updating ball and paddles
    process_group([ball, paddle_1, paddle_2], canvas)

    # drawing mid line, gutters and scores
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_text("Player 1: " + game.get_score(1), (25, 25), 36, "White")
    canvas.draw_text("Player 2: " + game.get_score(2), (400, 25), 36, "White")

# starting the game
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
game = GameState()
move_dict = {"w" : [paddle_1, - PAD_VEL],
             "s" : [paddle_1, PAD_VEL],
             "up" : [paddle_2, - PAD_VEL],
             "down" : [paddle_2, PAD_VEL]}
frame.start()
