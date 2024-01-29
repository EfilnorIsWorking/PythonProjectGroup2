import os
import json

from tkinter import filedialog

# default settings
DEFAULT_SETTINGS = {
    "tilemap": {
        "width": 64,
        "height": 64,
    },
    "entities": {
        "bobs_amount": 100,
        "food_amount": 100,
    },
    "time": {
        "day_length": 100,
    },
    "reproduction": {
        "parthenogenesis": True,
        "sexual": True,
    },
    "genetics": {
        "min_vel": 0.8,
        "max_vel": 2.0,
        "min_mass": 0.4,
        "max_mass": 2.5,
        "min_perc": 3,
        "max_perc": 18,
    },
}


# data class
class Data:
    def __init__(self, bobs=[]):
        self.defaultSettings = DEFAULT_SETTINGS

        # all the data in a json
        self.bobs = bobs
        self.foods = []
        self.camera = [0, 0]
        self.day = {"time": 100, "current": 0}
        self.settings = self.defaultSettings

    # return in json format
    def get_json(self):
        data = {
            "bobs": [],
            "foods": [],
            "camera": [0, 0],
            "day": {"time": 100, "current": 0},
            "settings": self.defaultSettings,
        }

        # get all the bobs and put them into the json
        for bob in self.bobs:
            x = bob.x
            y = bob.y
            vel = bob.velocity
            mass = bob.mass
            energy = bob.energy
            perc = bob.perception

            data["bobs"].append({
                "x": x,
                "y": y,
                "vel": vel,
                "mass": mass,
                "energy": energy,
                "perc": perc,
            })

        # get all the foods and put in json
        for food in self.foods:
            x = food.x
            y = food.y
            give = food.energyGive

            data["foods"].append({
                "x": x,
                "y": y,
                "give": give,
            })

        # camera pos in json
        data["camera"] = self.camera

        # day in the json
        data["day"] = self.day

        # settings in the json
        data["settings"] = self.settings

        # return the json data
        return data


# file class
class File:
    def __init__(self, path):
        self.path = path

        self.full = path

    # save into the file
    def save_data(self, data):
        # get the data
        if data is not None:
            # convert to string
            data = json.dumps(data)
        else:
            # data corrupt? generate new data
            data = {
                "bobs": [],
                "foods": [],
                "camera": [0, 0],
                "day": {"time": 100, "current": 0},
                "settings": DEFAULT_SETTINGS,
            }
            # convert to string
            data = json.dumps(data)

        # write in file
        f = open(self.full, "w")
        f.write(data)
        f.close()

    # get data from the file
    def get_data(self):
        # read it if the file exists
        if os.path.isfile(self.full):
            # read it
            with open(self.full, "r") as f:
                data = f.read()
            
            # convert string to json/dictionairy
            data = json.loads(data)
            return data
        else:
            return None


# save file class
class SaveFile:
    def __init__(self, game):
        self.game = game

        self.data = Data()
        self.current = None

    # filedialog to open save file
    def ask_file(self):
        # self.save()

        self.game.menuGUI.close()

        file = filedialog.askopenfile(mode="r", filetypes=[("Save Files", f"*.{self.game.extension}")])

        if file is not None:
            self.load_file(file.name)
            file.close()

    # filedialog to save new file
    def save_as(self):
        self.save()

        self.game.menuGUI.close()

        file = filedialog.asksaveasfilename(filetypes=[("Save Files", f"*.{self.game.extension}")], defaultextension=[("Save Files", f"*.{self.game.extension}")])

        if file is not None and file != "":
            self.current = File(file)
            self.save()

    def load_file(self, file):
        self.data = Data()

        self.current = File(file)
        load = self.current.get_data()
        if load is not None:
            self.data.bobs = load["bobs"]
            self.data.foods = load["foods"]
            self.data.camera = load["camera"]
            self.data.day = load["day"]
            self.data.settings = load["settings"]
        else:
            self.current.save_data(None)

        if self.data is not None:
            self.game.tilemap.bobs = []
            self.game.tilemap.foods = []

            print("loading")

            # bobs
            bobs = self.data.bobs
            for bob in bobs:
                self.game.tilemap.add_bob(bob["x"], bob["y"], bob["vel"], bob["mass"], bob["energy"], bob["perc"])

            # foods
            foods = self.data.foods
            for food in foods:
                self.game.tilemap.add_food(food["x"], food["y"], food["give"])

            # day & time
            day = self.data.day
            self.game.currentDay = day["current"]
            self.game.dayTimer.current = day["time"]

            # camera position
            self.game.camera.x = self.data.camera[0]
            self.game.camera.y = self.data.camera[1]

            # settings
            self.game.tilemap.sizeWidth = self.data.settings["tilemap"]["width"]
            self.game.tilemap.sizeHeight = self.data.settings["tilemap"]["height"]
            self.game.tilemap.bobsAmount = self.data.settings["entities"]["bobs_amount"]
            self.game.tilemap.foodAmount = self.data.settings["entities"]["food_amount"]
            self.game.dayTimer.duration = self.data.settings["time"]["day_length"]

            self.game.parthenoRepr = self.data.settings["reproduction"]["parthenogenesis"]
            self.game.sexualRepr = self.data.settings["reproduction"]["sexual"]

            # genetic settings
            gs = self.data.settings["genetics"]
            self.game.tilemap.minVelocity = gs["min_vel"]
            self.game.tilemap.maxVelocity = gs["max_vel"]
            self.game.tilemap.minMass = gs["min_mass"]
            self.game.tilemap.maxMass = gs["max_mass"]
            self.game.tilemap.minPerc = gs["min_perc"]
            self.game.tilemap.maxPerc = gs["max_perc"]

            # tilemap
            self.game.tilemap.generate_map()

    def save(self):
        if self.current is not None:
            self.data.bobs = self.game.tilemap.bobs
            self.data.foods = self.game.tilemap.foods
            self.data.camera = [self.game.camera.x, self.game.camera.y]
            self.data.day = {
                "time": self.game.dayTimer.current,
                "current": self.game.currentDay
            }

            self.data.settings = {
                "tilemap": {
                    "width": self.game.tilemap.sizeWidth,
                    "height": self.game.tilemap.sizeHeight,
                },
                "entities": {
                    "bobs_amount": self.game.tilemap.bobsAmount,
                    "food_amount": self.game.tilemap.foodAmount,
                },
                "time": {
                    "day_length": self.game.dayTimer.duration,
                },
                "reproduction": {
                    "parthenogenesis": self.game.parthenoRepr,
                    "sexual": self.game.sexualRepr,
                },
                "genetics": {
                    "min_vel": self.game.tilemap.minVelocity,
                    "max_vel": self.game.tilemap.maxVelocity,
                    "min_mass": self.game.tilemap.minMass,
                    "max_mass": self.game.tilemap.maxMass,
                    "min_perc": self.game.tilemap.minPerc,
                    "max_perc": self.game.tilemap.maxPerc,
                },
            }

            data = self.data.get_json()
            self.current.save_data(data)
