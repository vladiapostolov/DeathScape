from random_object import random_object

class health_obj(random_object):
    def __init__(self, enemy_x, enemy_y, health):
        super().__init__(enemy_x, enemy_y)
        self.health = health
        self.is_activated = False
        
    def apply_to_player(self, player_object):
        player_object.health = min(100, player_object.health + self.health)