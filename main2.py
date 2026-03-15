# standard library imports
import sys, pygame # type: ignore

# local modules providing game logic
import functions
import path
from enemy import *   # enemy types and movement code
from tutorial import * # tutorial screen code

# initialize pygame once at startup
pygame.init()


"""
Udělat tutorial, přidat jednoduché sprity, popřípadě vybalancovat
"""


def main():
    """Main game loop. Runs until the player quits or chooses to retry.

    This function encapsulates one play session; when the player loses and
    presses retry it returns False and the outer loop resets state.
    """

    # state used during path creation / tower placing
    finished = False
    cur_block = Block.create(0,0)      # block under mouse
    previous_block = Block.create(0,0) # previous mouse block
    buttons = [Button.create(0,0,0,0,"")]

    # clear screen background colour before drawing path
    constants.screen.fill(constants.blue)

    #--- generate the enemy path before starting gameplay ---
    # path.draw_path returns a tuple (finished, end_block), and will
    # keep redrawing until a valid path is produced.
    while not finished:
        finished, end_block = path.draw_path(constants.blocks)
        if not finished:
            print("Path generation failed; retrying")
            constants.background.fill(constants.blue)
            constants.blocks = []  # clear blocks and try again
    pygame.display.flip()  # show the completed path on the screen

    x_of_fast, x_of_slow, x_of_camo, last_spawn_time, fast_enemy, slow_enemy, camo_enemy, new_wave = functions.spawn_wave(5, 0, 0, 3000, 0, constants.difficulty)
    constants.fast_enemies.append(fast_enemy)
    constants.enemies.append(fast_enemy)
    fast_enemy.going_to = fast_enemy.pick_where_to(constants.blocks, constants.start_block) 
    
    next = 0
    while constants.first_time:
        constants.clock.tick(60)
        click_event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_event = event

        # Show tutorial message and wait for player to click to continue
        constants.screen.blit(constants.background, (0, 0))
        next = basics(constants.screen, next, click_event)
        if next > 8:
            constants.first_time = False
        pygame.display.flip()

    while not constants.game_over:
        # --- per-frame timing and input ---
        cur_time = pygame.time.get_ticks()      # current time in ms
        constants.clock.tick(60)               # cap at 60 FPS
        mouse_pos = pygame.mouse.get_pos()      # current mouse position
        event = None
        retry_clicked = False

        # keep HUD counters in sync with current game state
        constants.current_towers = len(constants.towers)
        constants.max_towers = constants.wave + 1

        # create HUD text for current wave number and player gold
        # these are re-generated each frame so they reflect up-to-date values
        wave_text = Text.create(f"Wave: {constants.wave}", textColor=(186, 184, 47))
        wave_rect = wave_text.text.get_rect()
        wave_rect.topright = (constants.width - 10, constants.height - 35)
        gold_text = Text.create(f"Gold: {constants.gold}", textColor=(186, 184, 47))
        gold_rect = gold_text.text.get_rect()
        gold_rect.topright = (constants.width - 10, constants.height - 69)
        max_towers_text = Text.create(f"Towers: {constants.current_towers}/{constants.max_towers}", textColor=(186, 184, 47))
        max_towers_rect = max_towers_text.text.get_rect()
        max_towers_rect.topright = (constants.width - 10, constants.height - 103)

        # process all pending events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # user closed the window
            if constants.game_over:
                # when the game is over we still need to display the overlay
                retry_clicked = functions.game_over(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and functions.no_button_clicked(event, buttons, cur_block):
                # start a tower build screen on clicked block
                previous_block = cur_block
                previous_block.tbs_stays = False
                cur_block = Block.create(mouse_pos[0] // constants.block_width,
                                         mouse_pos[1] // constants.block_height)
                cur_block.tbs_stays, buttons = functions.open_tower_build_screen(cur_block, event)
                if cur_block.check_if_tower_on():
                    # if there's already a tower, open the tower menu instead
                    cur_block.tbs_stays, buttons = functions.open_tower_menu(cur_block, event)

        # draw transparent menu layer; tower build dialog may be drawn here
        constants.menu_screen.fill((0, 0, 0, 0))
        if cur_block.tbs_stays:
            if not cur_block.check_if_tower_on():
                buttons = cur_block.tower_build_screen(constants.menu_screen, event)
            else:
                cur_block.tbs_stays, buttons = functions.open_tower_menu(cur_block, event)
        else:
            buttons = [Button.create(0, 0, 0, 0, "")]  # clear buttons if no menu should be open

        # spawn enemies according to wave counters and difficulty
        x_of_fast, x_of_slow, x_of_camo, last_spawn_time, new_wave = functions.spawn_enemy(x_of_fast, x_of_slow, x_of_camo, cur_time, last_spawn_time, constants.difficulty)
        if new_wave:
            x_of_fast, x_of_slow, x_of_camo = functions.start_new_wave()
        
        # render background and then all active towers/projectiles
        constants.screen.blit(constants.background, (0, 0))

        for tower in constants.towers:
            tower.draw(constants.screen)
            tower.shoot_enemy(cur_time)  # each tower handles its own cooldown

        for projectile in constants.projectiles:
            projectile.move()
            projectile.draw(constants.screen)
            projectile.hit_target(constants.projectiles)

        # overlay GUI elements (menu, wave/gold text)
        constants.screen.blit(constants.menu_screen, (0, 0))
        constants.screen.blit(wave_text.text, wave_rect)
        constants.screen.blit(gold_text.text, gold_rect)
        constants.screen.blit(max_towers_text.text, max_towers_rect)

        # update and render all enemies, remove any that die or reach the end
        functions.manage_enemies(fast_enemy, constants.fast_enemies, end_block, (255, 0, 0))

        # handle slower green enemies separately
        functions.manage_enemies(slow_enemy, constants.slow_enemies, end_block, (0, 255, 0))

        # handle camo enemies separately
        functions.manage_enemies(camo_enemy, constants.camo_enemies, end_block, (255, 255, 0))

        
        pygame.display.flip()

    # Stay on game-over screen until player explicitly clicks Retry.
    while True:
        constants.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if functions.game_over(event):
                return

        functions.game_over()
        pygame.display.flip()

# ---------------------------------------------------------------------
# outer loop that allows the player to restart the game when they lose
# ---------------------------------------------------------------------
continue_playing = True

while continue_playing:
    main()  # run a single playthrough

    # reset all mutable global constants back to their defaults
    constants.game_over = False
    constants.background.fill(constants.blue)
    constants.blocks = []
    constants.retry = False
    constants.difficulty = 1
    constants.wave = 1
    constants.max_towers = constants.wave + 1
    constants.towers = []
    constants.current_towers = len(constants.towers)
    constants.projectiles = []
    constants.fast_enemies = []
    constants.slow_enemies = []
    constants.camo_enemies = []
    constants.enemies = []
    constants.gold = 100

