class Hero:
    def __init__(self, cur_x, cur_y):
        self.health = 100
        self.x = cur_x
        self.y = cur_y
        self.ammo = 50
    
    def __getattr__(self, to_return):
        if to_return == 'x':
            return self.x
        elif to_return == 'y':
            return self.y
        elif to_return == 'health':
            return self.health
        elif to_return == 'ammo':
            return self.ammo
        else:
            raise ValueError("Invalid get argument passed")
    
    def shoot(self, shotFired):
        self.ammo -= 1