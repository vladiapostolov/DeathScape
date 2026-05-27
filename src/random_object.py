from abc import ABC, abstractmethod

class random_object(ABC):
    def __init__(self, enemy_x, enemy_y):
        self.x = enemy_x
        self.y = enemy_y
    
    @abstractmethod
    def apply_to_player(self, player_object):
        raise NotImplementedError
    
    