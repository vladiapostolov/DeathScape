import random_object
import health_object

def object_factory(random_object, number):
    if number >=1 and number <=4:
        return health_object(random_object.x, random_object.y)
    elif number > 4 and number <= 8:
        return #to implement ammo
    elif number > 8 and number <= 12:
        return # to implement grenade