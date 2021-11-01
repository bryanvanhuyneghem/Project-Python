import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkf
import math
from Code.StarSystem import StarSystem as ss
import random
import threading
import time
import pygame
import pickle
from PIL import Image, ImageTk
import os

LARGE_FONT = ("Verdana", 11)


class Application(tk.Tk):
    """The class Application is the main application of the class."""
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(0, 0)
        self.title("Project Stars - A simulation")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)  # fill vult de volledig plaats
        pygame.init()
        pygame.mixer.init()  # sound
        # menu bovenaan
        self.menu = tk.Menu(self.container)
        self.config(menu=self.menu)
        self.submenu = tk.Menu(self.menu, tearoff=0)  # menu in menu
        self.submenu2 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.submenu)
        self.submenu.add_command(label="Save", command=lambda: self.save_file(self.start.StarSystem), state="disabled")
        self.submenu.add_command(label="Load", command=lambda: self.load_file(self.start))
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=lambda: self.destroy())
        self.menu.add_cascade(label="Options", menu=self.submenu2)
        self.mute_sounds_var = tk.IntVar()
        self.submenu2.add_checkbutton(label="Mute Sounds", variable=self.mute_sounds_var)
        self.mute_music_var = tk.IntVar()
        self.submenu2.add_checkbutton(label="Mute Music", variable=self.mute_music_var)

        self.start = MainPage(self.container, self)
        self.start.grid(row=0, column=0, sticky="nesw")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)  # x -> window to close
        self.end = None
        self.begin_screen = None
        self.start_startscreen()
        # thread for music
        self.t2 = threading.Thread(target=self.update_music, args=())
        self.t2.daemon = 1
        self.t2.start()

    def update_music(self):
        """Play the music, this can be muted."""
        while True:
            if self.mute_music_var.get() == 0:
                pygame.mixer.music.unpause()
            elif self.mute_music_var.get() == 1:
                pygame.mixer.music.pause()
            time.sleep(1)

    def start_startscreen(self):
        """Show the start screen."""
        self.submenu.entryconfig("Load", state="disabled")
        self.begin_screen = StartPage(self.container, self)
        self.begin_screen.grid(row=0, column=0, sticky="nesw")
        self.begin_screen.tkraise()

    def start_simulation(self):
        """Show the simulation panel."""
        del self.start
        self.start = MainPage(self.container, self)
        self.start.grid(row=0, column=0, sticky="nesw")
        self.start.tkraise()
        if os.path.isfile("save_file.pkl") is True:
            self.submenu.entryconfig("Load", state=tk.NORMAL)
        else:
            self.submenu.entryconfig("Load", state=tk.DISABLED)
        del self.end

    def load_simulation(self):
        """Load the start screen from a previous simulation."""
        if messagebox.askyesno("Loading", "Do you want to load your save file?"):
            del self.start
            self.start = MainPage(self.container, self)
            self.start.grid(row=0, column=0, sticky="nesw")
            self.start.tkraise()
            self.submenu.entryconfig("Load", state="normal")
            with open("save_file.pkl", "rb") as input:
                StarSystem = pickle.load(input)
                self.start.load_startpage(StarSystem)

    def save_file(self, ss):
        """Save the current simulation."""
        if messagebox.askyesno("Saving", "Do you want to overwrite your save file?"):
            with open("save_file.pkl", "wb") as output:
                pickle.dump(ss, output)
            self.submenu.entryconfig("Load", state="normal")

    def end_frame(self, index, information):
        """Show the appropriate end screen."""
        self.end = EndPage(self.container, self, index, information)
        self.end.grid(row=0, column=0, sticky="nesw")
        self.end.tkraise()

    def load_file(self, frame):
        """Load the StarSystem object from the save file."""
        if messagebox.askyesno("Loading", "Do you want to load your save file?"):
            with open("save_file.pkl", "rb") as input:
                StarSystem = pickle.load(input)
                frame.load_startpage(StarSystem)

    def enable_save_file(self, x):
        """Enable the save button."""
        if x == 0:
            self.submenu.entryconfig("Save", state="normal")
        else:
            self.submenu.entryconfig("Save", state="disabled")

    def window_size(self, width, height):
        """Sets the size of the window."""
        self.geometry('{0}x{1}-{2}+0'.format(width, height, int((self.winfo_screenwidth() - width) / 2)))

    def on_exit(self):
        """Is called upon closure."""
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.destroy()


class StartPage(tk.Frame):
    """This class is the start window."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.title_font = tkf.Font(family="Verdana", size=18, weight=tkf.BOLD)
        self.update()
        self.picture = Image.open("Images\\title_screen_image_title.jpg").resize(
            (self.parent.winfo_width(), self.parent.winfo_height())
        )
        self.picture = ImageTk.PhotoImage(self.picture)
        self.picture_lbl = tk.Label(self, image=self.picture)
        self.picture_lbl.image = self.picture
        self.picture_lbl.place(x=0, y=0)
        self.btn_start = ttk.Button(self, text="Start", command=lambda: self.controller.start_simulation())
        self.btn_start.place(anchor="c", relx=.30, rely=.45)
        self.btn_start = ttk.Button(self, text="Load", command=lambda: self.controller.load_simulation())
        self.btn_start.place(anchor="c", relx=.30, rely=.50)
        if os.path.isfile("save_file.pkl") is False:
            self.btn_start.config(state=tk.DISABLED)
        self.btn_start = ttk.Button(self, text="Exit", command=lambda: self.controller.on_exit())
        self.btn_start.place(anchor="c", relx=.30, rely=.55)
        r = random.randint(0, 1000)
        pygame.mixer.init()
        if r == 999:
            pygame.mixer.music.load("Sounds\start_screen_special_music.wav")  # ;) you're welcome
        else:
            pygame.mixer.music.load("Sounds\interstellar_do_not_go_gentle.wav")
        pygame.mixer.music.play(loops=-1)


class MainPage(tk.Frame):
    """This is the class with all other canvasses and objects."""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # , background="blue"
        # choose background image
        self.background_image = tk.PhotoImage(file="Images\Space_goldilock.png")
        self.parent = controller
        self.controller = controller

        self.StarSystem = ss()
        # linker en rechter frame aanmaken
        self.frm_left = tk.Frame(self)
        self.frm_left.grid(row=0, column=0, sticky="n")
        self.frm_right = tk.Frame(self)
        self.frm_right.grid(row=0, column=1, sticky="n")

        # frame met knoppen voor focus aanmaken
        self.frm_btn = tk.Frame(self.frm_right, background="red")
        self.frm_btn.grid(row=0, column=0, sticky="ne")  # frame in frame!
        self.btn_text = ["Medicine", "Agriculture", "Architecture", "Engineering"]
        self.btn_list = []
        for i in range(0, len(self.btn_text)):
            self.btn_list.append(ttk.Button(self.frm_btn, text="{0}".format(self.btn_text[i]), width=14,
                                            command=lambda i=i: self.research_focus(i), state=tk.DISABLED))
            self.btn_list[i].grid(row=0, column=i)

        # thread
        self.t1 = threading.Thread(target=self.update_canvas, args=())
        self.t1.daemon = 1
        # thread for auto run
        self.t3 = threading.Thread(target=self.auto_update_turn, args=())
        self.t3.daemon = 1
        self.auto_update = False

        # make progression label
        self.lbl_progression = tk.Label(self.frm_left, text="Progression = 0/1000", font=LARGE_FONT)
        self.lbl_progression.grid(row=1, sticky="w")
        self.prev_progression = 0
        self.lbl_year = tk.Label(self.frm_left, text="Year : ????", font=LARGE_FONT)
        self.lbl_year.grid(row=1, column=1, sticky="e")
        self.year = 1600 + (100 - self.StarSystem.remaining_turns) * 10

        # canvas for drawing planets
        self.planet_drawings = []
        self.circles_drawings = []
        image = Image.open("Images\Star.png")
        image = image.resize((31, 31))
        self.sun = ImageTk.PhotoImage(image)
        self.var_pb = tk.IntVar(self)
        self.canv = self.create_canvas()

        # Event message box
        self.lbl_title_text = None
        self.lbl_body_text = None
        self.message_window = self.create_message_window()
        self.instruction_path(0)

        # info planet
        self.frm_planet_info = self.create_info_frame_planet(self.StarSystem.planets_list[0].show_information())

        # next turn button
        self.btn_auto_next_turn = ttk.Button(self.frm_right, text="Auto Next Turn", state=tk.DISABLED, width=15)
        self.btn_auto_next_turn.grid(row=2, column=0, sticky="w")
        self.btn_auto_next_turn.config(command=lambda: self.auto_update_change())
        self.btn_next_turn = ttk.Button(self.frm_right, text="Start", state=tk.DISABLED, width=15)
        self.btn_next_turn.grid(row=2, column=0, sticky="e")
        self.btn_next_turn.config(command=lambda: self.next_turn())
        self.first_press = True

        # create progression_bar
        self.progression_bar = self.create_progressbar()

        self.frm_left.update()
        self.frm_right.update()
        controller.window_size(self.frm_right.winfo_width() + self.frm_left.winfo_width(),
                               self.frm_left.winfo_height())
        # remember old info
        self.prev_info_MainPlanet = None

        pygame.mixer.init()
        pygame.mixer.music.load("Sounds\Space_planets.wav")
        pygame.mixer.music.play(loops=-1)

        # remember main planet
        self.main_planet = None

        self.t3.start()

    def load_startpage(self, ss):  # methode voor het laden van de file
        """Load the start page."""
        self.StarSystem = ss  # StarSystem updaten
        # make progression label
        self.progression_label = tk.Label(self.frm_left, text=(
            "Progression = ", self.StarSystem.planets_list[self.StarSystem.index_of_main_planet].progression, "/1000"),
                                          font=LARGE_FONT)
        # clear old planets and make a canvas for drawing new ones
        self.planet_drawings = []
        self.circles_drawings = []
        # remember main planet
        self.main_planet = self.StarSystem.planets_list[self.StarSystem.index_of_main_planet]
        self.create_canvas()
        # create progression_bar
        self.progression_bar = self.create_progressbar()
        # retrieve progression and update it
        self.var_pb = int(self.main_planet.progression)
        self.lbl_progression.config(text="Progression = {0}/1000".format(self.var_pb))
        self.progression_bar.config(value=self.var_pb)
        self.year = 1600 + (100 - self.StarSystem.remaining_turns) * 10
        self.lbl_year = tk.Label(self.frm_left, text="Year : {0}".format(self.year), font=LARGE_FONT)
        self.lbl_year.grid(row=1, column=1, sticky="e")
        # update general info about the planet
        self.frm_planet_info = self.create_info_frame_planet(self.main_planet.show_information(), True)
        self.update_info_frame_label(self.main_planet.show_information())
        # set the color of the main planet to green
        self.planet_drawings[self.StarSystem.index_of_main_planet].change_color(self.planet_color())
        # enable all the buttons, except for the tech which is currently being researched
        for btn in self.btn_list:
            btn.config(state=tk.NORMAL)
        self.btn_list[self.StarSystem.planets_list[self.StarSystem.index_of_main_planet].tech_focus].config(
            state=tk.DISABLED)
        # enable the "next turn" button
        self.btn_next_turn.config(text="Next turn", state="normal")
        # enable button fast forward
        self.btn_auto_next_turn.config(state=tk.NORMAL)
        # announce that the file has been successfully loaded
        self.show_message_window("Instructions", "We are pleased to announce that your file has loaded with succes!")
        # start music
        pygame.mixer.init()
        pygame.mixer.music.load("Sounds\Space.wav")
        pygame.mixer.music.play(loops=-1)
        # update the canvas
        try:
            self.update_canvas()
        except:
            print("")

    def research_focus(self, index):
        """Enable all buttons except the current focus"""
        if not self.t1.is_alive():
            self.instruction_path(3)
        for button in self.btn_list:
            button.config(state=tk.NORMAL)
        self.btn_list[index].config(state=tk.DISABLED)
        self.main_planet.set_research_focus(index)

    def create_canvas(self):
        """Create window to draw figures on."""
        canv = tk.Canvas(self.frm_left, width=800, height=720)
        canv.grid(row=0, column=0, columnspan=2, sticky="w")
        canv.update()
        canv.create_image(400, 360, image=self.background_image)  # set background image
        canv.create_image(canv.winfo_width() / 2 + 1, canv.winfo_height() / 2 + 1,
                          image=self.sun)
        # This is old code in case of emergency
        # create_oval(canv.winfo_width() / 2 - 20, canv.winfo_height() / 2 - 20,
        #                             canv.winfo_width() / 2 + 20,
        #                             canv.winfo_height() / 2 + 20, tags='figuur')
        self.show_planets(canv, self.StarSystem.planets_list)
        return canv

    def thread_make(self):
        """create a thread for drawing the planets."""
        self.frm_planet_info.grid()
        self.t1.start()

    def show_planets(self, obj, planets):
        """Make new PlanetDrawing objects who draw themselves."""
        angle_list = self.get_random_angle(len(planets))
        for i, planet_obj in enumerate(planets):
            planet_draw = PlanetDrawing(self, obj, planet_obj, angle_list[i])
            self.planet_drawings.append(planet_draw)

    def get_random_angle(self, number):
        """Generate number of angles who differ 20 degree with the others."""
        angle_list = []
        angle = None
        for i in range(0, number):
            found = True
            while found:
                angle = random.randint(0, 359)
                found = False
                for a in angle_list:
                    if angle - 10 < a < angle + 10:
                        found = True
                        break
            angle_list.append(angle)
        return angle_list

    def update_canvas(self):
        """Make planets move."""
        while True:
            for planet in self.planet_drawings:
                planet.move_obj()
                self.canv.update()
            time.sleep(0.05)

    def auto_update_turn(self):
        """Automatically increase turns"""
        while True:
            if self.auto_update is True:
                self.next_turn()
            time.sleep(2.5)

    def auto_update_change(self):
        """Change state when button is pressed."""
        if self.auto_update is False:
            self.btn_auto_next_turn.config(text="Stop")
            self.btn_next_turn.config(state=tk.DISABLED)
            self.auto_update = True
        else:
            self.btn_auto_next_turn.config(text="Auto Next Turn")
            self.btn_next_turn.config(state=tk.NORMAL)
            self.auto_update = False

    def create_progressbar(self):
        """Create the progressbar."""
        progression_bar = ttk.Progressbar(self.frm_left, length=self.canv.winfo_width(), maximum=1000,
                                          variable=self.var_pb,
                                          orient=tk.HORIZONTAL, mode='determinate')
        progression_bar.grid(row=2, column=0, columnspan=2, sticky="w")
        return progression_bar

    def create_message_window(self):
        """Create message window. Used for communication with user."""
        #  venster met events
        # aanmaak window frame
        frm_window = tk.Frame(self.frm_right, width=150, height=15)  # , background="red"
        frm_window.grid(row=1, column=0, sticky="nesw")
        frm_window.propagate(0)
        #  font aanmaken
        font = tkf.Font(family="Verdana", size=12, underline=1)

        # text labels for title and body text
        self.lbl_title_text = tk.Label(frm_window, font=font, width=35)
        self.lbl_title_text.grid(row=0, column=0, sticky="ns", pady=(30, 0))
        self.lbl_body_text = tk.Label(frm_window, wraplength=300, justify=tk.LEFT, font=LARGE_FONT)
        self.lbl_body_text.grid(row=1, column=0, columnspan=2, sticky="nesw")

        # exit button message window
        btn_exit = tk.Button(frm_window, text="X", bg="grey", command=lambda: self.message_window.grid_remove())
        btn_exit.grid(row=0, column=1, sticky="ne", pady=(30, 0))

        # vaste grote -> tegen verspringen andere grid rijen eronder
        self.frm_right.rowconfigure(1, minsize=200)
        return frm_window

    def show_message_window(self, title, body_text):
        """Show message window. Used for communication with user."""
        self.message_window.grid()
        self.lbl_title_text.config(text=title)
        self.lbl_body_text.config(text=body_text)

    def create_info_frame_planet(self, startinfo, main=False):
        """Show planet information, if MainPlanet set, only this information will be shown."""
        size = len(startinfo.keys()) + 1
        if not main:
            size = len(startinfo.keys()) + 1
        frame_size = 30 * size
        frm_info = tk.Frame(self.frm_right, width=self.frm_btn.winfo_width(), height=frame_size)  # , bg="red"
        frm_info.grid(row=3, column=0, sticky="w")
        frm_info.grid_propagate(0)  # autosize afzetten
        frm_info.update()
        frm_info.columnconfigure(0, minsize=self.frm_btn.winfo_width())
        space = frm_info.winfo_height() / size
        i = 0
        self.lbl_list = []
        if main:
            i = 1
            self.lbl_list.append(
                tk.Label(frm_info, text="Turns left: {0}".format(self.StarSystem.remaining_turns), padx=20,
                         font=LARGE_FONT))  # , bg="green"
            self.lbl_list[0].grid(row=0, sticky="nws")
            frm_info.rowconfigure(0, minsize=space)
        for key, value in startinfo.items():
            self.lbl_list.append(
                tk.Label(frm_info, text="{0} {1}".format(key, value), padx=20, font=LARGE_FONT))  # , bg="green"
            self.lbl_list[i].grid(row=i, sticky="nws")
            frm_info.rowconfigure(i, minsize=space)
            i = i + 1
        if not main:
            self.btn_set_main_planet = ttk.Button(frm_info,
                                                  text="Click here to select this planet as your main planet.")
            self.btn_set_main_planet.grid(row=i, sticky="nwes")
        else:
            self.update_info_frame_label(startinfo)
        frm_info.grid_remove()
        return frm_info

    def update_info_frame_label(self, startinfo, planet=None):
        """Update the information labels."""
        self.frm_planet_info.grid()
        i = 1
        if planet is None:
            self.lbl_list[0].config(text="Turns left: {0}".format(self.StarSystem.remaining_turns))
            for key, value in startinfo.items():
                if self.prev_info_MainPlanet is None:
                    self.prev_info_MainPlanet = startinfo
                    self.lbl_list[i].config(text="{0}  {1}".format(key, value))
                else:
                    if i < 5 or i > 10:
                        if isinstance(value, str):
                            self.lbl_list[i].config(text="{0}  {1}".format(key, value))
                        else:
                            self.lbl_list[i].config(text="{0}  {1:,}".format(key, value))
                        self.lbl_list[i].config(foreground="Black")
                    else:
                        tussen = value - self.prev_info_MainPlanet.get(key)
                        if tussen > 0:
                            self.lbl_list[i].config(text="{0}  {1:,} (+{2:,})".format(key, value, round(tussen, 2)))
                            self.lbl_list[i].config(foreground="Green")
                        elif tussen < 0:
                            self.lbl_list[i].config(text="{0}  {1:,} ({2:,})".format(key, value, round(tussen, 2)))
                            self.lbl_list[i].config(foreground="Red")
                        else:
                            self.lbl_list[i].config(text="{0}  {1:,} (––)".format(key, value))
                            self.lbl_list[i].config(foreground="Black")
                i = i + 1
            self.prev_info_MainPlanet = startinfo
        else:
            i = 0
            for key, value in startinfo.items():
                if isinstance(value, str):
                    self.lbl_list[i].config(text="{0}  {1}".format(key, value))
                else:
                    self.lbl_list[i].config(text="{0}  {1:,}".format(key, value))
                i = i + 1
        if planet is not None:
            self.btn_set_main_planet.config(command=lambda: self.set_main_planet(planet))

    def set_main_planet(self, planet):
        """Remember the main planet and asks for points set."""
        self.update()
        result = tk.messagebox.askquestion("Main planet selection",
                                           "Are you sure you want to set this planet as your main planet throughout the "
                                           "simulation?")
        if result == 'yes':
            self.btn_set_main_planet.config(state=tk.DISABLED)
            self.instruction_path(1)
            self.StarSystem.set_main_planet(planet)
            self.main_planet = self.StarSystem.planets_list[self.StarSystem.index_of_main_planet]
            d = MyPopupWindow(self)
            self.controller.submenu.entryconfig("Load", state="disabled")
            self.controller.submenu.entryconfig("Exit", state="disabled")
            self.wait_window(d.top)
            if os.path.isfile("save_file.pkl") is True:
                self.controller.submenu.entryconfig("Load", state="normal")
            self.controller.submenu.entryconfig("Exit", state="normal")
            self.btn_set_main_planet.grid_forget()
            self.instruction_path(2)
            self.main_planet.spend_points(d.getallen)
            self.frm_planet_info = self.create_info_frame_planet(self.main_planet.show_information(), True)
            self.planet_drawings[self.StarSystem.index_of_main_planet].change_color(self.planet_color())

    def next_turn(self):
        """Generate next turn."""
        if self.main_planet is not None:
            if self.StarSystem.check_winning_condition() is None:
                if self.first_press is False:
                    event = self.StarSystem.next_turn()
                    if event is not None:
                        self.show_message_window(event.title, event.message)
                        if event.sound is not "" and self.parent.mute_sounds_var.get() == 0:
                            sound = pygame.mixer.Sound("Sounds\\" + event.sound + ".wav")
                            sound.play()
                else:
                    self.first_press = False
                if not self.t1.is_alive():
                    self.instruction_path(4)
                self.year = 1600 + (100 - self.StarSystem.remaining_turns) * 10
                self.lbl_year.config(text="Year : {0}".format(self.year))
                self.update_info_frame_label(self.main_planet.show_information())
                self.var_pb = int(self.main_planet.progression)
                tussen = self.var_pb - self.prev_progression
                if tussen is 0:
                    self.lbl_progression.config(text="Progression = {0}(––)/1000".format(self.var_pb))
                elif tussen > 0:
                    self.lbl_progression.config(text="Progression = {0}(+{1})/1000 ".format(self.var_pb, tussen))
                else:
                    self.lbl_progression.config(text="Progression = {0}({1})/1000 ".format(self.var_pb, tussen))
                self.progression_bar.config(value=self.var_pb)
                self.prev_progression = self.var_pb
                self.planet_drawings[self.StarSystem.index_of_main_planet].change_color(self.planet_color())
            if self.StarSystem.check_winning_condition() is not None:
                self.parent.enable_save_file(1)
                self.auto_update = False
                self.btn_auto_next_turn.config(state=tk.DISABLED)
                self.btn_next_turn.config(state=tk.NORMAL, text="Go To Endscreen",
                                          command=lambda: self.controller.end_frame(
                                              self.StarSystem.check_winning_condition(), self.main_planet))
                self.controller.submenu.entryconfig("Load", state="disabled")

    def planet_color(self):
        """Create color code."""
        color = self.main_planet.life_quality
        return "#{0:02x}{1:02x}00".format(int((100 - color) * 2.55), int(color * 2.55))

    def instruction_path(self, x):
        """Show instructions to guide the user."""
        if x == 0:
            self.show_message_window("Instructions",
                                     "Click on a planet to see its attributes.\nPlease choose a main planet. ")
        elif x == 1:
            self.show_message_window("Instructions", "Spend 12 points in these technologies.")
        elif x == 2:
            pygame.mixer.init()
            pygame.mixer.music.load("Sounds\Space.wav")
            pygame.mixer.music.play(loops=-1)
            self.show_message_window("Instructions", "Set a Research Focus using the buttons in the top-right corner.")
            for btn in self.btn_list:
                btn.config(state=tk.NORMAL)
        elif x == 3:
            self.show_message_window("Instructions", "Press the start button to begin the simulation.")
            self.btn_next_turn.config(state=tk.NORMAL)
        elif x == 4:
            self.thread_make()
            self.btn_auto_next_turn.config(state=tk.NORMAL)
            self.btn_next_turn.config(text="Next turn")
            self.show_message_window("Instructions",
                                     "Your species have {} turns to reach the progression of 1000. Good luck!".format(
                                         self.StarSystem.remaining_turns))
            self.parent.enable_save_file(0)


class PlanetDrawing:
    """Class object who contains the planet drawing and the rotation ring."""

    def __init__(self, parent, canv, planet, angle):
        self.angle = angle
        self.parent = parent
        self.planet = planet
        self.canv = canv
        self.distance_from_sun_draw = planet.distance / 1000000
        self.radius = int(planet.radius / 1000)
        self.circle_drawing = canv.create_oval(canv.winfo_width() / 2 - self.distance_from_sun_draw,
                                               canv.winfo_height() / 2 - self.distance_from_sun_draw,
                                               canv.winfo_width() / 2 + self.distance_from_sun_draw,
                                               canv.winfo_height() / 2 + self.distance_from_sun_draw, outline="white")
        self.planet_draw = canv.create_oval(0, self.radius, self.radius, self.radius * 2, fill="red")
        bounds = canv.bbox(self.planet_draw)  # returns a tuple like (x1, y1, x2, y2)
        self.width = bounds[2] - bounds[0]
        self.height = bounds[3] - bounds[1]
        self.move_obj()
        self.canv.tag_bind(self.planet_draw, '<ButtonPress-1>',
                           self.show_planet_info)  # bij klikken op cirkel wordt event afgehand

    def move_obj(self):
        """set drawing on new coordinates."""
        self.angle = self.angle + 1
        x = (self.canv.winfo_width() / 2 - self.width / 2) + self.distance_from_sun_draw * math.sin(
            math.radians(self.angle))
        y = (self.canv.winfo_height() / 2 - self.height / 2) + self.distance_from_sun_draw * math.cos(
            math.radians(self.angle))
        self.canv.move(self.planet_draw, x - self.canv.coords(self.planet_draw)[0],
                       y - self.canv.coords(self.planet_draw)[1])

    def show_planet_info(self, event):
        """Get information about the planet."""
        if not self.parent.t1.isAlive():
            self.parent.update_info_frame_label(self.planet.show_information(), self.planet)

    def change_color(self, color):
        """Change color of planetdrawing, only used for main planet."""
        self.canv.itemconfig(self.planet_draw, fill="{0}".format(color))


class MyPopupWindow:
    """Asks user for point distribution."""

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.top.title("Points")
        self.top.resizable(0, 0)
        lbl_text = ["Medicine:", "Agriculture:", "Architecture:"]
        w = 200  # width for the Tk root
        h = 120  # height for the Tk root

        # get screen width and height
        ws = self.top.winfo_screenwidth()  # width of the screen
        hs = self.top.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.entryList = []
        tk.Label(top, text="Spend 12 points in total:").grid(row=0, column=0, columnspan=2)
        for i in range(1, len(lbl_text) + 1):
            tk.Label(top, text="{0}".format(lbl_text[i - 1])).grid(row=i, column=0)
            self.entryList.append(tk.Entry(top))
            self.entryList[i - 1].grid(row=i, column=1)
        tk.Button(top, padx=20, text="OK", command=self.ok).grid(row=len(lbl_text) + 1, column=0, columnspan=2)
        self.top.protocol("WM_DELETE_WINDOW", self.ok)
        self.top.bind('<Return>', self.ok_enter)
        self.entryList[0].focus()

    def ok_enter(self, event):  # event gegenereerd door enter
        """Calls method ok when used."""
        self.ok()

    def ok(self):
        """Checks if the values are valid."""
        som = 0
        self.getallen = []
        try:
            for ent in self.entryList:
                self.getallen.append(int(ent.get()))
                if int(ent.get()) < 0:
                    raise ValueError('Negative number!')
                else:
                    som += int(ent.get())
            if som == 12:
                self.top.destroy()
            else:
                messagebox.showwarning(
                    "Error",
                    "Error: Please spend a total of 12 points."
                )
                self.top.lift()
        except ValueError:
            messagebox.showwarning(
                "Error",
                "Error: Please enter a positive number instead."
            )
            self.top.lift()
            self.entryList[0].focus()


class EndPage(tk.Frame):
    """Shows the end frame."""
    def __init__(self, parent, controller, index, main_planet=None):
        tk.Frame.__init__(self, parent, background="yellow")
        self.controller = controller
        self.index = index
        self.main_planet = main_planet
        self.title_font = tkf.Font(family="Verdana", size=18, weight=tkf.BOLD)

        self.picture = None
        if index is 0:
            self.picture = Image.open("Images\successful_screen.jpg").resize(
                (parent.winfo_width(), parent.winfo_height()))
        elif index is 1:
            self.picture = Image.open("Images\\failure_turns_screen.jpg").resize(
                (parent.winfo_width(), parent.winfo_height()))
        elif index is 2:
            self.picture = Image.open("Images\\failure_1_pop_screen.jpg").resize(
                (parent.winfo_width(), parent.winfo_height()))
        else:
            self.picture = Image.open("Images\\failure_0_pop_screen.jpg").resize(
                (parent.winfo_width(), parent.winfo_height()))
        self.picture = ImageTk.PhotoImage(self.picture)
        self.picture_lbl = tk.Label(self, image=self.picture)
        self.picture_lbl.image = self.picture
        self.picture_lbl.place(x=0, y=0)
        self.frm_info = tk.Frame(self)
        self.frm_info.place(anchor="c", relx=.50, rely=.50)  # in_=self,
        self.show_end(index, main_planet)

    def show_end(self, index, information):
        """Show end text."""
        text_list = ["The star has imploded.", "Only one person has survived.", "Everyone died."]
        if index is 0:
            tk.Label(self.frm_info, text="Simulation successful.", font=self.title_font).grid(row=0, column=0,
                                                                                              columnspan=2)
            tk.Label(self.frm_info, text="Your species have found a suitable exoplanet.").grid(row=1, column=0,
                                                                                               columnspan=2)
            tk.Label(self.frm_info, text="End population : {0:,}".format(self.main_planet.total_population)).grid(row=2,
                                                                                                                  column=0,
                                                                                                                  columnspan=2)
        else:
            tk.Label(self.frm_info, text="Simulation failed.", font=self.title_font).grid(row=0, column=0, columnspan=2)
            tk.Label(self.frm_info, text="{0}".format(text_list[index - 1])).grid(row=1, column=0, columnspan=2)
            tk.Label(self.frm_info, text="End progression : {0}".format(int(self.main_planet.progression))).grid(row=2,
                                                                                                                 column=0,
                                                                                                                 columnspan=2)
        ttk.Button(self.frm_info, text="Restart", command=lambda: self.controller.start_simulation()).grid(
            row=self.frm_info.grid_size()[1], sticky="nesw")
        ttk.Button(self.frm_info, text="Exit", command=lambda: self.controller.on_exit()).grid(
            row=self.frm_info.grid_size()[1] - 1, column=1, sticky="nesw")


app = Application()
app.iconbitmap("Images\\render_sun_r9l_icon.ico")
app.mainloop()
