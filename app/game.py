import pygame

from app.window import *
from app.tilemap import Tilemap
from app.camera import Camera
from app.image import Image
from app.timer import Timer
from app.menu_gui import MenuGUI
from app.reinit_gui import ReinitGUI
from app.savefile import SaveFile


# main game class
class Game:
    def __init__(self):
        self.running = True

        # save file extension
        self.extension = "bobs"

        # timers
        self.timers = []
        self.nonTickTimers = []

        # guis
        self.guis = []


        # savefile
        self.savefile = SaveFile(self)

        # initialize game
        self.init()

    # property function to return the window surface
    @property
    def screen(self):
        return self.window.screen
    
    # property function to return deltaTime
    @property
    def dt(self):
        return self.window.deltaTime

    # load the necessary images
    def load_images(self):
        self.imgBob = Image(self, "bob/bob.png", 64, 64)
        self.imgDeadBob = Image(self, "bob/bob_dead.png", 64, 64)

        self.imgFood = Image(self, "food/food.png", 64, 64)
        self.imgFoodShadow = Image(self, "food/food_shadow.png", 64, 64)

        self.imgFoodLeftover = Image(self, "food/food_leftover.png", 64, 64)
        self.imgFoodLeftoverShadow = Image(self, "food/food_leftover_shadow.png", 64, 64)

    # game init function
    def init(self):
        # setup variables
        self.tileWidth = 200
        self.tileHeight = 100
        self.dayLength = 100 # ticks

        self.tickDuration = 100
        self.currentTickCountdown = self.tickDuration
        self.currentTick = 0

        # setup window
        self.window = Window(self)

        # load images
        self.load_images()

        # create camera
        self.camera = Camera(self)

        # create tilemap
        self.tilemap = Tilemap(self)

        # create gui
        self.menuGUI = MenuGUI(self)
        self.add_gui(self.menuGUI)

        self.reinitGUI = ReinitGUI(self)
        self.add_gui(self.reinitGUI)

        # color filter (for day and night)
        self.colorFilterSurface = pygame.Surface((self.window.w, self.window.h))
        self.colorFilterSurface.set_alpha(105)

        self.nightFilterColor = (0, 97, 255)

        # state
        self.isDay = True
        self.currentDay = 0
        self.pauseTick = False
        self.tickSpeedMult = 1
        self.renderingEnabled = True
        self.parthenoRepr = True
        self.sexualRepr = True
        self.mutation = 0.1

        # day and night cycle
        self.dayNightTimer = Timer(self, self.dayLength//2, self.switch_day_night, True)
        #self.add_timer(self.dayNightTimer)

        self.dayTimer = Timer(self, self.dayLength, self.new_day, True)
        self.add_timer(self.dayTimer)

        self.dayNightTimer.start()
        self.dayTimer.start()

        self.tilemap.init_map()

    # switch day/night
    def switch_day_night(self):
        if self.isDay:
            self.isDay = False
            return
        else:
            self.isDay = True
            return

    # reinitialize the game (map, bobs, etc)
    def reinit(self, mapW, mapH, bobsAm, foodAm, dayL, parth, sex, minVel, maxVel, minMass, maxMass, minPerc, maxPerc):
        # set new parameters
        self.tilemap.sizeWidth = mapW
        self.tilemap.sizeHeight = mapH
        self.tilemap.bobsAmount = bobsAm
        self.tilemap.foodAmount = foodAm
        self.dayTimer.duration = dayL
        self.dayTimer.current = dayL
        self.parthenoRepr = parth
        self.sexualRepr = sex

        self.tilemap.minVelocity = minVel
        self.tilemap.maxVelocity = maxVel
        self.tilemap.minMass = minMass
        self.tilemap.maxMass = maxMass
        self.tilemap.minPerc = minPerc
        self.tilemap.maxPerc = maxPerc

        # regenerate map
        self.tilemap.generate_map()
        self.tilemap.init_map()

    # on new day
    def new_day(self):
        # add currentDay
        self.currentDay += 1

        # new food
        self.tilemap.spawn_food(self.tilemap.foodAmount)

    # register a new timer
    def add_timer(self, timer):
        self.timers.append(timer)

    # register a new timer that is not based on tick but frame
    def add_timer_not_tick(self, timer):
        self.nonTickTimers.append(timer)

    # handle ticks
    def update_tick(self):
        # countdown the tick
        self.currentTickCountdown -= (0.1 * self.dt) * self.tickSpeedMult

        if self.currentTickCountdown <= 0:
            # add tick
            self.currentTick += 1

            # update timers
            for timer in self.timers:
                timer.countdown()

            # reset countdown
            self.currentTickCountdown = self.tickDuration

    # update all the GUI
    def update_guis(self):
        for gui in self.guis:
            gui.update()

    # register a new gui to render infront of everything
    def add_gui(self, gui):
        self.guis.append(gui)

    # remove from gui list and stop updating it
    def remove_gui(self, gui):
        if gui in self.guis:
            self.guis.remove(gui)

    # game update
    def update(self):
        # handle window events: on closed, keyboard, etc
        self.window.handle_events()

        # update scene
        self.camera.update()
        self.tilemap.update()

        # color filter (night)
        if self.renderingEnabled:
            self.colorFilterSurface.fill(self.nightFilterColor)
            if not self.isDay:
                self.screen.blit(self.colorFilterSurface, (0, 0))


        # update guis
        self.update_guis()

        # tick update
        if not self.pauseTick:
            self.update_tick()

        # day/night
        if self.dayTimer.current <= self.dayTimer.duration/2:
            # night
            self.isDay = False
        else:
            self.isDay = True

        # non-tick timers
        for timer in self.nonTickTimers:
            timer.countdown()

        # window update
        self.window.update()
