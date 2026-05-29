from random_object import random_object

class grenade_obj(random_object):
    def __init__(self, enemy_x, enemy_y):
        super().__init__(enemy_x, enemy_y)
        self.is_activated = False
    
    def apply_to_player(self, player_object):
        player_object.grenades_count += 1