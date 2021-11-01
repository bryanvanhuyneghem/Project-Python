from Prototype.Planet import Planet
from math import ceil


class MainPlanet(Planet):
    TECH_CAP = 15
    ENGINEERING_CAP = 30

    def __init__(self, planet):
        # copy-constructor for planet
        self.planet_name = planet.planet_name
        self.landmass = planet.landmass
        self.distance = planet.distance
        self.is_gz = planet.is_gz
        self.atmosphere = planet.atmosphere
        self.radius = planet.radius

        self.total_population = 100000
        self.prev_population = self.total_population
        self.population_health = 100
        self.tech_counter = 5
        self.tech_focus = None
        # self.tech_medicine -> tech_list[0]
        # self.tech_agriculture -> tech_list[1]
        # self.tech_architecture -> tech_list[2]
        # self.tech_engineering -> tech_list[3]
        self.tech_list = [4, 4, 4, 0]  # for testing
        self.atmosphere_multiplier = 1
        self.landmass_multiplier = 1
        self.population_multiplier = 1
        self.usable_landmass = self.calc_usable_landmass()
        self.calculated_atmosphere = self.atmosphere * self.atmosphere_multiplier
        self.calculated_temperature = self.calc_temperature()
        self.life_quality = self.calc_life_quality()
        self.progression = 0

    def spend_points(self, points):  # return value form GUI
        self.tech_list[0] = points[0]
        self.tech_list[1] = points[1]
        self.tech_list[2] = points[2]
        self.tech_list[3] = points[3]

    def set_research_focus(self, index):
        if self.tech_focus != index:
            self.tech_counter = 5
            self.tech_focus = index

    def update_research_focus(self):
        if self.tech_counter == 0:
            if self.tech_focus is not None:
                self.update_technologies(self.tech_focus)
                self.tech_counter = 4
        else:
            self.tech_counter -= 1

    def change_base_values(self, event):
        if event.type_event == 0:
            self.update_multipliers(event.get_multipliers())
        if event.type_event == 1:
            self.update_technologies(event.get_tech_index())

    def update_multipliers(self, multipliers):
        self.atmosphere_multiplier *= multipliers[0]
        self.landmass_multiplier *= multipliers[1]
        self.population_health *= multipliers[2]
        self.population_multiplier = multipliers[3]

    def update_technologies(self, tech_index):
        if tech_index != 3 and self.tech_list[tech_index] < self.TECH_CAP:
            self.tech_list[tech_index] += 1
        elif tech_index == 3 and self.tech_list[tech_index] < self.ENGINEERING_CAP:
            self.tech_list[tech_index] += 1

    def update_variables(self):
        # atmosphere
        self.calculated_atmosphere = self.calc_atmosphere()
        # temperature
        self.calculated_temperature = self.calc_temperature()
        # usable landmass
        self.usable_landmass = self.calc_usable_landmass()
        # population health
        if self.population_health + self.tech_list[0] >= 100:
            self.population_health = 100
        else:
            self.population_health += self.tech_list[0]
        # life quality
        self.calc_life_quality()
        # total population
        self.calc_total_population()
        # progression
        self.progression = self.calc_progression()
        self.update_research_focus()

    def calc_atmosphere(self):
        if self.atmosphere_multiplier + self.tech_list[1] / 150 >= 1:
            self.atmosphere_multiplier = 1
        else:
            self.atmosphere_multiplier += self.tech_list[1] / 150
        return self.atmosphere * self.atmosphere_multiplier

    def calc_temperature(self):  # goldi -25 - +50 # -250 - +500
        if self.distance < self.GOLDILOCK_DISTANCE:
            const = -1.0
        else:
            const = 0.5
        return (250 - (self.distance / 600000)) * (100 / self.atmosphere) if self.is_gz else 230 \
                                                                                             + 3.5 / const - const * (
            -const * self.calculated_atmosphere + 300 + (const * self.distance / 1_000_000) * 4)

    def calc_usable_landmass(self):
        from math import ceil
        tech_variable = (self.tech_list[2] * 0.5 + self.tech_list[1] * 0.5) / self.TECH_CAP
        if self.landmass_multiplier < 1:
            if self.landmass_multiplier + tech_variable / 10 >= 1:
                self.landmass_multiplier = 1
            else:
                self.landmass_multiplier += tech_variable / 10
        usable_landmass = ceil(self.landmass_multiplier * self.landmass * (tech_variable * 0.8 + 0.2))
        return usable_landmass

    def calc_life_quality(self):  # nog eens bekijken
        x = 0
        if (self.calculated_temperature > -25) and (self.calculated_temperature < 50):
            x = -(self.calculated_temperature + 25) * (
                self.calculated_temperature - 50) / 1406.25  # / number between -a and 0
            self.life_quality = ceil(((self.tech_list[3] / 6) + ((self.usable_landmass / self.landmass) * 35) + (
                ((1 - x) * self.tech_list[2] / self.TECH_CAP + x) * 30) + (self.population_health * 0.4)) * 100) / 100
        else:
            x = 0
            self.life_quality = ceil(((self.tech_list[3] / 6) + ((self.usable_landmass / self.landmass) * 35) + (
                ((1 - x) * self.tech_list[2] / self.TECH_CAP + x) * 30) + (self.population_health * 0.4)) * 100) / 100
            if self.calculated_temperature <= -25:
                self.life_quality *= 1 - (self.calculated_temperature + 25) / (
                -248)  # the lower the temperature, the worse the life quality
            else:
                self.life_quality *= 1 - (self.calculated_temperature - 50) / (
                500)  # the higher the temperature, the worse the life quality
        return self.life_quality

    def calc_total_population(self):
        if self.total_population < 5000:
            self.total_population = int(
                self.total_population + ((self.life_quality / 100) - 0.5) * 3 * self.total_population)
        elif self.total_population > 1000000000:
            self.total_population = int(
                1000000000 + ((self.life_quality / 100) - 0.5) * 1000000000 / 1.3)
        else:
            self.total_population = int(
                self.total_population + ((self.life_quality / 100) - 0.5) * self.total_population / 1.3)
        self.total_population *= self.population_multiplier
        self.population_multiplier = 1
        if self.total_population < 0:
            self.total_population = 0

    def calc_progression(self):  # use life quality or health?
        population = int(self.total_population)
        progression = 0
        if self.prev_population - population >= 0:
            progression = self.progression - (1 - (self.life_quality / 100)) * (
                (self.prev_population - population) / 250000)
            if progression < (self.progression / 1.5):
                progression = self.progression / 1.5
        else:
            if self.total_population >= 1000000:
                population = 1000000
            progression = self.progression + (self.tech_list[3] * 1 + self.tech_list[2] * 0.25 + self.tech_list[
                0] * 0.1 + ((self.life_quality / 100) - 0.5) * 10) * (population / 500000)
        if progression < 0:
            progression = 0
        if progression > 1000:
            progression = 1000
        return progression

    def get_total_population(self):
        return ceil(self.total_population)

    def show_information(self):
        return {"Name of Planet:": self.planet_name, "Distance (kilometer):": ceil(self.distance),
                "Radius (kilometer):": ceil(self.radius),
                "Usable Landmass (%):": round(self.usable_landmass, 2),
                "Atmosphere (%):": round(self.calculated_atmosphere, 2),
                "Temperature (°C):": ceil(self.calculated_temperature),
                "Life Quality (%):": round(self.life_quality, 2), "Population:": ceil(self.total_population),
                "Health (%):": round(self.population_health, 2),
                "Medicine:": str(self.tech_list[0]) + "/15", "Agriculture:": str(self.tech_list[1]) + "/15",
                "Architecture:": str(self.tech_list[2]) + "/15", "Engineering:": str(self.tech_list[3]) + "/30"}

    def get_progression(self):
        return ceil(self.progression)

    def cache_population(self):
        self.prev_population = int(self.total_population)

    def __repr__(self):
        return str(self.show_information())

    def __str__(self):
        return self.__repr__()

    """
    m = MainPlanet(150000000)
    print(m.life_quality)
    m.tech_agriculture = 4
    m.tech_architecture = 4
    m.tech_engineering = 7
    m.tech_medicine = 3
    for x in range(0,100):
        m.update_variables()
        print(m.life_quality,m.usable_landmass) """
