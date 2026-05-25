SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

class Bullet:
    def __init__(self, x, y, speed, damage, facing):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.facing = facing
        self.collided = False
        self.killed_enemy = False
        
    def updateBullet(self, dt):
        if self.facing == 'right':
            self.x += self.speed * dt
        elif self.facing == 'left':
            self.x -= self.speed * dt
    
    def isOffMap(self):
        return self.x > SCREEN_WIDTH or self.x < 0
        