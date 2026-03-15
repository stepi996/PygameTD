# Import pygame library and custom game objects
import pygame # type: ignore
from objects import *

# Screen dimensions: 900x600 pixels
size = width, height = 900, 600

# Movement speed for game entities (2 pixels per frame)
speed = [2, 2]

# Background color (RGB: blue)
blue = 29, 134, 240

# Game state variables
game_over = False
game_over_text = Text.create("Game Over", textColor=(255, 0, 0))
retry = False

# Tutorial state variable
first_time = True

# Grid system dimensions for the game map
ROWS = 20  # Number of columns in the grid
block_width = width / ROWS  # Width of each block
LINES = 15  # Number of rows in the grid
block_height = height / LINES  # Height of each block

# Starting position for the player/tower placement
start_block = Block.create(1, 0)

# Path-related constants
path_length = 50

# Game object collections
blocks = []  # List of block/tile objects on the map

# Tower defense game objects
towers = []  # List of active towers
projectiles = []  # List of projectiles shot by towers

# Enemy collections separated by type for different behaviors
fast_enemies = []  # Enemies that move quickly
slow_enemies = []  # Enemies that move slowly
camo_enemies = []  # Enemies that are harder to detect
enemies = []  # All enemies combined

# Gold rewards for defeating different enemy types
gold_gained_from_fast = 20 # Gold awarded for defeating a fast enemy
gold_gained_from_slow = 40 # Gold awarded for defeating a slow enemy
gold_gained_from_camo = 50 # Gold awarded for defeating a camo enemy

# Game state and progression variables
alive = True  # Whether the player is still alive
difficulty = 1  # Current difficulty level
wave = 1  # Current wave number
max_towers = wave + 1  # Maximum number of towers allowed, increases with each wave
current_towers = len(towers)  # Current number of towers built by the player
gold = 100  # Player's starting gold/resources
spawn_time = 3000  # Time interval (ms) between enemy spawns

# Pygame display and rendering setup
clock = pygame.time.Clock()  # Clock object for managing frame rate
screen = pygame.display.set_mode(size)  # Main game window
background = pygame.Surface(screen.get_size())  # Background surface
background = background.convert()  # Optimize background for faster blitting
background.fill(blue)  # Fill background with blue color
menu_screen = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # Transparent menu overlay
menu_screen = menu_screen.convert_alpha()  # Optimize alpha surface for blitting