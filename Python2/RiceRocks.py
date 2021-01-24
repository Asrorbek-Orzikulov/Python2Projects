"""Code for the classic game RiceRocks."""

LINK = "http://www.codeskulptor.org/#user47_IwfLKFJEQs_21.py"

import simplegui
import math
import random

# ImageInfor class for getting the dimensions of an image
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris3_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([50, 50], [100, 100], 17, 81, animated = True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRAME_SIZE = [WIDTH, HEIGHT]
score = 0
lives = 3
time = 0
ANGULAR_VEL = 0.1
started = False
rock_group = set()
missile_group = set()
explosion_group = set()


# helper functions to handle transformations
def angle_to_vector(ang):
    """ Converts an angle to a vector """
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    """ Finds the distance between two points"""
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

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

def process_sprite_group(sprite_set, canvas):
    """ Draws and updates each object in the set """
    for sprite in set(sprite_set):
        if sprite.update():
            sprite_set.remove(sprite)
        else:
            sprite.draw(canvas)
            sprite.update()

def group_collide(group, other_object):
    """ Removes collided elements from the group """
    for member in set(group):
        if member.collide(other_object):
            group.remove(member)
            position = other_object.get_position()
            explosion = Sprite(position, [0, 0], 0, 0, explosion_image,
                               explosion_info, explosion_sound)
            explosion_group.add(explosion)
            return True

    return False

def group_group_collide(group1, group2):
    """ group_collide() function for two groups """
    count_true = 0
    for member in set(group1):
        if group_collide(group2, member):
            count_true += 1
            group1.remove(member)

    return count_true

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = list(pos)
        self.vel = list(vel)
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_position(self):
        """ Returns the center of an image """
        return self.pos

    def get_radius(self):
        """ Returns the radius of an image """
        return self.radius

    def start_thrust(self, sound):
        """ Turns the thrusters on """
        self.thrust = True
        sound.play()

    def stop_thrust(self, sound):
        """ Turns the thrusters off """
        self.thrust = False
        sound.rewind()

    def shoot(self):
        """ Shoots a Missile """
        global missile_group
        ship_tip_pos = add_vec(self.pos, scale_vec(self.forward_vec, self.radius))
        missile_vel = add_vec(self.vel, scale_vec(self.forward_vec, 5))
        a_missile = Sprite(ship_tip_pos, missile_vel, 0, 0,
                           missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def change_direction(self, key):
        """ Changes the direction the Ship is facing """
        direction = {"left" : - ANGULAR_VEL, "right" : ANGULAR_VEL, "stop" : 0}
        self.angle_vel = direction[key]

    def update(self):
        """ Updates the Ship's position and accelerates the
        Ship if the thrusters are on """
        self.pos = add_vec(self.pos, self.vel, wrap_frame = True)
        self.vel = scale_vec(self.vel, scale = 0.99)
        self.angle += self.angle_vel
        self.forward_vec = angle_to_vector(self.angle)
        if self.thrust:
            self.vel = add_vec(self.vel, scale_vec(self.forward_vec))

    def draw(self, canvas):
        """ Draws the Ship's image depending on whether or not
        the thrusters are on """
        if not self.thrust:
            image_center = self.image_center
        else:
            image_center = add_vec(self.image_center, [90, 0])

        canvas.draw_image(self.image, image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = list(pos)
        self.vel = list(vel)
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_position(self):
        """ Returns the center of an image """
        return self.pos

    def get_radius(self):
        """ Returns the radius of an image """
        return self.radius

    def update(self):
        """ Changes the position and rotation angle
        of the Sprite object"""
        self.angle += self.angle_vel
        self.pos = add_vec(self.pos, self.vel, wrap_frame = True)
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True

    def collide(self, other_object):
        """ Determines whether the Object
        collides with another object """
        pos1 = self.pos
        radius1 = self.radius
        pos2 = other_object.get_position()
        radius2 = other_object.get_radius()
        if dist(pos1, pos2) <= radius1 + radius2:
            return True
        else:
            return False

    def draw(self, canvas):
        """ Draws the Sprite object created """
        if self.animated:
            explosion_dim = [9, 9]
            explosion_index = [self.age % explosion_dim[0], (self.age // explosion_dim[0]) % explosion_dim[1]]
            canvas.draw_image(explosion_image,
                              [self.image_center[0] + explosion_index[0] * self.image_size[0],
                              self.image_center[1] + explosion_index[1] * self.image_size[1]],
                              self.image_size, self.pos, self.image_size)
            self.age += 1


        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

# keydown and keyup handlers
def keydown(key):
    global my_ship

    if key == simplegui.KEY_MAP["left"] :
        my_ship.change_direction("left")
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.change_direction("right")
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.start_thrust(ship_thrust_sound)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    global my_ship
    if (key == simplegui.KEY_MAP["left"]) or (key == simplegui.KEY_MAP["right"]):
        my_ship.change_direction("stop")
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.stop_thrust(ship_thrust_sound)

# draw handler
def draw(canvas):
    global rock_group, missile_group, explosion_group
    global lives, score, time, started

    # animiating the background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # drawing and updating the Ship
    my_ship.draw(canvas)
    my_ship.update()

    # drawing and updating the Sprites
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # decreasing lives if a Rock hits the Ship
    if group_collide(rock_group, my_ship):
        lives -= 1

    # increasing score if a Missile hits a Rock
    score += 10* group_group_collide(rock_group, missile_group)

    # displaying the score and lives
    canvas.draw_text("Lives: " + str(lives), [50,60], 30, "White")
    canvas.draw_text("Score: " + str(score), [640,60], 30, "White")

    # ending the game
    if lives == 0:
        started = False
        rock_group = set()
        soundtrack.rewind()

    # drawing the splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

# mouseclick handler (Splash)
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    # starting/restarting the game
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        soundtrack.play()

# timer handler that spawns a rock
def rock_spawner():
    """ Creates a Rock object with a random position,
    velocity and rotation speed """
    global rock_group

    # stopping the Rock spawner when the game is over
    if not started:
        return

    # spawning a new Rock
    a_rock = Sprite([random.randrange(WIDTH), random.randrange(HEIGHT)],
                    [random.randrange(-19, 20) / 30.0, random.randrange(-19, 20) / 30.0],
                    0, random.randrange(-8, 9) / 100.0, asteroid_image, asteroid_info)

    # preventing Rocks from appearing on top of the Ship
    if a_rock.collide(my_ship):
        return

    # limiting the number of Rocks
    elif len(rock_group) >= 10:
        rock_group.pop()

    # adding the Rock to the set
    rock_group.add(a_rock)

# initializing a frame and timer
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
timer = simplegui.create_timer(1000.0, rock_spawner)

# initializing the Ship and two Sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], - math.pi / 2, ship_image, ship_info)

# registering the handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

# starting the frame and timer
timer.start()
frame.start()
