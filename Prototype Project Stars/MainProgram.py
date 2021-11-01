import random
import math
import copy
from math import ceil
from Prototype.Planet import Planet
from Prototype.MainPlanet import MainPlanet
from Prototype.Event import Event


class StarSystem:
    MAX_PLANETS = 7
    MIN_PLANETS = 5
    GOLDILOCK_DISTANCE = 150_000_000  # distance in millions of kilometres
    PREGZ_RINGS = 2
    INGZ_RINGS = 3
    POSTGZ_RINGS = 6

    def __init__(self):
        self.remaining_turns = 100
        self.current_turn = 1
        self.planets_list = []
        self.distance_list = []
        self.gz_distance_list = []  # list for goldi_distance
        self.index_of_main_planet = None
        self.set_up()
        self.show_planets()
        self.event = Event("Events.csv")
        self.set_main_planet()

    def set_up(self):
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

    def show_planets(self):
        # draw planet system
        for x in self.planets_list:
            print("Planet " + str(self.planets_list.index(x) + 1) + ": ")
            print(x)

            # def show_planet(self):
            # info per planet

    def set_main_planet(self):  # In gui: user clicks on planet and sees info; options: return or select as main planet
        selection = True
        while selection:
            s = int(input("Please enter your planet number of choice: ")) - 1
            if s <= len(self.planets_list):
                selection = False
                self.index_of_main_planet = s
                self.planets_list[self.index_of_main_planet] = MainPlanet(self.planets_list[self.index_of_main_planet])
                print("\nYou have selected planet number: " + str(s + 1) + "\n" + "Main Planet: " + str(
                    self.planets_list[s]))
            else:
                print("This is not a valid planet. Select a valid planet number.")

    def next_turn(self):
        print("\nTurn: " + str(self.current_turn))
        if self.current_turn == 1:
            self.planets_list[self.index_of_main_planet].set_research_focus(int(input("Set a technology "
                        "(0: Medicine, 1: Architecture, 2: Agriculture as, 3: Engineering) as a Research Focus: ")))
        elif self.current_turn != 1 and self.current_turn < 100:
             if input("set new research focus? (y)") == "y":
                 self.planets_list[self.index_of_main_planet].set_research_focus(int(input("Which technology?")))
        self.planets_list[self.index_of_main_planet].cache_population()
        rand_numb = random.randint(0, 3)
        if rand_numb == 0 and self.remaining_turns < 95:
            self.event.generate_event(self.planets_list[self.index_of_main_planet].get_progression())
            self.planets_list[self.index_of_main_planet].change_base_values(self.event)
            print(self.event)
        self.planets_list[self.index_of_main_planet].update_variables()
        print(self.planets_list[self.index_of_main_planet])
        self.remaining_turns -= 1
        self.current_turn += 1
        return self.check_winning_condition()

    def check_winning_condition(self):
        if self.planets_list[self.index_of_main_planet].get_progression() >= 1000:
            return "Won! Your progression: " + str(
                self.planets_list[self.index_of_main_planet].get_progression()) + " ---- Population: " + str(
                self.planets_list[self.index_of_main_planet].get_total_population())
        elif self.remaining_turns == 0 or ceil(self.planets_list[self.index_of_main_planet].get_total_population()) <= 1:
            return "Lost. Your progression: " + str(
                self.planets_list[self.index_of_main_planet].get_progression()) + " ---- Population: " + str(
                self.planets_list[self.index_of_main_planet].get_total_population())
        else:
            return None

#Below is a test:

Star = StarSystem()
test = Star.next_turn()
while test is None:
    test = Star.next_turn()
print(test)

