import math

def violated_drones(drones):
    violated = []
    for drone in drones:
        distance = math.sqrt(drone["x"]**2 + drone["y"]**2)
        if distance < 1000:
            violated.append(drone)
    return violated