import random
import math
import copy
from math import ceil
from Code.Planet import Planet
from Code.MainPlanet import MainPlanet
from Code.EventManager import EventManager


class StarSystem:
    """Main class that keeps all the info and planets."""
    MAX_PLANETS = 7
    MIN_PLANETS = 5
    GOLDILOCK_DISTANCE = 150_000_000  # distance in millions of kilometres
    PREGZ_RINGS = 2
    INGZ_RINGS = 3
    POSTGZ_RINGS = 6

    def __init__(self):
        self.remaining_turns = 100
        self.planets_list = []
        self.distance_list = []
        self.gz_distance_list = []  # list for goldi_distance
        self.index_of_main_planet = None
        self.set_up()
        self.event = EventManager("Events.csv")

    def set_up(self):
        """Setup, to read in all the file names, and give the planets different distances."""
        planet_names = []
        # read file with names for planets
        with open("Planets.csv", "r") as f:
            for line in f:
                line = line.rstrip()
                planet_names.append(line)
        # set up the planets
        for i in range(0, self.PREGZ_RINGS):
            self.distance_list.append((i * (0.8 / self.PREGZ_RINGS) +
                                       (random.randint(10, int(
                                           10 + (70 / self.PREGZ_RINGS))) / 100)) * self.GOLDILOCK_DISTANCE)
            # (min 0.1 -> max 0.90) * GOLDILOCK

        for i in range(0, self.INGZ_RINGS):
            self.gz_distance_list.append((i * (0.30 / self.INGZ_RINGS) +
                                          (random.randint(90, int(
                                              90 + (20 / self.INGZ_RINGS))) / 100)) * self.GOLDILOCK_DISTANCE)
            # (min 0.9 -> max 1.2) * GOLDILOCK
        for i in range(0, self.POSTGZ_RINGS):
            self.distance_list.append((i * (1.2 / self.POSTGZ_RINGS) +
                                       (random.randint(120, int(
                                           120 + 100 / self.POSTGZ_RINGS)) / 100)) * self.GOLDILOCK_DISTANCE)
            # (min 1.2 -> max 2.4) * GOLDILOCK
        goldinumber = random.randint(1, self.INGZ_RINGS)
        # number of planets in Goldilocks' zone

        for i in range(0, random.randint(self.MIN_PLANETS, self.MAX_PLANETS) - goldinumber):
            # generate random planet name
            temp_name = planet_names.pop(random.randint(0, len(planet_names) - 1))
            # generate number of planets between 5 en 7
            distance_number = random.randint(0, len(self.distance_list) - 1)
            self.planets_list.append(Planet(self.distance_list[distance_number], temp_name))
            self.distance_list.remove(self.distance_list[distance_number])  # remove elements from list
        for i in range(0, goldinumber):
            # generate random planet name
            temp_name = planet_names.pop(random.randint(0, len(planet_names) - 1))
            distance_number = random.randint(0, len(self.gz_distance_list) - 1)
            self.planets_list.append(Planet(self.gz_distance_list[distance_number], temp_name, True))
            self.gz_distance_list.remove(self.gz_distance_list[distance_number])  # remove elements from list

    def set_main_planet(self,planet):
        """"Let the star system know, what is the main planet, and put it in the correct list."""
        self.index_of_main_planet = self.planets_list.index(planet)
        self.planets_list[self.index_of_main_planet] = MainPlanet(self.planets_list[self.index_of_main_planet])

    def next_turn(self):
        """Simulate the next turn, and call all the methods to update the values."""
        res = None
        self.planets_list[self.index_of_main_planet].cache_population()
        rand_numb = random.randint(0, 3)
        if rand_numb == 0 and self.remaining_turns < 95:
            self.event.generate_event(self.planets_list[self.index_of_main_planet].progression)
            self.planets_list[self.index_of_main_planet].change_base_values(self.event)
            res = self.event
        self.planets_list[self.index_of_main_planet].update_variables()
        self.remaining_turns -= 1
        return res

    def check_winning_condition(self):
        """Check if the game is either won, or lost, depending on progression and population."""
        if self.planets_list[self.index_of_main_planet].progression >= 1000:
            return 0
        elif self.remaining_turns == 0 :
            return 1
        elif ceil(self.planets_list[self.index_of_main_planet].total_population) == 1:
            return 2
        elif ceil(self.planets_list[self.index_of_main_planet].total_population) < 1:
            return 3
        else:
            return None