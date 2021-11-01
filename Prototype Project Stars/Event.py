import random


class Event:
    def __init__(self, event_file):
        self.type_event = None
        self.atmosphere_multiplier = None
        self.landmass_multiplier = None
        self.population_health_multiplier = None
        self.population_multiplier = None
        self.disaster_list = list()
        self.breakthrough_list = list()
        self.tech_index = None
        self.title = None
        self.message = None
        with open(event_file, "r") as f:
            for line in f:
                line = list(line.rstrip().split(";"))
                if line[0] == '0':
                    self.disaster_list.append(line)
                elif line[0] == '1':
                    self.breakthrough_list.append(line)

    def generate_event(self, progression):
        temp_chance_disaster = ((progression / 1000) * 50) + 35  # the higher the progression,
        # the higher the chances of a disaster
        if (random.randint(0, 100) < temp_chance_disaster) and len(self.disaster_list) != 0:
            temp_disaster = self.disaster_list.pop(random.randint(0, len(self.disaster_list) - 1))
            x = 0
            while ((int(temp_disaster[1]) > progression) or (int(temp_disaster[2]) < progression)) and x < 100:
                self.disaster_list.append(temp_disaster)
                temp_disaster = self.disaster_list.pop(random.randint(0, len(self.disaster_list) - 1))
                x += 1
            self.type_event = int(temp_disaster[0])
            self.title = temp_disaster[3]
            self.message = temp_disaster[4]
            self.atmosphere_multiplier = float(temp_disaster[5])
            self.landmass_multiplier = float(temp_disaster[6])
            self.population_health_multiplier = float(temp_disaster[7])
            self.population_multiplier = float(temp_disaster[8])
        elif len(self.breakthrough_list) != 0:
            temp_break = self.breakthrough_list.pop(random.randint(0, len(self.breakthrough_list) - 1))
            x = 0
            while ((int(temp_break[1]) > progression) or (int(temp_break[2]) < progression)) and x < 100:
                self.breakthrough_list.append(temp_break)
                temp_break = self.breakthrough_list.pop(random.randint(0, len(self.breakthrough_list) - 1))
                x += 1
            self.type_event = int(temp_break[0])
            self.title = temp_break[3]
            self.message = temp_break[4]
            self.tech_index = int(temp_break[5])
        else:
            raise ValueError("Need more events!")

    def get_type(self):
        return self.type_event

    def get_multipliers(self):
        return [self.atmosphere_multiplier, self.landmass_multiplier, self.population_health_multiplier, self.population_multiplier]

    def get_tech_index(self):
        return self.tech_index

    def get_title(self):
        return self.title

    def get_message(self):
        return self.message

    def __repr__(self):
        return self.title + " ; " + self.message

    def __str__(self):
        return self.title + " ; " + self.message

# test = Event()
# getal = 0
# for x in range(0, 10):
#   test.generate_event(999)
#  if test.get_type() == 0:
#        getal += 1
# print(getal)
