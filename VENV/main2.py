import sys, pygame # type: ignore
import constants
import functions
import objects
pygame.init()

"""
!!!!!!!!Next time you need to fix the game overe, doesnt work!!!!!!!
"""


def main():
    finished = False
    constants.screen.fill(constants.blue)

    #loading path

    while not finished:
        finished, end_block = functions.draw_path(constants.blocks)
        if not finished:
            print("Path generation failed; retrying")
            constants.background.fill(constants.blue)
            constants.blocks = []
    pygame.display.flip()

    x_of_fast, x_of_slow, last_spawn_time, fast_enemy, slow_enemy = functions.spawn_wave(5, 3, 5000, 0)
    last_spawn_time = 0
    constants.fast_enemies.append(fast_enemy)
    fast_enemy.going_to = fast_enemy.pick_where_to(constants.blocks, constants.start_block) 


    while True:
        cur_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if constants.game_over:
                # Draw the game-over screen every frame
                constants.retry = functions.game_over(event)

        if constants.retry:
            return False

        x_of_fast, x_of_slow, last_spawn_time, fast_enemy, slow_enemy = functions.spawn_wave(x_of_fast, x_of_slow, cur_time, last_spawn_time)
        if fast_enemy != None:
            constants.fast_enemies.append(fast_enemy)
            print("Fast enemy appended")
            fast_enemy.going_to = fast_enemy.pick_where_to(constants.blocks, constants.start_block)
        if slow_enemy != None:
            constants.slow_enemies.append(slow_enemy)
            slow_enemy.going_to = slow_enemy.pick_where_to(constants.blocks, constants.start_block)
        
        constants.screen.blit(constants.background, (0, 0))

        for fast_enemy in constants.fast_enemies:
            fast_enemy.going_to = functions.move_enemy(fast_enemy, fast_enemy.going_to)
            pygame.draw.circle(constants.screen, (255, 0, 0), (fast_enemy.x_middle, fast_enemy.y_middle), 10)
            constants.game_over = functions.check_if_over(end_block, fast_enemy)

        for slow_enemy in constants.slow_enemies:
            slow_enemy.going_to = functions.move_enemy(slow_enemy, slow_enemy.going_to)
            pygame.draw.circle(constants.screen, (0, 255, 0), (slow_enemy.x_middle, slow_enemy.y_middle), 10)
            constants.game_over = functions.check_if_over(end_block, slow_enemy)

        
        pygame.display.flip()

continue_playing = True

while continue_playing:
    main()
    
    
    

