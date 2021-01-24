"""Implementation of classic arcade game Pong."""

LINK = "http://www.codeskulptor.org/#user47_wLqZd5t19qaf2f3_8.py"

import simplegui
import random

# global variables
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
HALF_BALL_RADIUS = BALL_RADIUS / 2
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# paddle1_pos and paddle2_pos are distances from the top of the canvas
paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initializing ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# spawning a new ball
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4), - random.randrange(1, 3)]
    elif direction == LEFT:
        ball_vel = [- random.randrange(2, 4), - random.randrange(1, 3)]
    else:
        print "Something is wrong. Please, check your code"

# defining event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # drawing mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # drawing the motion of a ball
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:

        if (paddle1_pos - HALF_BALL_RADIUS < ball_pos[1]
            < paddle1_pos + PAD_HEIGHT + HALF_BALL_RADIUS):
            ball_vel[0] = - 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            spawn_ball(RIGHT)

    elif ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):

        if (paddle2_pos - HALF_BALL_RADIUS  < ball_pos[1]
            < paddle2_pos + PAD_HEIGHT + HALF_BALL_RADIUS):
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            spawn_ball(LEFT)

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # updating paddle's vertical position and drawing them
    if (paddle1_pos + paddle1_vel < 0) or (
        paddle1_pos + paddle1_vel > HEIGHT - PAD_HEIGHT):
        paddle1_pos = paddle1_pos
    elif 0 <= paddle1_pos <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel < 0) or (
        paddle2_pos + paddle2_vel > HEIGHT - PAD_HEIGHT):
        paddle2_pos = paddle2_pos
    elif 0 <= paddle2_pos <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    canvas.draw_line( [HALF_PAD_WIDTH / 2, paddle1_pos],
                      [HALF_PAD_WIDTH / 2, paddle1_pos + PAD_HEIGHT],
                      PAD_WIDTH, "White")
    canvas.draw_line( [WIDTH - HALF_PAD_WIDTH / 2, paddle2_pos],
                      [WIDTH - HALF_PAD_WIDTH / 2, paddle2_pos + PAD_HEIGHT],
                      PAD_WIDTH, "White")

    # drawing scores
    canvas.draw_text("Player1", (25, 25),
                     30, "Red")
    canvas.draw_text(str(score1), (270, 60),
                     48, "White")
    canvas.draw_text("Player2", (480, 25),
                     30, "Red")
    canvas.draw_text(str(score2), (310, 60),
                     48, "White")

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 4
    else:
        print "This key doesn't have an event handler"

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0

def restart():
    new_game()

# creating a frame and registering handlers
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 100)

# start frame
new_game()
frame.start()
