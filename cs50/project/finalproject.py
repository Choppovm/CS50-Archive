# This was made outside CS50 codespace, using the VSCODE app.
# You will need to copy the code and paste it into an app.
# Furthermore, ensure you install the following modules: pyglet, random, math

'''
INSTRUCTIONS:
Use WASD keys to move
Touch green balls - larger it is, the more score you get.
Avoid red balls - 1 spawns every 10 seconds, and they speed up every 30 seconds. The larger it is, the more points you lose.
Getting a score below zero ends the game.
'''

import pyglet
from pyglet.window import key
import random
import math

# Window size
WIDTH, HEIGHT = 800, 600

# Square (player) settings
SQUARE_SIZE = 40
MOVEMENT_SPEED = 600  # Speed of the player when a key is pressed
FRICTION = 0.95  # Friction to slow down movement over time
PLAYER_COLOR = (0, 255, 255)  # Cyan Blue

# Circle (food) settings
CIRCLE_MIN_SIZE = 10 # How small the radius can be
CIRCLE_MAX_SIZE = 30 # how large the radius can be
NEW_CIRCLE_DELAY = 1.0  # Time delay before generating a new circle after one is eaten

# Red (hazard) circle settings
INITIAL_RED_CIRCLES = 1 # How many hazards/red circles spawn when the game first starts
RED_CIRCLE_SPEED = 100  # Initial speed at which red circles move towards the player
RED_CIRCLE_SPEED_INCREASE_INTERVAL = 30.0  # Time interval to increase speed
RED_CIRCLE_SPAWN_INTERVAL = 5  # Time interval to spawn new red circles (for example, a new red circle wil spawn every 5 seconds)

# Colors
GREEN_COLOR = (50, 225, 50)
RED_COLOR = (225, 50, 50)
PURPLE_COLOR = (128, 0, 128)  # Purple particles
YELLOW_COLOR = (255, 255, 0)  # Yellow particles

# Particle settings
PARTICLE_LIFETIME_YELLOW = 1  # Duration of yellow particles
PARTICLE_COUNT_YELLOW = 25  # Number of yellow particles from green circles
PARTICLE_SPEED_YELLOW = 500  # Speed of yellow particles

PARTICLE_LIFETIME_PURPLE = 0.5  # Duration of purple particles
PARTICLE_COUNT_PURPLE = 25  # Number of purple particles from red circles
PARTICLE_SPEED_PURPLE = 250  # Speed of purple particles

# Initialize window
window = pyglet.window.Window(WIDTH, HEIGHT)
batch = pyglet.graphics.Batch()

# Score label
score = 0
score_label = pyglet.text.Label(
    f"Score: {score}",
    font_name="Arial",
    font_size=18,
    x=WIDTH // 2,
    y=20,
    anchor_x="center",
    anchor_y="center",
    batch=batch
)

# Player square
class Square:
    def __init__(self, x, y):
        self.size = SQUARE_SIZE
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.sprite = pyglet.shapes.Rectangle(self.x, self.y, self.size, self.size, color=PLAYER_COLOR, batch=batch)

    def update(self, dt):
        # Apply friction
        self.dx *= FRICTION
        self.dy *= FRICTION

        # Update position
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Prevent the square from going off the screen
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

        self.sprite.x = self.x
        self.sprite.y = self.y

# Base Circle class (food or hazard)
class Circle:
    def __init__(self, radius, x, y, color):
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color
        self.sprite = pyglet.shapes.Circle(self.x, self.y, self.radius, color=self.color, batch=batch)

    def check_collision(self, square):
        dist = math.sqrt((square.x + square.size / 2 - self.x) ** 2 + (square.y + square.size / 2 - self.y) ** 2)
        return dist < square.size / 2 + self.radius

    def update_position(self, player_x, player_y, dt):
        """Update position to move towards the player."""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * RED_CIRCLE_SPEED * dt
            self.y += dy * RED_CIRCLE_SPEED * dt
            self.sprite.x = self.x
            self.sprite.y = self.y

# Green circle (food)
class GreenCircle(Circle):
    def __init__(self):
        radius = random.randint(CIRCLE_MIN_SIZE, CIRCLE_MAX_SIZE)
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)
        super().__init__(radius, x, y, GREEN_COLOR)

    def award_points(self):
        return self.radius  # Score based on the radius of the circle

# Red circle (hazard)
class RedCircle(Circle):
    def __init__(self):
        radius = random.randint(CIRCLE_MIN_SIZE, CIRCLE_MAX_SIZE)
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)
        super().__init__(radius, x, y, RED_COLOR)

# Particle class for yellow particles
class YellowParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = PARTICLE_LIFETIME_YELLOW
        self.alpha = 255  # Full opacity
        self.dx = random.uniform(-1, 1) * PARTICLE_SPEED_YELLOW
        self.dy = random.uniform(-1, 1) * PARTICLE_SPEED_YELLOW
        self.sprite = pyglet.shapes.Circle(self.x, self.y, 5, color=YELLOW_COLOR)  # Yellow particles

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.lifetime -= dt
        self.alpha = max(0, self.alpha - (255 / PARTICLE_LIFETIME_YELLOW) * dt)  # Fade out
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.color = (YELLOW_COLOR[0], YELLOW_COLOR[1], YELLOW_COLOR[2], int(self.alpha))  # Update color with alpha

    def is_alive(self):
        return self.lifetime > 0

# Particle class for purple particles
class PurpleParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = PARTICLE_LIFETIME_PURPLE
        self.alpha = 255  # Full opacity
        self.dx = random.uniform(-1, 1) * PARTICLE_SPEED_PURPLE
        self.dy = random.uniform(-1, 1) * PARTICLE_SPEED_PURPLE
        self.sprite = pyglet.shapes.Circle(self.x, self.y, 5, color=PURPLE_COLOR)  # Purple particles

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.lifetime -= dt
        self.alpha = max(0, self.alpha - (255 / PARTICLE_LIFETIME_PURPLE) * dt)  # Fade out
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.color = (PURPLE_COLOR[0], PURPLE_COLOR[1], PURPLE_COLOR[2], int(self.alpha))  # Update color with alpha

    def is_alive(self):
        return self.lifetime > 0

# Initialize the player
player = Square(WIDTH // 2, HEIGHT // 2)
circles = []  # Green circles (food)
hazards = []  # Red circles (hazards)
yellow_particles = []  # Yellow particle effects
purple_particles = []  # Purple particle effects

# Key states
key_handler = key.KeyStateHandler()

# Variables to manage red circle spawning and speed increase
time_since_last_red_circle = 0
time_since_last_speed_increase = 0

# Function to generate a new green circle
def generate_green_circle():
    circle = GreenCircle()
    circles.append(circle)

# Function to generate a new red circle (hazard)
def generate_red_circle():
    hazard = RedCircle()
    hazards.append(hazard)

# Function to generate yellow particles
def generate_yellow_particles(x, y):
    for _ in range(PARTICLE_COUNT_YELLOW):
        yellow_particles.append(YellowParticle(x, y))

# Function to generate purple particles
def generate_purple_particles(x, y):
    for _ in range(PARTICLE_COUNT_PURPLE):
        purple_particles.append(PurpleParticle(x, y))

def update(dt):
    global score, time_since_last_red_circle, time_since_last_speed_increase

    # Move the player using WASD keys
    if key_handler[key.W]:
        player.dy += MOVEMENT_SPEED * dt
    if key_handler[key.S]:
        player.dy -= MOVEMENT_SPEED * dt
    if key_handler[key.A]:
        player.dx -= MOVEMENT_SPEED * dt
    if key_handler[key.D]:
        player.dx += MOVEMENT_SPEED * dt

    player.update(dt)

    # Update yellow particles
    for particle in yellow_particles[:]:
        particle.update(dt)
        if not particle.is_alive():
            yellow_particles.remove(particle)

    # Update purple particles
    for particle in purple_particles[:]:
        particle.update(dt)
        if not particle.is_alive():
            purple_particles.remove(particle)

    # Update red circles' positions
    for hazard in hazards:
        hazard.update_position(player.x + player.size / 2, player.y + player.size / 2, dt)

    # Check for collisions with green circles (food)
    for circle in circles[:]:
        if circle.check_collision(player):
            score += circle.award_points()  # Add points based on the size of the circle
            score_label.text = f"Score: {score}"
            circles.remove(circle)
            pyglet.clock.schedule_once(lambda dt: generate_green_circle(), NEW_CIRCLE_DELAY)  # Generate a new green circle after a delay
            generate_yellow_particles(circle.x, circle.y)  # Generate yellow particles when a green circle is eaten

    # Check for collisions with red circles (hazards)
    for hazard in hazards[:]:
        if hazard.check_collision(player):
            score -= hazard.radius
            if score < 0:
                pyglet.app.exit()
            score_label.text = f"Score: {score}"
            hazards.remove(hazard)
            generate_purple_particles(player.x + player.size / 2, player.y + player.size / 2)  # Generate purple particles when hit
            pyglet.clock.schedule_once(lambda dt: generate_red_circle(), NEW_CIRCLE_DELAY)  # Generate a new red circle immediately

    # Manage red circle spawning
    time_since_last_red_circle += dt
    if time_since_last_red_circle >= RED_CIRCLE_SPAWN_INTERVAL:
        generate_red_circle()
        time_since_last_red_circle = 0

    # Manage red circle speed increase
    time_since_last_speed_increase += dt
    if time_since_last_speed_increase >= RED_CIRCLE_SPEED_INCREASE_INTERVAL:
        global RED_CIRCLE_SPEED
        time_since_last_speed_increase = 0

@window.event
def on_draw():
    window.clear()
    batch.draw()

    # Draw yellow particles
    for particle in yellow_particles:
        particle.sprite.draw()

    # Draw purple particles
    for particle in purple_particles:
        particle.sprite.draw()

# Generate initial set of circles (green)
for _ in range(10): # spawns 10 green circles
    generate_green_circle()

# Generate initial red circle
for _ in range(1): # starts round with 1 red circle
    generate_red_circle()

# Update game every frame
pyglet.clock.schedule_interval(update, 1/60.0)

# Add the key handler to the window
window.push_handlers(key_handler)

# Run the Pyglet app
pyglet.app.run()
