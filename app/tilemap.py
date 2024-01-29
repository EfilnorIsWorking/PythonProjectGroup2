from app.image import Image
from app.bob import Bob
from app.food import Food
from app.window import *

import random


# tilemap class
class Tilemap:
    def __init__(self, game):
        global Window
        self.game = game
        window = Window(self.game)
        # setup map size
        self.sizeWidth = 50
        self.sizeHeight = 50

        # setup tile size
        self.tileWidth = self.game.tileWidth
        self.tileHeight = self.game.tileHeight
        self.halfTileWidth = self.tileWidth * 0.45
        self.halfTileHeight = self.tileHeight * 0.78

        # map
        self.mapData = []
        self.chunks = [[], [], [], [], [], [], [], [], []]
        self.chunkDivide = 16

        # bobs
        self.bobs = []
        self.foods = []

        # amounts
        self.bobsAmount = 100
        self.foodAmount = 200

        # genetic limits
        self.minVelocity = 0.8
        self.maxVelocity = 2.0
        self.minMass = 0.4
        self.maxMass = 2.5
        self.minPerc = 3
        self.maxPerc = 18

        # init
        self.init()

    # init tilemap
    def init(self):
        # load images
        self.imgGrass = Image(self.game, "tiles/grass.png", w=self.tileWidth, h=self.tileHeight)
        self.imgSand = Image(self.game, "tiles/sand.png", w=self.tileWidth, h=self.tileHeight)

        # generate map
        self.generate_map()

    # return lowest point in a chunk (top left)
    def find_lowest_point(self, tilemap):
        lowestPoint = min(tilemap, key=lambda tile: tile[1])
        return [lowestPoint[0], lowestPoint[1]]

    # return highest point in a chunk (bottom right)
    def find_highest_point(self, tilemap):
        highestPoint = max(tilemap, key=lambda tile: tile[1])
        return [highestPoint[0], highestPoint[1]]

    # return a random location on the map
    def random_location(self):
        randX = random.randint(1, self.sizeWidth-4)
        randY = random.randint(1, self.sizeHeight-4)
        return [randX, randY]

    # generate a new bob into the map
    def add_bob(self, x, y, vel, mass, energy, perc):
        bob = Bob(self.game, x, y, False)
        bob.velocity = vel
        bob.mass = mass
        bob.energy = energy
        bob.perception = perc

        bob.load_images()

        bob.resize()
        self.bobs.append(bob)

    # add a new food to the map
    def add_food(self, x, y, give):
        food = Food(self.game, x, y)
        food.energyGive = give

        self.foods.append(food)

    # spawn an amount of bobs
    def spawn_bobs(self, amount):
        self.bobs = []

        # amount
        for i in range(amount):
            # random loc
            x, y = self.random_location()

            # add
            bob = Bob(self.game, x, y)
            self.bobs.append(bob)

    # spawn food with amount
    def spawn_food(self, amount):
        self.foods = []

        # amount
        for i in range(amount):
            # random location
            x, y = self.random_location()

            # spawn food
            food = Food(self.game, x, y)
            self.foods.append(food)

    # generate a map
    def generate_map(self):
        # clear current map
        self.mapData = []
        self.chunks = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        print(self.sizeWidth, self.sizeHeight)

        # generate 2d map
        for x in range(self.sizeWidth):
            for y in range(self.sizeHeight):
                tileType = random.randint(0, 1)

                toAdd = [x, y, tileType]

                self.mapData.append(toAdd)

                # get chunk size
                chunkW = self.sizeWidth//self.chunkDivide
                chunkH = self.sizeHeight//self.chunkDivide
                cur = 0

                for col in range(self.chunkDivide):
                    if x > col*chunkW and x <= (col+1)*chunkW:
                        self.chunks[col].append(toAdd)

        # self.spawn_bobs(self.bobsAmount)
        # self.spawn_food(self.foodAmount)

    # init the map
    def init_map(self):
        # clear entities & spawn new
        self.bobs = []
        self.foods = []
        self.spawn_bobs(self.bobsAmount)
        self.spawn_food(self.foodAmount)

    # calculate and return to isometric location
    def to_isometric(self, x, y):
        nx = x - y
        ny = (x + y) / 2
        nx = 9500 + nx * self.halfTileWidth + self.tileWidth / 2
        ny = 3000 + ny * self.halfTileHeight + self.tileHeight / 2
        return [nx, ny]

    # get count of alive bobs
    def get_bobs_count(self):
        count = 0
        for bob in self.bobs:
            if bob.energy > 0 and not bob.dead:
                count += 1
        return count

    # update map
    def update(self):
        toRender = []

        # get what chunks to render
        for chunk in self.chunks:
            lpX, lpY = self.find_lowest_point(chunk)
            lpX, lpY = self.to_isometric(lpX, lpY)
            lpX = lpX - self.game.camera.x
            lpY = lpY - self.game.camera.y

            hpX, hpY = self.find_highest_point(chunk)
            hpX, hpY = self.to_isometric(hpX, hpY)
            hpX = hpX - self.game.camera.x
            hpY = hpY - self.game.camera.y

            #if lpX > -self.game.window.w and lpX < self.game.window.w*4:
            toRender += chunk

        # render 2.5d isometric map
        if self.game.renderingEnabled:
            for tile in toRender:
                x, y = self.to_isometric(tile[0], tile[1])
                tileType = tile[2]

                zoom = self.game.camera.zoom
                if x-self.game.camera.x > (-self.tileWidth*1.2)/zoom and y-self.game.camera.y > (-self.tileHeight*1.2)/zoom:
                    if x-self.game.camera.x < (self.game.window.w*1.1)/zoom and y-self.game.camera.y < (self.game.window.h*1.1)/zoom:
                        img = self.imgGrass
                        if tileType == 0:
                            img = self.imgGrass
                        if tileType == 1:
                            img = self.imgSand

                        img.draw(x, y)

        # render bobs
        for bob in self.bobs:
            bob.update()

            if bob.despawned:
                self.bobs.remove(bob)

        # render food
        for food in self.foods:
            food.update()

            if not food.active:
                self.foods.remove(food)
