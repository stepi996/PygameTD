import pygame # type: ignore
import objects

size = width, height = 900, 600
speed = [2, 2]
blue = 29, 134, 240
game_over = False
game_over_text = objects.Text.create("Game Over", (255, 0, 0))
retry = False

ROWS = 30
block_width = width / ROWS
LINES = 20
block_height = height / LINES
start_block = objects.Block.create(1, 0)

path_length = 50
blocks = []

fast_enemies = []
slow_enemies = []

alive = True

screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(blue)