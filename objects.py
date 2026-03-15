# Import required modules and constants
import constants
import pygame # type: ignore
from tower import *
import functions
pygame.init()

# Represents a single block/tile on the game grid
class Block():
    def __init__(self, x, y):
        self.x = x  # Grid X coordinate
        self.y = y  # Grid Y coordinate
        self.is_path = False  # Is this block part of the enemy path?
        self.is_tower_on = False  # Is there a tower on this block?
        self.tbs_stays = False  # Should the tower build screen stay open?
        # Calculate the center position of the block
        self.x_middle = (self.x * constants.block_width + (self.x + 1) * constants.block_width) / 2
        self.y_middle = (self.y * constants.block_height + (self.y + 1) * constants.block_height) / 2
        self.end = False  # Is this block the end of the path?

    # Checks if the block is already a path
    def check_if_path(self):
        """Checks if the block is already a path, if not, it turns it into a path and returns False, if it is already a path, it returns True"""
        if self.is_path:
            return True
        else:
            return False
        
    # Checks if a tower is present on the block
    def check_if_tower_on(self):
        for tower in constants.towers:
            if tower.x == self.x and tower.y == self.y:
                return True
        
    # Displays the tower build screen UI for this block
    def tower_build_screen(self, screen, event):
        if not self.check_if_path() and not self.check_if_tower_on():
            buttons = []
            rect = functions.manage_UI(self, pygame.Rect(0, 0, constants.block_width * 5, constants.block_height * 3))
            build_button = Button.create(0, 0, rect.width - constants.block_width*2.9, rect.height - 30, "Build Tower", font=pygame.font.Font('freesansbold.ttf', 16))
            buttons.append(build_button)

            # Set gold text color based on player's gold
            if constants.gold >= 100:
                textColor = (199, 182, 30)  # Gold color if enough gold
            else:
                textColor = (255, 0, 0)    # Red color if not enough gold
            gold_text = Text.create("100 gold", 16, textColor)  # transparent bg
            gold_rect = gold_text.text.get_rect()
            gold_rect.center = (rect.centerx, rect.centery + constants.block_height + 10)

            # Center button inside rect
            build_button.rect.center = (rect.center[0], rect.center[1] - 7)

            # Draw the build screen UI
            pygame.draw.rect(screen, (65, 74, 89), rect)
            build_button.draw(screen)
            screen.blit(gold_text.text, gold_rect)

            # Handle build button click and tower creation
            if build_button.is_clicked(event):
                if constants.gold >= 100 and len(constants.towers) < constants.max_towers:
                    constants.gold -= 100  # Deduct gold for building tower
                    print("Button clicked")
                    tower = Tower.create(self.x, self.y, 100, 50)
                    constants.towers.append(tower)
                    self.tbs_stays = False
  
            return buttons

    # Class method to create a new block
    @classmethod
    def create(cls, x, y):
        """creates a block with given coordinates"""
        return cls(x, y)

# Text class for rendering text on the screen
class Text():
    def __init__(self, text, font_size=32, textColor=(255, 255, 255), backgroundColor=None):
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = self.font.render(text, True, textColor, backgroundColor)
        self.text_rect = self.text.get_rect()

    # Class method to create a new text object
    @classmethod
    def create(cls, text, font_size=32, textColor=(255, 255, 255), backgroundColor=None):
        return cls(text, font_size, textColor, backgroundColor)
    

# Button class for clickable UI buttons
class Button():
    def __init__(self, x, y, width, height, text, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (70, 130, 180)
        self.font = font if font is not None else pygame.font.Font('freesansbold.ttf', 32)

    # Draws the button on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # Checks if the button was clicked based on the event
    def is_clicked(self, event):
        if event is None:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    # Class method to create and draw a new button
    @classmethod
    def create(cls, x, y, width, height, text, font=None):
        if font is None:
            font = pygame.font.Font('freesansbold.ttf', 32)
        button = cls(x, y, width, height, text, font)
        button.draw(constants.screen)
        return button
