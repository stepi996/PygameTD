# path.py handles procedural generation of the enemy path on the grid

import pygame # type: ignore
import random

# local modules that define constants and Block/Tower classes
import constants
import objects

# must initialize pygame for drawing operations used during generation
pygame.init()

def check_if_in_blocks(blocks, cur_block):
    """Return True if a block with the same coordinates exists in `blocks`.

    Used during path generation to avoid revisiting the same tile.
    """

    for block in blocks:
        if block.x == cur_block.x and block.y == cur_block.y:
            return True
    return False

def draw_path(blocks, x=1, y=0):
    """Generate a random non‑branching path of fixed length.

    The path begins at the coordinates `(x, y)` (default 1,0) and extends
    one block at a time in a random direction, avoiding boundaries and
    self‑intersection.  The `blocks` list is mutated in place.

    Returns ``(True, end_block)`` on success or ``(False, 0)`` if the
    generator gets stuck and gives up after too many failed attempts.
    """

    # draw the start tile in green and add it to our block list
    pygame.draw.rect(constants.background, (0, 255, 0),
                     (x*constants.block_width, y*constants.block_height,
                      constants.block_width, constants.block_height))
    blocks.append(constants.start_block)
    i = 0              # how many path blocks have been placed
    stuck = 0          # consecutive invalid moves counter

    # main loop: extend the path until desired length reached
    while i < constants.path_length:
        # pick a random direction and compute the candidate coordinates
        sides = 0  # number of adjacent path blocks at the candidate
        cur_x = x
        cur_y = y
        rand = random.randint(0, 3)
        if rand == 0:
            y -= 1  # move up
        elif rand == 1:
            x += 1  # right
        elif rand == 2:
            y += 1  # down
        elif rand == 3:
            x -= 1  # left
        cur_block = objects.Block.create(x, y)

        # count how many of the four neighbors are already part of the path
        neighboring_blocks = [objects.Block.create(x, y-1),
                              objects.Block.create(x+1, y),
                              objects.Block.create(x, y+1),
                              objects.Block.create(x-1, y)]
        for block in neighboring_blocks:
            if check_if_in_blocks(blocks, block):
                sides += 1

        # validate the candidate: ensure it is within the grid, not
        # already used, and does not create a junction (no more than one
        # adjacent existing path cell).  If it fails, revert and increment
        # the `stuck` counter so we can abort after too many retries.

        if cur_block.y < 1 or cur_block.x < 1 or \
           cur_block.y > constants.LINES - 2 or cur_block.x > constants.ROWS - 2:
            # out of bounds – backtrack
            x = cur_x
            y = cur_y
        elif check_if_in_blocks(blocks, cur_block):
            # already visited tile – backtrack and increment stuck counter
            x = cur_x
            y = cur_y
            stuck += 1
        elif sides > 1:
            # would create a fork/junction
            print("too many sides")
            x = cur_x
            y = cur_y
            stuck += 1
        elif cur_block.check_if_path() == False:
            # valid new path segment; draw it white
            pygame.draw.rect(constants.background, (255, 255, 255),
                             (x*constants.block_width, y*constants.block_height,
                              constants.block_width, constants.block_height))
            if i == constants.path_length - 1:
                # mark the end block in red
                pygame.draw.rect(constants.background, (255, 0, 0),
                                 (x*constants.block_width, y*constants.block_height,
                                  constants.block_width, constants.block_height))
                cur_block.end = True
                end_block = cur_block
            print(f"Block {x}, {y} is now a path")
            cur_block.is_path = True
            blocks.append(cur_block)
            stuck = 0
            i += 1
        else:
            # tile already flagged as path via another check
            x = cur_x
            y = cur_y
            stuck += 1
        
        # if we have retried too often without progress, bail out and return False
        if stuck > 10:
            print("stuck")
            return False, 0


    return True, end_block