from health_object import health_obj

def object_factory(x, y, number):
    if 1 <= number <= 4:
        return health_obj(x, y, 50)
    # elif number > 4 and number <= 8:
    #     return #to implement ammo
    # elif number > 8 and number <= 12:
    #     return # to implement grenade
    return None