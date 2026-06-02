class ThrowGrenade:
    def __init__(self, start_x, start_y, target_x, target_y, flight_time, damage, explosion_radius):
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.flight_time = flight_time
        self.damage = damage
        self.explosion_radius = explosion_radius
        self.t = 0.0
        self.x = start_x
        self.y = start_y
        self.arc_height = 70
        self.exploded = False
        self.explosion_timer = 0.0