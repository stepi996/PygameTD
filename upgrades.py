from tower import *
import pygame # type: ignore

def faster_shots(tower):
    tower.fire_rate -= 250
    tower.dot_color = (78, 252, 3)

def more_damage(tower):
    tower.damage += 40
    tower.dot_color = (252, 3, 3)

def double_shot(tower):
    tower.num_of_projectiles += 1
    tower.dot_size += 2

def green_damage(tower):
    tower.green_multiplier = 1.75
    tower.body_color = (43, 39, 39)

def yellow_damage(tower):
    tower.can_attack_camo = True
    tower.body_color = (252, 252, 3)

def more_range(tower):
    tower.range += 75
    tower.body_color = (3, 252, 252)