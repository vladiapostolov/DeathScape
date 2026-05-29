from health_object import health_obj
from ammo_object import ammo_obj
from grenade_object import grenade_obj

def object_factory(x, y, number):
    if 1 <= number <= 4:
        return health_obj(x, y, 50)
    elif 4 < number <= 8:
        return ammo_obj(x, y, 12)
    elif number > 8 and number <= 12:
        return grenade_obj(x, y)
    return None