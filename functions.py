# Import required modules and initialize pygame
import random
from enemy import *
from objects import *
pygame.init()

# Moves an enemy to the next block along its path
def move_enemy(enemy, going_to):
    """moves the enemy to the next block"""
    if enemy.x_middle != going_to.x_middle or enemy.y_middle != going_to.y_middle:
        enemy.move(going_to)
    elif not going_to.end:
        going_to = enemy.pick_where_to(constants.blocks, going_to) 
    return going_to

# Opens the tower build screen for the selected block
def open_tower_build_screen(cur_block, event):
    # Mark the current block as path if it matches any block in the grid
    for block in constants.blocks:
        if cur_block.x == block.x and cur_block.y == block.y:
            cur_block.is_path = True
    
    # Check if a tower is already present on the block
    is_tower_on = cur_block.check_if_tower_on()
    
    # If block is not a path and no tower is present, show tower build UI
    if not cur_block.is_path and not is_tower_on:
        button = cur_block.tower_build_screen(constants.menu_screen, event)
        return True, button
    return False, Button.create(0,0,0,0,"")

def open_tower_menu(cur_block, event):
    # Check if a tower is present on the block
    is_tower_on = cur_block.check_if_tower_on()
    
    # If a tower is present, show the tower menu UI
    if is_tower_on:
        for tower in constants.towers:
            if tower.x == cur_block.x and tower.y == cur_block.y:
                tbs_stays, button = tower.tower_menu(constants.menu_screen, event)
                return tbs_stays, button
    return False, Button.create(0,0,0,0,"")

def no_button_clicked(event, buttons, block):
    """Checks if any button in the list of buttons is clicked, if not, it returns True, if so, it returns False"""
    for button in buttons:
        if button.is_clicked(event):
            return False
    return True

# Spawns a wave of enemies gradually over time
def spawn_wave(x_of_fast, x_of_slow, x_of_camo, cur_time, last_spawn_time, difficulty):
    """Spawns enemies gradually over time."""
    spawn_time = constants.spawn_time  # Time delay between spawns
    fast_enemy = None
    slow_enemy = None
    camo_enemy = None
    new_wave = False
    if cur_time - last_spawn_time >= spawn_time:
        if x_of_fast > 0:
            # Spawn one fast enemy
            print("Spawning fast enemy")
            fast_enemy = Enemy.create(1, 0, (255, 0, 0), 1.5, difficulty*100)
            x_of_fast -= 1
            last_spawn_time = cur_time
        elif x_of_slow > 0:
            # Spawn one slow enemy
            slow_enemy = Enemy.create(1, 0, (0, 255, 0), 0.75, difficulty*200)
            x_of_slow -= 1
            last_spawn_time = cur_time
        elif x_of_camo > 0:
            # Spawn one camo enemy
            camo_enemy = Enemy.create(1, 0, (255, 255, 0), 1.25, difficulty*150, camo=True)
            x_of_camo -= 1
            last_spawn_time = cur_time
        else:
            new_wave = True

    return x_of_fast, x_of_slow, x_of_camo, last_spawn_time, fast_enemy, slow_enemy, camo_enemy, new_wave

def start_new_wave():
    # begin next wave: increase difficulty and recalc spawn counts
    constants.spawn_time -= 100
    if constants.spawn_time < 100:
        constants.spawn_time = 100
    if constants.wave % 2 == 0:
        constants.difficulty *= 1.4
    # Configure composition for the wave we are about to start.
    next_wave = constants.wave + 1
    if next_wave == 3 or next_wave == 7:
        x_of_fast = 0
    else:
        x_of_fast = int(constants.difficulty * random.randint(3, 8))
    if next_wave >= 3 and next_wave != 7:
        x_of_slow = int(constants.difficulty * random.randint(1, 5))
    else:
        x_of_slow = 0
    if next_wave >= 7:
        x_of_camo = int(constants.difficulty * random.randint(1, 3))
    else:
        x_of_camo = 0
    constants.wave = next_wave
    if constants.wave % 3 == 0:
        constants.gold_gained_from_camo -= 2
        if constants.gold_gained_from_camo < 1:
            constants.gold_gained_from_camo = 1
        constants.gold_gained_from_slow -= 2
        if constants.gold_gained_from_slow < 1:
            constants.gold_gained_from_slow = 1
        constants.gold_gained_from_fast -= 1
        if constants.gold_gained_from_fast < 1:
            constants.gold_gained_from_fast = 1
    print(f"Wave {constants.wave} started")
    return x_of_fast, x_of_slow, x_of_camo

# Handles spawning and appending enemies to the game lists
def spawn_enemy(x_of_fast, x_of_slow, x_of_camo, cur_time, last_spawn_time, difficulty):
    x_of_fast, x_of_slow, x_of_camo, last_spawn_time, fast_enemy, slow_enemy, camo_enemy, new_wave = spawn_wave(x_of_fast, x_of_slow, x_of_camo, cur_time, last_spawn_time, difficulty)
    if fast_enemy != None:
        constants.fast_enemies.append(fast_enemy)
        constants.enemies.append(fast_enemy)
        print("Fast enemy appended")
        fast_enemy.going_to = fast_enemy.pick_where_to(constants.blocks, constants.start_block)
    if slow_enemy != None:
        constants.slow_enemies.append(slow_enemy)
        constants.enemies.append(slow_enemy)
        print("Slow enemy appended")
        slow_enemy.going_to = slow_enemy.pick_where_to(constants.blocks, constants.start_block)
    if camo_enemy != None:
        constants.camo_enemies.append(camo_enemy)
        constants.enemies.append(camo_enemy)
        print("Camo enemy appended")
        camo_enemy.going_to = camo_enemy.pick_where_to(constants.blocks, constants.start_block)
    return x_of_fast, x_of_slow, x_of_camo, last_spawn_time, new_wave

# Manages enemy movement, drawing, and removal when defeated
def manage_enemies(enemy, enemies, end_block, color):
    for enemy in enemies:
        # Move enemy to next block
        enemy.going_to = move_enemy(enemy, enemy.going_to)
        # Draw enemy on the screen
        enemy.draw(color, constants.screen)
        # Check if enemy is alive
        alive = enemy.check_if_alive()
        if alive == False:
            # Award gold based on enemy type
            if enemies == constants.fast_enemies:
                constants.gold += constants.gold_gained_from_fast
            elif enemies == constants.slow_enemies:
                constants.gold += constants.gold_gained_from_slow
            elif enemies == constants.camo_enemies:
                constants.gold += constants.gold_gained_from_camo
            # Remove defeated enemy from lists
            enemies.remove(enemy)
            constants.enemies.remove(enemy)
            print("Fast enemy removed")
        # Check if enemy reached the end block (game over)
        is_game_over = check_if_over(end_block, enemy)
        if is_game_over:
            constants.game_over = True
            print("Game over triggered by fast enemy")
            break

def manage_UI(self, rect):
    # Default position (above the tile)
    rect.centerx = self.x_middle
    rect.centery = self.y_middle - rect.height

    # If not enough space above → show below
    if rect.top < 0:
        rect.centery = self.y_middle + rect.height

    # Clamp horizontally so it stays on screen
    if rect.left < 0:
        rect.left = 0
    if rect.right > constants.width:
        rect.right = constants.width

    # Clamp vertically (extra safety)
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > constants.height:
        rect.bottom = constants.height

    # If not enough space above → show below
    if rect.top < 0:
        rect.centery = self.y_middle + rect.height

    # Clamp horizontally so it stays on screen
    if rect.left < 0:
        rect.left = 0
    if rect.right > constants.width:
        rect.right = constants.width

    # Clamp vertically (extra safety)
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > constants.height:
        rect.bottom = constants.height

    return rect
        

# Displays the game over screen and handles retry button
def game_over(event=None):
    """Creates (and optionally handles) the game over screen"""

    # Draw the game-over screen
    game_over_rect = pygame.draw.rect(constants.screen, (0, 0, 0), (constants.width/2 - 200, constants.height/2 - 100, 400, 200))
    game_over_text_rect = constants.game_over_text.text.get_rect(center=game_over_rect.center)
    game_over_text_rect.midtop = (constants.width/2, constants.height/2 - 50)
    constants.screen.blit(constants.game_over_text.text, game_over_text_rect)
    # Create and draw the retry button
    retry_button = objects.Button.create(game_over_rect.centerx - 50, game_over_rect.centery + 25, 100, 45, "Retry")
    retry_button.draw(constants.screen)
    # Check if retry button is clicked
    if event is not None and retry_button.is_clicked(event):
        return True
    return False

# Checks if the enemy has reached the end block
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

