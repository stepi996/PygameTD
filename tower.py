# Import required modules and constants
import pygame # type: ignore
import constants
from enemy import *
import objects
import functions
from math import sqrt 
from upgrades import *

# Tower class represents a defensive structure that attacks enemies
class Tower():
    def __init__(self, x, y, range, damage):
        self.x = x  # Grid X coordinate
        self.y = y  # Grid Y coordinate
        self.tier = 1
        self.body_color = (128, 128, 128)
        self.dot_color = (252, 249, 3)
        self.dot_size = 5
        self.range = range  # Attack range of the tower
        self.damage = damage  # Damage dealt per shot
        self.green_multiplier = 1  # Multiplier for green damage upgrade
        self.can_attack_camo = False  # Whether the tower can attack camo enemies
        self.fire_rate = 1000  # Time between shots (ms)
        self.num_of_projectiles = 1  # Number of projectiles fired at once
        self.last_shot_time = 0  # Last time the tower fired
        # Calculate the center position of the tower
        self.x_middle = (self.x * constants.block_width + (self.x + 1) * constants.block_width) / 2
        self.y_middle = (self.y * constants.block_height + (self.y + 1) * constants.block_height) / 2

    # Finds the closest enemy within range
    def find_enemy(self, enemies):
        """finds the closest enemy within range and returns it, if there are no enemies within range, it returns None"""
        for enemy in enemies:
            enemy_location = (enemy.x_middle, enemy.y_middle)
            distance = sqrt((enemy_location[0] - self.x_middle)**2 + (enemy_location[1] - self.y_middle)**2)
            if distance <= self.range:
                return enemy, distance
        return None, None
    
    # Attempts to shoot at the nearest enemy, respecting cooldown
    def shoot_enemy(self, cur_time):
        """Try to fire at the nearest enemy. Uses the tower's own cooldown state.

        Returns True if a shot was fired, False otherwise (for debugging/logging).
        """
        enemy, distance = self.find_enemy(constants.enemies)
        if enemy is None:
            return False

        # check cooldown
        if cur_time - self.last_shot_time >= self.fire_rate:
            if distance <= self.range:
                for i in range(self.num_of_projectiles):
                    projectile = Projectile.create(self.x_middle, self.y_middle, self.damage, enemy, self.green_multiplier, self.can_attack_camo)
                    constants.projectiles.append(projectile)
                self.last_shot_time = cur_time
                print(f"Enemy hit! Enemy HP: {enemy.HP}")
                return True
        return False

    def upgrade(self, rect):
        if self.tier == 1:
            options = ["Faster Shots", "More Damage"]
            upgrade_button_1 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, options[0], font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_1 = 125
            functionality_1 = lambda: faster_shots(self)
            upgrade_button_2 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, options[1], font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_2 = 175
            functionality_2 = lambda: more_damage(self)
        elif self.tier == 2:
            options = ["More Range", "Green Damage"]
            upgrade_button_1 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, options[0], font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_1 = 200
            functionality_1 = lambda: more_range(self)
            upgrade_button_2 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, options[1], font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_2 = 225
            functionality_2 = lambda: green_damage(self)
        elif self.tier == 3:
            options = ["Yellow Damage", "Double Shot"]
            upgrade_button_1 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, options[0], font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_1 = 300
            functionality_1 = lambda: yellow_damage(self)
            upgrade_button_2 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, options[1], font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_2 = 300
            functionality_2 = lambda: double_shot(self)
        else:
            upgrade_button_1 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, "No Upgrades Available", font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_1 = 0
            functionality_1 = lambda: None
            upgrade_button_2 = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, "No Upgrades Available", font=pygame.font.Font('freesansbold.ttf', 14))
            gold_cost_2 = 0
            functionality_2 = lambda: None
        return upgrade_button_1, upgrade_button_2, gold_cost_1, gold_cost_2, functionality_1, functionality_2

    def choose_text_color(self, gold_costs):
        textColors = []
        for i in range(len(gold_costs)): 
            if constants.gold >= gold_costs[i]:
                textColor = (199, 182, 30)  # Gold color if enough gold
            else:
                textColor = (255, 0, 0)    # Red color if not enough gold
            textColors.append(textColor)
        return textColors

    def tower_menu(self, screen, event):
        tbs_stays = True
        rect = functions.manage_UI(self, pygame.Rect(0, 0, constants.block_width * 7, constants.block_height * 3))
        delete_button = objects.Button.create(0, 0, rect.width - constants.block_width*5, rect.height - 30, "Delete Tower", font=pygame.font.Font('freesansbold.ttf', 14))
        upgrade_button_1, upgrade_button_2, gold_cost_1, gold_cost_2, functionality_1, functionality_2 = self.upgrade(rect)
        
        # Center button inside rect
        delete_button.rect.center = (rect.center[0] + rect.width/3, rect.center[1] - 7)
        upgrade_button_1.rect.center = (rect.center[0] - rect.width/3, rect.center[1] - 7)
        upgrade_button_2.rect.center = (rect.center[0], rect.center[1] - 7)
        buttons = [delete_button, upgrade_button_1, upgrade_button_2]

        #draw gold cost for upgrade options
        text_colors = self.choose_text_color([gold_cost_1, gold_cost_2])
        gold_text_1 = objects.Text.create(f"{gold_cost_1} gold", 16, text_colors[0])  # transparent bg
        gold_rect_1 = gold_text_1.text.get_rect()
        gold_rect_1.center = (upgrade_button_1.rect.centerx, upgrade_button_1.rect.centery + constants.block_height + 15)
        gold_text_2 = objects.Text.create(f"{gold_cost_2} gold", 16, text_colors[1])  # transparent bg
        gold_rect_2 = gold_text_1.text.get_rect()
        gold_rect_2.center = (upgrade_button_2.rect.centerx, upgrade_button_2.rect.centery + constants.block_height + 15)

        # Draw the build screen UI
        pygame.draw.rect(screen, (65, 74, 89), rect)
        delete_button.draw(screen)
        upgrade_button_1.draw(screen)
        upgrade_button_2.draw(screen)
        screen.blit(gold_text_1.text, gold_rect_1)
        screen.blit(gold_text_2.text, gold_rect_2)

        # Handle delete button click and tower removal
        if delete_button.is_clicked(event):
            print("Delete button clicked")
            constants.towers.remove(self)
            tbs_stays = False

        if upgrade_button_1.is_clicked(event):
            if constants.gold >= gold_cost_1:
                constants.gold -= gold_cost_1
                functionality_1()
                self.tier += 1
                print("Upgrade 1 applied")
                tbs_stays = False

        if upgrade_button_2.is_clicked(event):
            if constants.gold >= gold_cost_2:
                constants.gold -= gold_cost_2
                functionality_2()
                self.tier += 1
                print("Upgrade 2 applied")
                tbs_stays = False

        return tbs_stays, buttons

    # Draws the tower on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.body_color, (self.x * constants.block_width, self.y * constants.block_height, constants.block_width, constants.block_height))
        pygame.draw.circle(screen, self.dot_color, (self.x_middle, self.y_middle), self.dot_size)

    # Class method to create and draw a new tower
    @classmethod
    def create(cls, x, y, range, damage):
        tower = cls(x, y, range, damage)
        tower.draw(constants.screen)
        return tower



# Projectile class represents a projectile fired by a tower
class Projectile(): #inherits move function from Enemy
    def __init__(self, x, y, damage, target, green_multiplier, can_attack_camo):
        self.x = x  # Current X position
        self.y = y  # Current Y position
        self.damage = damage  # Damage dealt to target
        self.green_multiplier = green_multiplier  # Multiplier for green damage upgrade
        self.can_attack_camo = can_attack_camo  # Whether the projectile can hit camo enemies
        self.speed = 10  # Movement speed of projectile
        self.target = target  # Target enemy
        self.hit = False  # Whether the projectile has hit its target

    # Moves the projectile towards its target
    def move(self):
        """moves enemy to the next coordinate"""
        if self.x < self.target.x_middle:
            self.x += self.speed
            if self.x > self.target.x_middle:
                self.x = self.target.x_middle
        if self.x > self.target.x_middle:
            self.x -= self.speed
            if self.x < self.target.x_middle:
                self.x = self.target.x_middle
        if self.y < self.target.y_middle:
            self.y += self.speed
            if self.y > self.target.y_middle:
                self.y = self.target.y_middle
        if self.y > self.target.y_middle:
            self.y -= self.speed
            if self.y < self.target.y_middle:
                self.y = self.target.y_middle

    # Handles collision with the target and applies damage
    def hit_target(self, projectiles):
        if self.target is not None:
            if self.x == self.target.x_middle and self.y == self.target.y_middle:
                if self.target.camo and not self.can_attack_camo:
                    self.damage = 0  # Projectile cannot hit camo enemy
                    print("Projectile cannot hit camo enemy!")
                elif self.target in constants.slow_enemies:
                    self.damage *= self.green_multiplier
                self.target.HP -= self.damage
                print(f"Enemy hit by projectile! Enemy HP: {self.target.HP}")
                self.hit = True
        
        if self.hit:
            projectiles.remove(self)

    # Draws the projectile on the screen
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 3)

    # Class method to create a new projectile
    @classmethod
    def create(cls, x, y, damage, target, green_multiplier, can_attack_camo):
        projectile = cls(x, y, damage, target, green_multiplier, can_attack_camo)
        projectile.draw(constants.screen)
        return projectile