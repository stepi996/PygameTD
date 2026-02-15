import random
import constants
import objects
import pygame # type: ignore
pygame.init()

def check_if_in_blocks(blocks, cur_block):
    """checks if the current block is in the list of blocks"""

    for block in blocks:
        if block.x == cur_block.x and block.y == cur_block.y:
            return True
    return False

def draw_path(blocks, x=1, y=0):
    """generates a random path on the screen starting from the top left corner"""

    #generates starting block

    pygame.draw.rect(constants.background, (0, 255, 0), (x*constants.block_width, y*constants.block_height, constants.block_width, constants.block_height))
    blocks.append(constants.start_block)
    i = 0
    stuck = 0

    #generates path

    while i < constants.path_length:
        sides = 0
        cur_x = x
        cur_y = y
        rand = random.randint(0, 3)
        if rand == 0:
            y -= 1
        elif rand == 1:
            x += 1
        elif rand == 2:
            y += 1
        elif rand == 3:
            x -= 1
        cur_block = objects.Block.create(x, y)

        #checks neghboring blocks
        
        neighboring_blocks = [objects.Block.create(x, y-1), objects.Block.create(x+1, y), objects.Block.create(x, y+1), objects.Block.create(x-1, y)]
        for block in neighboring_blocks:
            if check_if_in_blocks(blocks, block):
                sides += 1

        #checks if block is out of bounds, if it is already a path, or if it has more than 1 neighboring path blocks, if any of these are true, it goes back to the previous block and tries again, if not, it turns the block into a path block and adds it to the list of blocks

        if cur_block.y < 1 or cur_block.x < 1 or cur_block.y > constants.LINES - 2 or cur_block.x > constants.ROWS - 2:
            x = cur_x
            y = cur_y
        elif check_if_in_blocks(blocks, cur_block):
            x = cur_x
            y = cur_y
            stuck += 1
        elif sides > 1:
            print("too many sides")
            x = cur_x
            y = cur_y
            stuck += 1
        elif cur_block.check_if_path() == False:
            pygame.draw.rect(constants.background, (255, 255, 255), (x*constants.block_width, y*constants.block_height, constants.block_width, constants.block_height))
            if i == constants.path_length - 1:
                pygame.draw.rect(constants.background, (255, 0, 0), (x*constants.block_width, y*constants.block_height, constants.block_width, constants.block_height))
                cur_block.end = True
                end_block = cur_block
            print(f"Block {x}, {y} is now a path")
            cur_block.is_path = True
            blocks.append(cur_block)
            stuck = 0
            i += 1
        else:
            x = cur_x
            y = cur_y
            stuck += 1
        
        #stops the function if it gets stuck in a loop and can't find a path after 10 tries

        if stuck > 10:
            print("stuck")
            return False, 0


    return True, end_block


def move_enemy(enemy, going_to):
    """moves the enemy to the next block"""
    if enemy.x_middle != going_to.x_middle or enemy.y_middle != going_to.y_middle:
        enemy.move(going_to)
    elif not going_to.end:
        going_to = enemy.pick_where_to(constants.blocks, going_to) 
    return going_to

# Create a persistent retry button
retry_button = None


def spawn_wave(x_of_fast, x_of_slow, cur_time, last_spawn_time):
    """Spawns enemies gradually over time."""
    spawn_time = 5000  # Time delay between spawns
    fast_enemy = None
    slow_enemy = None
    print(f"Current time: {cur_time}, Last spawn time: {last_spawn_time}")
    if cur_time - last_spawn_time >= spawn_time:
        if x_of_fast > 0:
            # Spawn one fast enemy
            print("Spawning fast enemy")
            
            fast_enemy = objects.Enemy.create(1, 0, (255, 0, 0), 0.1)
            x_of_fast -= 1
            last_spawn_time = cur_time
        elif x_of_slow > 0:
            # Spawn one slow enemy
            slow_enemy = objects.Enemy.create(1, 0, (0, 255, 0), 0.05, 200)
            x_of_slow -= 1
            last_spawn_time = cur_time

    return x_of_fast, x_of_slow, last_spawn_time, fast_enemy, slow_enemy



def game_over(event=None):
    """Creates (and optionally handles) the game over screen"""
    global retry_button

    # Draw the game-over screen
    game_over_rect = pygame.draw.rect(constants.screen, (0, 0, 0), (constants.width/2 - 200, constants.height/2 - 100, 400, 200))
    game_over_text_rect = constants.game_over_text.text.get_rect(center=game_over_rect.center)
    game_over_text_rect.midtop = (constants.width/2, constants.height/2 - 50)
    constants.screen.blit(constants.game_over_text.text, game_over_text_rect)

    # Create the retry button if it doesn't exist
    if retry_button is None:
        retry_button = objects.Button.create(game_over_rect.centerx - 50, game_over_rect.centery + 25, 100, 45, "Retry")

    # Draw the retry button
    retry_button.draw(constants.screen)

    # Handle click events
    if event is not None and retry_button.is_clicked(event):
        return True
    return False



def check_if_over(end_block, enemy):
    """checks if the enemy has reached the end block, if it has, it blits the game over text and returns False, if not, it returns True"""

    if enemy.x_middle == end_block.x_middle and enemy.y_middle == end_block.y_middle:
        game_over_rect = pygame.draw.rect(constants.screen, (0, 0, 0), (constants.width/2 - 200, constants.height/2 - 100, 400, 200))
        game_over_text_rect = constants.game_over_text.text.get_rect(center=game_over_rect.center)
        game_over_text_rect.midtop = (constants.width/2, constants.height/2 - 50)

        retry_button = objects.Button.create(game_over_rect.centerx - 50, game_over_rect.centery + 25, 100, 45, "Retry")
        constants.screen.blit(constants.game_over_text.text, game_over_text_rect)
        return True
    else:
        return False

