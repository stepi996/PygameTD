while not finished:
    finished = functions.draw_path(constants.blocks)
    if not finished:
        print("Path generation failed; retrying")
        constants.screen.fill(constants.blue)
        constants.blocks = []