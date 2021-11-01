# Project Star

**Project Stars** is a _simulation_ in which an organism has to overcome the destruction of their home planet. As their star reaches its final one-thousand years, the organism’s goal is to survive the catastrophes with which its civilisation is about to be hit and manage to escape towards a new, more distant and fertile planet. 

Lift off for _Project Stars_.

### Project Stars : Introduction

Welcome to Project Stars’ Analysis and Functionality Report. Project Stars is a simulation by Bryan Van Huyneghem, Michiel Mortier, Jonathan Van Damme, Robin Goussey and Jelle Hamerlinck. This simulation was commissioned by the University of Ghent as part of the Bachelor of Science in Information Engineering Technology education programme, under the subject Multidisciplinary Engineering Project. The exact assignment stated:

_“The students have to create an application that uses a non-trivial algorithm in a Python version that exceeds version 3.0. This algorithm needs to be constructed in such a way such that it can be recycled for future work, and such that other engineers with a similar background can understand and edit the code. Furthermore, there must be enough theoretical support through Analysis and Design diagrams such that the general structure and functionality can be understood in a short period of time.”_

An estimated 90 hours work per member was expected to be spent on this project. A good chunk of this time was spent at University campus inside the classroom, though most work was done at home where the team collaborated together through Teamviewer, Skype, GitHub and Google Docs or worked individually on a person-specific task.

Within said assignment, the group quickly found common ground in our passion for games. After a short brainstorm, it was agreed that the creation of an interactive simulation of a star system was going to be the main goal. 

The central star of the system is on the brink of dying, forcing the local intelligent species on a human-controlled planet to commence a race against the clock to evacuate its population from the planet and settle on a new one. The user is in control of the decisions the species make in their final one thousand years, all the while random events will either help or hinder the progression they make to escape fate.

The algorithm creates an environment where all kinds of planet properties, species properties and technologies, and random events interact with each other. After each turn in the simulation, every change is calculated and then presented to the user through the visual interface. In this interface, the user can adjust the research focus of their species, according to what seems necessary.

This Analysis and Functionality Report offers the reader with an extensive and in-depth look at Project Stars. Chapter 1 briefly describes the concept behind the simulation, whilst Chapter 2 provides the reader with a detailed, initial analysis of the project and work to be done. Chapter 3 solidifies the functionality and mechanics behind the simulation, whilst Chapter 4 will describe how these were implemented. Lastly, conclusions are drawn in regards to the end result and future work. Appendices include a Manual of the simulation, Technical Documentation and a list of all Events.

### Project Stars: Concept

The Project Stars simulation follows the progression of an organism in its race against time and destruction. Its main goal is to escape its home planet and find a new, more distant world where its civilisation can further improve itself and continue its space quest. The organism’s final one-thousand years of civilisation before catastrophe hits, symbolises the inevitable confrontation of a race with its annihilation.

At the start of each simulation, Project Stars offers the user a star system consisting of one star and a number of planets to choose from. These planets are generated on so called planet rings, which are possible locations for planets to exist at, each at a particular distance from the system’s star. It should be noted that the Goldilocks’ Zone or GZ contains the planet rings that spawn the most optimal and easiest planets for the organism to survive on. Similar to how Earth is a planet within the GZ, these planets come with very strong and positive attributes. 

Each planet is equipped with an information panel where these attributes are listed, allowing the user to make an informed and optimal selection based on said information -- if they so choose to. The user’s planet of choice turns this planet into the Main Planet or home planet. 

Initially, a planet has (1) a distance from its star, (2) a planet radius, (3) the percentage of landmass, (4) a value indicating the quality of the atmosphere, and (5) an average surface temperature. Finally, values (3) and (5) are combined into one attribute that indicates the overall quality of the planet, which can be seen as an overall score for that planet.

It is assumed that the planet’s organism commences its journey with the technology and wisdom of a humanlike civilisation during the 17th century..

As the simulation -- and therefore the organism -- progresses, a planet will also indicate what (6) the organism’s overall health (population health) is and what (7) the total amount of living organisms (total population) is. The simulation progresses through what are called turns. One turn equals ten years, so the simulation supports a grand total of one-hundred turns before the organism’s time runs out.

The organism has access to four technologies: agriculture, medicine, architecture and engineering. The user is allowed to spend a total of twelve points in the first three technologies to boost the initial values. These will further increase as the user’s organism progresses throughout the simulation to a cap of fifteen for the first three technologies and a cap of thirty for engineering.

Technologies play a major role in the survivability of the organism, as they will directly influence the susceptibility of the organism to disasters. The organism is allowed to research passively into one technology at a time, as such generating one point per five turns. Furthermore, they influence the life quality, which is a grand total of the usable landmass, average surface temperature and population health.

Disasters are one of two, the other one being Breakthroughs, simulation mechanics that are part of the Events. An event is Project Stars approach to simulate reality by adding the randomness and unpredictability of daily life. Disasters have negative effects on the planet and organism, whilst Breakthroughs have positive effects. Both of them appear in wide variety and the frequency and gravity depend on how long your organism has been alive for. A full list of all disasters and all breakthroughs with their corresponding effects can be found in Appendix C.

The ultimate goal of the simulation is to escape the organism’s home planet within one-thousand years. This can be achieved by reaching a progression of 1,000. Progression is the simulation’s way of showing the user how advanced the organism has become. It is based on the amount of organisms alive – and therefore the life quality – and the engineering technology.

### Definition list for Project Stars

1.	**Agriculture**: Agriculture is one of four technologies and aids the organism in their combat against disasters such as diseases and famine. Agriculture indirectly influences the quality of life of an organism.
2.	**Architecture**: Architecture is one of four technologies and aids the organism in their combat against disasters such as natural disasters. Architecture indirectly influences the quality of life of an organism.
3.	**Atmosphere**: The atmosphere of a planet determines how well the composition is suited for the organism and, combined with distance, they play a vital role in determining a planet’s temperature.
4.	**Attribute**: An attribute is a characteristic for a planet or organism. Attributes are collected and displayed as a whole in the information panel.
5.	**Breakthrough**: A breakthrough is part of the mechanic events and is Project Stars approach to simulate reality by adding the randomness and unpredictability of daily life. Breakthroughs have positive effects on the planet and organism. They appear in a wide variety and their frequency and gravity depend on how many turns have passed.
6.	**Cap**: The highest amount of technology points an organism can own. This cap is set at 15 for the technologies agriculture, architecture and medicine, and is set at 30 for the technology engineering.
7.	**Disaster**: A disaster is part of the mechanic events and is Project Stars approach to simulate reality by adding the randomness and unpredictability of daily life. Disasters have negative effects on the planet and organism. They appear in a wide variety and their frequency and gravity depend on how many turns have passed.
8.	**Distance (from star)**: The distance between a planet and a star is set by Project Stars to be between 15,0000,000 km and 360,000,000 km.
9.	**Engineering**: Engineering is one of four technologies and aids the organism in their combat against disasters. Engineering directly influences the quality of life of an organism and is a major component of the progression mechanic.
10.	**Event**: An event is Project Stars approach to simulate reality by adding the randomness and unpredictability of daily life. Events can occur as being beneficial or harmful to the planet and organism, the former being a breakthrough and latter being a disaster. A full list of all disasters and all breakthroughs with their corresponding effects can be found at **TBA**.
11.	**Goal**: The user’s organism has successfully survived and reached another planet, if and only if it reaches a progression of 1000.
12.	**GZ** _or_ **Goldilocks’ Zone**: The Goldilocks’ Zone -- or in short GZ -- is a zone at a set distance from its star that has (easy) optimised planet attributes for an organism’s survival. Project Stars’ GZ starts at 135 million km and ends at 180 million km, with its centre set at 150 million km.
13.	**Home Planet** _or_ **Main Planet**: The single planet that is inhabited by the organism whom is trying to escape said planet and near-imminent destruction.
14.	**Information Panel**: The information panel collects and displays all attributes for a planet. The main planet displays its own attributes as well as its organism’s attributes.
15.	**Landmass**: The landmass of a planet is a value between 10 and 100, and is defined as the percentage of land on a planet. The complement of landmass would be the percentage of water on the planet. Landmass is one of the planet attributes that is used to calculate the usable landmass of a planet.
16.	**Landmass (usable)**: The amount of usable landmass of a planet is a percentage value calculated through the total landmass of a planet, the technology level in agriculture and the technology level in architecture.
17.	**Main Planet** _or_ **Home Planet**: The single planet that is inhabited by the organism whom is trying to escape said planet near-imminent destruction.
18.	**Mechanic**: A mechanic is a construct of rules or methods designed for interaction with the simulation, thus providing progression throughout said simulation. Different theories and styles with relation to the mechanic differ as to their ultimate importance in the simulation.
19.	**Medicine**: Medicine is one of four technologies and aids the organism in their combat against disasters such as diseases. Medicine directly influences the regeneration of the population health of an organism and indirectly influences the quality of life of said organism.
20.	**Multiplier**: A multiplier is a factor that is multiplied with a planet attribute, such as usable landmass, or an organism attribute such as population health or total population to either increase or decrease said attributes. 
21.	**Organism**: The organism is the key ingredient in the simulation and is what progresses during one-thousand years to escape its home planet. It is hindered by disasters and aided by breakthroughs. User choice also impacts the organism's well-being (see more at: population health and quality of life).
22. **Planet**: A planet is part of the star system and has five characteristics or attributes that define what it is like: its (1) planet name, (2) distance, (3) atmosphere, (4) landmass, (5) temperature and its (6) planet quality.
23. **Planet Quality**: The quality of a planet is a value (score) between 0 and 100 that indicates how well-suited a planet is to be inhabited by an organism. It is initially presented to the user in an effort to guide them in their (easy) selection of a main planet. The quality of a planet is determined by the amount of landmass and its average surface temperature (which is determined through distance and planet radius).
24.	**Population (health)**: The population health (0-100) of an organism is an indicator for its well-being and its regeneration is dependent on the technology level in medicine. It is possibly negatively affected by the health multiplier as a result of disasters. Population health is visually represented by a keyword that is determined as followed: 100-70: Healthy, 70-40: Average health, <40: Bad health.
25.	**Population (total)**: The total population of the organism is the total amount of species of said organism that are living on the main planet.
26.	**Progression**: The progression mechanic is what indicates the organism’s level of sophistication on a scale of 0 to 1000 and is what ultimately leads to the organism’s escape from its home planet -- in other words the successful finalisation of the simulation. If the population is not on the decline, the progression is dependent on the technology level in medicine, architecture, engineering,  life quality and the total population. However, in a scenario where population has decreased in relation to the previous turn, progression is dependent on life quality and the difference in population between this turn and the previous. Progression is visualised as a progression bar that tells the user what the total progression is and how much progression will be gained or lost upon ending the current turn.
27.	**Quality of Life**: The quality of life (also referred to as life quality) is the combination of the usable landmass, average surface temperature, population health and the technology level in engineering. This life quality is a factor that is used to calculate the total population for the organism. 
28.	**Radius (planet)**: The radius of a planet affects the total area of the planet and therefore the maximum possible value for the amount of (usable) landmass. It is determined through the distance of the planet to its star.
29.	**Research (focus)**: An organism’s research is a way to passively gain points in a particular technology each x amount of turns.
30.	**Rings (planet)**: A planet ring is a possible location for a planet around its star. Project Stars has a set total of eleven rings that it chooses at random distances from the star, but allows for expandability for even more rings. The user is guaranteed to have at least 3 rings (or possible planet locations) in the GZ.
31.	**Simulation**: Project Stars is a simulation that shows the user’s organism’s star system and the progression that is made by the organism towards its ultimate goal.
32.	**Star**: The star system’s star is the organism’s driving force before behind the reasoning to escape its planet. In precisely one-thousand years, it will engulf the planet in massive amounts of solar winds and solar radiation, annihilating anything that lives.
33.	**Star System**: A star system is the world in which the simulation takes place. It contains a single, near-death star and a number of planets between 5 and 7.
34.	**Technology**: Technology is the mechanic that protects the organism from complete annihilation. There are four technologies: agriculture, architecture, medicine and engineering (see more at: medicine, agriculture, architecture, engineering). At the start of the simulation, the user is allowed twelve points which can be spent on the three first technologies to their heart’s content. Technology can be advanced passively via the mechanic research focus every x amount of turns or via a Breakthrough. 
35.	**Temperature (surface)**: The surface temperature of a planet in °C is defined per formula using the distance between star and planet, and the planet’s atmosphere quality.
36.	**Turn**: Project Stars limits the amount of turns to 100, which means that each turn is equal to exactly 10 years. A turn is the mechanic of continuing in the simulation and progressing through the one-thousand final years that the organism has to escape its home planet.
37.	**User**: The user is the person who chooses the main planet, spends the initial twelve technology points and takes critical decisions before, during and after disasters and breakthroughs which both alter the progression speed of the organism through technologies.

