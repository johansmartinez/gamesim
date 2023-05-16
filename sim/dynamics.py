def mrua(initial_vel, aceleration, time):
    return (initial_vel*time) + ((aceleration*(time**2)/2))

def mru(vel, time):
    return vel*time

def free_fall(gravity, time):
    return 0.5*gravity*(time**2)