from random_object import random_object

class ammo_obj(random_object):
    def __init__(self, enemy_x, enemy_y, ammo):
        super().__init__(enemy_x, enemy_y)
        self.ammo = ammo
        self.is_activated = False

    def apply_to_player(self, player_object):
        player_object.ammo += self.ammo
