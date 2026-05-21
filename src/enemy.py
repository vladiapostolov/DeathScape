class Enemy:
    def __init__(self, enemy_x, enemy_y):
        self.x = enemy_x
        self.y = enemy_y
        self.health = 100
        self.is_dead = False
        
    def take_damage(self, to_receive):
        self.health -= to_receive
        self.is_dead = True if self.health == 0 else False
    