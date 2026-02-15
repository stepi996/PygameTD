import constants
import pygame # type: ignore
pygame.init()

class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_path = False
        self.x_middle = (self.x * constants.block_width + (self.x + 1) * constants.block_width) / 2
        self.y_middle = (self.y * constants.block_height + (self.y + 1) * constants.block_height) / 2
        self.end = False

    def check_if_path(self):
        """Checks if the block is already a path, if not, it turns it into a path and returns False, if it is already a path, it returns True"""
        if self.is_path:
            return True
        else:
            return False
    
    @classmethod
    def create(cls, x, y):
        """creates a block with given coordinates"""
        return cls(x, y)
    

class Enemy():
    def __init__(self, x, y, speed, HP, size=10):
        self.x_middle = (x * constants.block_width + (x + 1) * constants.block_width) / 2
        self.y_middle = (y * constants.block_height + (y + 1) * constants.block_height) / 2
        self.body = pygame.Rect(self.x_middle, self.y_middle, size, size)
        self.speed = speed
        self.HP = HP
        self.going_to = constants.start_block
        self.already_gone = [False]

    def pick_where_to(self, blocks, cur_block):
        neighboring_blocks = [Block.create(cur_block.x, cur_block.y-1), Block.create(cur_block.x+1, cur_block.y), Block.create(cur_block.x, cur_block.y+1), Block.create(cur_block.x-1, cur_block.y)]
        for neighbor_block in neighboring_blocks:
            for block in blocks:
                if neighbor_block.x == block.x and neighbor_block.y == block.y and block.check_if_path() and block not in self.already_gone:
                    going_to = block
                    self.already_gone.append(cur_block)
                    return going_to
        else:
            print("Something went wrong, no neighboring blocks are paths or all neighboring path blocks have already been gone to")
            return None

    def move(self, going_to):
        """moves enemy to the next coordinate"""
        if self.x_middle < going_to.x_middle:
            self.x_middle += self.speed
            if self.x_middle > going_to.x_middle:
                self.x_middle = going_to.x_middle
        if self.x_middle > going_to.x_middle:
            self.x_middle -= self.speed
            if self.x_middle < going_to.x_middle:
                self.x_middle = going_to.x_middle
        if self.y_middle < going_to.y_middle:
            self.y_middle += self.speed
            if self.y_middle > going_to.y_middle:
                self.y_middle = going_to.y_middle
        if self.y_middle > going_to.y_middle:
            self.y_middle -= self.speed
            if self.y_middle < going_to.y_middle:
                self.y_middle = going_to.y_middle

    def draw(self, color, screen):
        pygame.draw.circle(screen, color, (self.x_middle, self.y_middle), 10)

    @classmethod
    def create(cls, x, y, color, speed=1, HP=100):
        """creates an enemy with given coordinates, speed and HP"""
        enemy = cls(x, y, speed, HP)
        enemy.draw(color, constants.screen)
        return enemy
    


class Text():
    def __init__(self, text, textColor=(255, 255, 255), backgroundColor=(0, 0, 0)):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(text, True, textColor, backgroundColor)
        self.text_rect = self.text.get_rect()
        #make it center
   
    @classmethod
    def create(cls, text, textColor=(255, 255, 255), backgroundColor=(0, 0, 0)):
        return cls(text, textColor, backgroundColor)
    

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (70, 130, 180)

    def draw(self, screen, font=pygame.font.Font('freesansbold.ttf', 32)):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    @classmethod
    def create(cls, x, y, width, height, text):
        button = cls(x, y, width, height, text)
        button.draw(constants.screen)
        return button