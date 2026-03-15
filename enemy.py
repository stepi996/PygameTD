# Import required modules and constants
import pygame # type: ignore
import constants
import objects

# Enemy class represents an enemy entity in the game
class Enemy():
    def __init__(self, x, y, speed, HP, camo=False, size=10):
        # Calculate the center position of the enemy based on grid coordinates
        self.x_middle = (x * constants.block_width + (x + 1) * constants.block_width) / 2
        self.y_middle = (y * constants.block_height + (y + 1) * constants.block_height) / 2
        # Create a rectangular body for collision and drawing
        self.body = pygame.Rect(self.x_middle, self.y_middle, size, size)
        self.speed = speed  # Movement speed
        self.HP = HP        # Health points
        self.going_to = constants.start_block  # Next block to move towards
        self.already_gone = []  # List of blocks already visited
        self.camo = camo

    # Determines the next block for the enemy to move to
    def pick_where_to(self, blocks, cur_block):
        neighboring_blocks = [
            objects.Block.create(cur_block.x, cur_block.y-1),
            objects.Block.create(cur_block.x+1, cur_block.y),
            objects.Block.create(cur_block.x, cur_block.y+1),
            objects.Block.create(cur_block.x-1, cur_block.y)
        ]
        for neighbor_block in neighboring_blocks:
            for block in blocks:
                # Move to a neighboring block if it's a path and hasn't been visited
                if neighbor_block.x == block.x and neighbor_block.y == block.y and block.check_if_path() and block not in self.already_gone:
                    going_to = block
                    self.already_gone.append(cur_block)
                    return going_to
        else:
            # No valid neighboring path found
            print("Something went wrong, no neighboring blocks are paths or all neighboring path blocks have already been gone to")
            return None

    # Moves the enemy towards the target block
    def move(self, going_to):
        """moves enemy to the next coordinate"""
        # Move horizontally towards target
        if self.x_middle < going_to.x_middle:
            self.x_middle += self.speed
            if self.x_middle > going_to.x_middle:
                self.x_middle = going_to.x_middle
        if self.x_middle > going_to.x_middle:
            self.x_middle -= self.speed
            if self.x_middle < going_to.x_middle:
                self.x_middle = going_to.x_middle
        # Move vertically towards target
        if self.y_middle < going_to.y_middle:
            self.y_middle += self.speed
            if self.y_middle > going_to.y_middle:
                self.y_middle = going_to.y_middle
        if self.y_middle > going_to.y_middle:
            self.y_middle -= self.speed
            if self.y_middle < going_to.y_middle:
                self.y_middle = going_to.y_middle

    # Draws the enemy as a circle on the screen
    def draw(self, color, screen):
        pygame.draw.circle(screen, color, (self.x_middle, self.y_middle), 10)

    # Checks if the enemy is still alive (HP > 0)
    def check_if_alive(self):
        """checks if the enemy is alive, if it is, it returns True, if it isn't, it returns False"""
        if self.HP > 0:
            return True
        else:
            return False
        

    # Class method to create and draw a new enemy
    @classmethod
    def create(cls, x, y, color, speed=1, HP=100, camo=False):
        """creates an enemy with given coordinates, speed and HP"""
        enemy = cls(x, y, speed, HP, camo)
        enemy.draw(color, constants.screen)
        return enemy