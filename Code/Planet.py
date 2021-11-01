import random
import math
from math import ceil


class Planet:
    """Class that keeps basic info about and represents a planet."""
    GOLDILOCK_DISTANCE = 150_000_000

    def __init__(self, distance, name, is_gz=False):
        self.planet_name = name
        self.distance = distance
        self.radius = int((5 + self.distance / 360000000 * 15) * 1000)
        self.is_gz = is_gz
        self.atmosphere = random.randint(80 if is_gz else 1, 100 if is_gz else 40)
        self.landmass = random.randint(10, 100)

    def calc_temperature(self):  # goldi -25 - +50 # -250 - +500
        """Calculate the temperature depending on distance and atmosphere."""
        if self.distance < self.GOLDILOCK_DISTANCE:
            const = -1.0
        else:
            const = 0.5
        return (250 - (self.distance / 600000)) * (100 / self.atmosphere) if self.is_gz else 230 \
                                                                                             + 3.5 / const - const * (
            -const * self.atmosphere + 300 + (const * self.distance / 1_000_000) * 4)

    def planet_quality(self):
        """"Calculate the planet quality, depending on the temperature, atmosphere and landmass."""
        scaled_temp = 0
        temp = self.calc_temperature()
        if temp > -25 and temp < 50:
            scaled_temp = (-(temp + 35) * (temp - 65) * 0.06)
        elif temp <= -25:
            scaled_temp = math.exp((temp + 104.75) / 20)
        else:
            scaled_temp = math.exp((-temp + 136.75) / 20)
        quality = (1/3)*scaled_temp + 0.15 * self.landmass + 0.35 * self.atmosphere
        return quality

    def show_information(self):
        """Display the information of the planet, like name, radius and more useful information."""
        return {"Name of Planet:": self.planet_name, "Distance (kilometer):": ceil(self.distance),
                "Radius (kilometer):": ceil(self.radius),
                "Landmass (%):": round(self.landmass, 2),
                "Atmosphere (%):": round(self.atmosphere, 2), "Temperature (°C):": ceil(self.calc_temperature()),
                "Planet Quality (%):": round(self.planet_quality(), 2)}

    def __str__(self):
        return str(self.show_information())

    def __repr__(self):
        return str(self.show_information())
