#we use singleton so we have one Item object that fucks around and spams the items
class Items:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.bullets = []
            cls._instance.shields = []
        return cls._instance

    def __init__(self):
        self.bullets = []
        self.shields = []

    def add_bullets(self, bullet_rect):
        self.bullets.append(bullet_rect)
    
    def add_shields(self, shield_rect):
        self.shields.append(shield_rect)