import pygame
import random
import math

from app.timer import Timer
from app.image import Image
from app.food import Food 
from app.gui import *


# function to clamp float
def clamp(a, mi, ma):
    if a <= mi:
        a = mi
    if a >= ma:
        a = ma
    return a


# GUI for a bob (to show statistics)
class BobGUI(GUI):
    def __init__(self, game, bob):
        super().__init__(game)
        self.bob = bob

        # setup UI elements
        self.frame = Frame(self, 0, 0, 250, 300, (64, 64, 64))
        self.entity = Text(self, 10, 10, text="Bob")

        self.energy = Text(self, 10, 50, text="Energy: 100", fontSize=20)
        self.velocity = Text(self, 10, 80, text="Velocity: 1.6", fontSize=20)
        self.mass = Text(self, 10, 110, text="Mass: 10", fontSize=20)
        self.perc = Text(self, 10, 140, text="Perception: 3", fontSize=20)
        self.memory = Text(self, 10, 170, text="Memory tiles : 0", fontSize=20)
        self.foodmem = Text(self, 10, 200, text="Food memory: 0", fontSize=20)
        self.visible = False

    def update(self):
        # check if it should be visible (if mouse hovers over bob)
        if self.visible:
            if self.game.menuGUI.frmMenu.active:
                self.visible = False
        mx, my = pygame.mouse.get_pos()
        s = 150 * self.game.camera.zoom
        mrect = pygame.Rect(mx - s / 2, my - s / 2, s, s)
        if not mrect.colliderect(self.bob.rect):
            self.visible = False

        if not self.game.renderingEnabled:
            self.visible = False

        # set position
        self.set_position(self.bob.rect.x, self.bob.rect.y)

        # rendering
        self.draw_element(self.frame)
        self.draw_element(self.entity)

        # set the text with the right variables
        self.energy.set_text(f"Energy: {int(self.bob.energy)}/{self.bob.maxEnergy}")
        self.velocity.set_text(f"Velocity: {self.bob.velocity}")
        self.mass.set_text(f"Mass: {self.bob.mass}")
        self.perc.set_text(f"Perception: {self.bob.perception}")
        self.memory.set_text(f"Memory: {len(self.bob.memoryTiles)}")
        self.foodmem.set_text(f"Food memory: {self.bob.foodmem}")

        # draw the text
        self.draw_element(self.velocity)
        self.draw_element(self.mass)
        self.draw_element(self.energy)
        self.draw_element(self.perc)
        self.draw_element(self.memory)
        self.draw_element(self.foodmem)


# bob entity class
class Bob:
    def __init__(self, game, x, y, generateRandomGenetics=False):
        self.game = game
        self.x = x
        self.y = y

        self.w = 48
        self.h = 48

        # movement
        self.speed = 30 # more = slower (interpolation speed, NOT velocity)
        self.totalMoveX = 0
        self.totalMoveY = 0
        self.speedBufferX = 0
        self.speedBufferY = 0

        # genetic properties
        self.velocity = 1
        self.mass = 1
        self.perception = 4
        self.memory = 4
        self.memoryTiles = []
        self.foodMemory = []
        self.foodmem = 0

        self.energy = 100
        self.maxEnergy = 200

        # state
        self.dead = False
        self.despawned = False
        self.newborn = True
        self.foodTarget = None
        self.stayOnFood = True

        # rect
        self.rect = pygame.Rect(0, 0, 48, 48)

        #direction
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        # init
        if generateRandomGenetics:
            self.random_genetics()
        self.init_gui()
        self.init()

    def random_genetics(self):
        self.velocity = random.randint(8, 20)/10
        self.mass = random.randint(4, 25)/10
        self.perception = random.randint(3, 18)

        self.load_images()

    def load_images(self):
        bobImage = "bob.png"

        # get the right image based on the velocity
        # more velocity = more blue
        if self.velocity >= 1.2 and self.velocity < 1.4:
            bobImage = "bob_blue_1.png"
        elif self.velocity >= 1.4 and self.velocity < 1.6:
            bobImage = "bob_blue_2.png"
        elif self.velocity >= 1.6 and self.velocity < 1.8:
            bobImage = "bob_blue_3.png"
        elif self.velocity >= 1.8 and self.velocity < 2.0:
            bobImage = "bob_blue_4.png"
        elif self.velocity >= 2.0:
            bobImage = "bob_blue_5.png"

        # load the images
        self.img = Image(self.game, f"bob/{bobImage}", 64, 64)
        self.imgShadow = Image(self.game, "bob/bob_shadow.png", 64, 64)
        self.imgDead = Image(self.game, "bob/bob_dead.png", 64, 64)

    def init_gui(self):
        # initialize the gui for this bob
        self.gui = BobGUI(self.game, self)
        self.game.add_gui(self.gui)

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def movement(self):
        if self.dead: return
        if self.game.pauseTick: return

        x = 1
        y = 1

        # smooth interpolation movement
        # slowly and smoothly moves to the tile it belongs to
        if self.totalMoveX > 0.2:
            self.x += x / (self.speed / self.game.tickSpeedMult)
            self.totalMoveX -= 1/(self.speed / self.game.tickSpeedMult)
        elif self.totalMoveX < -0.2:
            self.x -= x/(self.speed / self.game.tickSpeedMult)
            self.totalMoveX += 1/(self.speed / self.game.tickSpeedMult)

        if self.totalMoveY > 0.2:
            self.y += y / (self.speed / self.game.tickSpeedMult)
            self.totalMoveY -= 1 / (self.speed / self.game.tickSpeedMult)
        elif self.totalMoveY < -0.2:
            self.y -= y / (self.speed / self.game.tickSpeedMult)
            self.totalMoveY += 1 / (self.speed / self.game.tickSpeedMult)

        # update of the memory tiles    
        if len(self.memoryTiles) >= 2*self.memory and self.memoryTiles != [] and (self.memory != 0):
            food_coordinates = self.memoryTiles.pop(0)
            for food in self.game.tilemap.foods:
                if food.x == food_coordinates[0] and food.y == food_coordinates[1]:
                    self.foodMemory.append(food)
                    self.foodmem += 1
                    self.memory -=1
                    break

        self.memoryTiles.append([self.x, self.y])

    # initialize bob
    def init(self):
        # load imagse
        self.load_images()

        # set newborn to False after a time
        self.newbornTimer = Timer(self.game, 10, self.not_newborn, False)
        self.game.add_timer(self.newbornTimer)
        if self.newborn:
            self.newbornTimer.start()

        # randomly move every tick
        self.moveTimer = Timer(self.game, 1, self.random_move, True)
        self.moveTimer.start()
        self.game.add_timer(self.moveTimer)

        # despawn after some time if dead
        self.despawnTimer = Timer(self.game, 5, self.despawn, False)
        self.game.add_timer(self.despawnTimer)

        # resize the bobs image based on mass
        self.resize()

        # smooth movement (smoothly move to the tile it belongs to)
        self.movementTimer = Timer(self.game, 5, self.movement, True)
        self.game.add_timer_not_tick(self.movementTimer)
        self.movementTimer.start()

    def resize(self):
        # calculate the size
        w = 64 * self.mass
        h = 64 * self.mass
        self.w = w
        self.h = h

        # resize
        self.img.resize(w, h)
        self.imgShadow.resize(w, h)

    def not_newborn(self):
        # no longer newborn
        self.newborn = False

    def despawn(self):
        # despawn and remove from the game
        self.game.remove_gui(self.gui)
        self.despawned = True

    # move the bob
    def move(self, x, y):
        if self.dead: return

        # move the opposite direction if is close to the edge of the island
        if self.x <= 1.5:
            x = 1
        if self.y <= 1.5:
            y = 1
        if self.x >= self.game.tilemap.sizeWidth-7:
            x = -1
        if self.y >= self.game.tilemap.sizeHeight-7:
            y = -1

        # calculate the total movement
        addX = x * self.velocity
        addY = y * self.velocity

        # calculate with speedbuffer
        intX = int(addX)
        intY = int(addY)
        self.speedBufferX += abs(addX - intX)
        self.speedBufferY += abs(addY - intY)

        # take more movement from speedbuffer
        moreX = 0
        moreY = 0
        if self.speedBufferX >= 1:
            moreX = 1
            self.speedBufferX = 0
        if self.speedBufferY >= 1:
            moreY = 1
            self.speedBufferY = 0

        self.totalMoveX += addX + moreX
        self.totalMoveY += addY + moreY

    # get every food target that is within the perception range
    def get_food_targets(self):
        foods = []
        # get every food
        for food in self.game.tilemap.foods:
            # calculate distance
            distX = food.x - self.x
            distY = food.y - self.y
            if distX > -round(self.perception) and distX < round(self.perception):
                if distY > -round(self.perception) and distY < round(self.perception):
                    foods.append(food)

        if foods == [] : 
            foods = self.foodMemory
        
        # return the foods
        return foods

    # get the food with most energy from list
    def get_primary_food(self, foods):
        target = None
        if len(foods) == 0: return None

        mostEnergy = 0

        for food in foods:
            if food.energyGive > mostEnergy:
                mostEnergy = food.energyGive
                target = food

        return target

    # get every threat within the perception range
    def get_hunter_targets(self):
        hunters = []
        for bob in self.game.tilemap.bobs:
            # get distance between this bob and the hunter
            distX = abs(bob.x - self.x)
            distY = abs(bob.y - self.y)

            if distX < round(self.perception) and distY < round(self.perception):
                # if the mass is not 0 (to prevent zero-division error)
                if self.mass != 0 and bob.mass != 0:
                    # is this a threat? (if b_m/B_m <= 2/3)
                    if self.mass/bob.mass <= 0.67:
                        # then register this bob
                        hunters.append(bob)

        # return the list
        return hunters

    def move_to_target(self, target, towards=True):
        xOrY = 1
        print(target.x)
        distX = abs(target.x - self.x)
        distY = abs(target.y - self.y)

        if distX > distY:
            xOrY = 1
        else:
            xOrY = 0

        # should it go towards the target or run away?
        # ^ in the function parameter
        mult = 1
        if not towards:
            mult = -1

        # move to or from the target
        try:
            x = self.x
            y = self.y
            if xOrY:
                if x > target.x:
                    self.move(-1*mult, 0)
                elif x < target.x:
                    self.move(1*mult, 0)
            else:
                if y > target.y:
                    self.move(0, -1*mult)
                elif y < target.y:
                    self.move(0, 1*mult)
        except:
            pass
    
    def move_to_random(self):
        xOrY = random.randint(0, 1)

        # check where it was before
        for i in range(len(self.memoryTiles)):
            if self.memoryTiles[i] == [self.x-1, self.y]:
                self.left = True
            if self.memoryTiles[i] == [self.x+1, self.y]:
                self.right = True
            if self.memoryTiles[i] == [self.x, self.y-1]:
                self.down = True
            if self.memoryTiles[i] == [self.x, self.y+1]:
                self.up = True

        # choose the direction to go
        if self.left and self.right and self.up:
            self.move(0, -1)
        elif self.left and self.right and self.down:
            self.move(0, 1)
        elif self.left and self.up and self.down:
            self.move(1, 0)
        elif self.right and self.up and self.down:
            self.move(-1, 0)
        elif self.left and self.right:
            self.move(0, random.choice([-1, 1]))
        elif self.up and self.down:
            self.move(random.choice([-1, 1]), 0)
        elif self.left and self.up:
            if xOrY:
                self.move(1, 0)
            else:
                self.move(0, -1)
        elif self.left and self.down:
            if xOrY:
                self.move(1, 0)
            else:
                self.move(0, 1)
        elif self.right and self.up:
            if xOrY:
                self.move(-1, 0)
            else:
                self.move(0, -1)
        elif self.right and self.down:
            if xOrY:
                self.move(-1, 0)
            else:
                self.move(0, 1)
        elif self.left:
            if xOrY:
                self.move(1, 0)
            else:
                self.move(0, random.choice([-1, 1]))
        elif self.right:
            if xOrY:
                self.move(-1, 0)
            else:
                self.move(0, random.choice([-1, 1]))
        elif self.up:
            if xOrY:
                self.move(random.choice([-1, 1]), 0)
            else:
                self.move(0, -1)
        elif self.down:
            if xOrY:
                self.move(random.choice([-1, 1]), 0)
            else:
                self.move(0, 1)
        else:
            self.move(random.choice([-1, 1]), random.choice([-1, 1]))
        
        # reset the directions
        self.right = False
        self.left = False
        self.up = False
        self.down = False
                
        
    # move x or y
    def random_move(self):
        if self.dead: return

        # substract energy
        if not self.stayOnFood:
            self.energy -= self.mass * (self.velocity ** 2) # + self.perception/20 + self.memory/20
        else:
            # -0.5 energy but stay on the food
            self.energy -= 0.5
            return

        # to decide if bob should move to food or randomly move
        moveType = "random"

        # decide what to do:
        # random, food, survive hunter
        if self.foodTarget is None or not self.foodTarget.active:
            foundFoods = self.get_food_targets()

            if len(foundFoods) > 0:
                # get food with most energy
                self.foodTarget = self.get_primary_food(foundFoods)
                moveType = "food"
            else:
                moveType = "random"
        else:
            moveType = "food"

        # are there hunters?
        hunters = self.get_hunter_targets()
        if len(hunters) != 0:
            moveType = "survive hunter"

        # finally, move
        if moveType == "food":
            self.move_to_target(self.foodTarget)
        elif moveType == "random":
            self.move_to_random()
        elif moveType == "survive hunter":
            self.move_to_target(hunters[0], False)

    # eat a bob
    def eat_bob(self, bob):
        # if this bob is dead, cancel this function
        if self.dead: return

        # eat the bob if it's not dead or newborn
        if not bob.dead and not bob.newborn:
            # eat energy
            self.energy += bob.energy
            bob.energy = 0

    def draw(self):
        x = self.x
        y = self.y

        # calculate to isometric screen position
        x, y = self.game.tilemap.to_isometric(x, y)

        # decide what image to render: dead or normal
        if not self.dead:
            self.imgShadow.draw(x + 5, y + 5)
            self.img.draw(x, y)
        else:
            self.imgDead.draw(x, y)

    # update rect (for collisions)
    def update_rect(self):
        x = self.x
        y = self.y

        x, y = self.game.tilemap.to_isometric(x, y)
        y = y - self.game.camera.y
        x = x - self.game.camera.x
        x = x * self.game.camera.zoom
        y = y * self.game.camera.zoom
        x -= (8 * self.game.camera.zoom)
        y -= (8 * self.game.camera.zoom)

        w = self.w * self.game.camera.zoom + (20 * self.game.camera.zoom)
        h = self.h * self.game.camera.zoom + (20 * self.game.camera.zoom)

        # update the pygame rect
        self.rect = pygame.Rect(x-w/2, y-h/2, w, h)

    def reproduce(self):
        # cancel this function, if disabld or dead
        if not self.game.parthenoRepr: return
        if self.dead: return

        # the new bob
        newBob = Bob(self.game, self.x, self.y, False)
        newBob.energy = 50
        newBob.newborn = True

        # genetics
        newBob.perception = self.perception + random.choice([-1, 0, 1])
        newBob.memory = self.memory + random.choice([-1, 0, 1])
        newBob.velocity = self.velocity
        newBob.mass = self.mass

        if self.game.mutation !=0.0: 
            newBob.velocity = random.uniform(self.velocity - self.game.mutation, self.velocity + self.game.mutation)
            newBob.mass = random.uniform(self.mass - self.game.mutation, self.mass + self.game.mutation)

        # initialize
        newBob.init()

        # substract our energy
        self.energy -= 150

        # register new bob
        self.game.tilemap.bobs.append(newBob)

    # sexual reproduction with bob
    def reproduce_bob(self, bob):
        # cancel if disabled or dead
        if not self.game.sexualRepr: return
        if self.dead: return

        # do we have enough energy?
        if self.energy >= 150 and bob.energy >= 150:
            # make new bob
            # mutation based on those two bobs
            newBob = Bob(self.game, self.x, self.y, False)
            newBob.energy = 100
            if self.game.mutation == 0.0:
                newBob.velocity = (bob.velocity + self.velocity) / 2
                newBob.mass = (bob.mass + self.mass) / 2
            else : 
                newBob.velocity = random.uniform((bob.velocity + self.velocity) / 2 - self.game.mutation, (bob.velocity + self.velocity) / 2 + self.game.mutation)
                newBob.mass = random.uniform((bob.mass + self.mass) / 2 - self.game.mutation, (bob.mass + self.mass) / 2 + self.game.mutation)

            newBob.perception = (bob.perception + self.perception) / 2 + random.choice([-1, 0, 1])
            newBob.memory = (bob.memory + self.memory) / 2 + random.choice([-1, 0, 1])

            newBob.newborn = True
            newBob.init()

            # substract the parents' energy
            self.energy -= 100
            bob.energy -= 100

            # register the child bob
            self.game.tilemap.bobs.append(newBob)        

    # update function for bob
    def update(self):
        # return if this is despawned
        if self.despawned: return

        # rendering
        self.update_rect()
        if self.game.renderingEnabled: self.draw()

        # enable GUI if mouse is hovering
        mx, my = pygame.mouse.get_pos()
        s = 150 * self.game.camera.zoom
        mrect = pygame.Rect(mx - s / 2, my - s / 2, s, s)
        if mrect.colliderect(self.rect):
            self.gui.visible = True
        else:
            self.gui.visible = False

        # eat food
        self.stayOnFood = False
        for food in self.game.tilemap.foods:
            if food.active:
                if food.rect.colliderect(self.rect):
                    # calculate how much to eat
                    maxEat = self.maxEnergy - self.energy
                    toEat = maxEat
                    if toEat >= food.energyGive:
                        toEat = food.energyGive

                    # eat
                    self.energy += toEat
                    food.energyGive -= toEat
                    if food.energyGive <= 0:
                        food.active = False
                        self.stayOnFood = False
                    else:
                        self.stayOnFood = True

        # eat bobs
        for bob in self.game.tilemap.bobs:
            if self.rect.colliderect(bob.rect):
                try:
                    # can this bob be eaten? (if B_m/b_m <= 2/3)
                    if bob.mass/self.mass < 0.67:
                        self.eat_bob(bob)
                    else: # bob.mass >= self.mass-3:
                        if not bob.newborn:
                            self.reproduce_bob(bob)
                except:
                    pass

        # dead if energy <= 0
        if self.energy <= 0:
            self.energy = 0
            if not self.dead:
                self.despawnTimer.start()
                self.dead = True

        # reproduce if energy capped
        if self.energy >= self.maxEnergy:
            self.reproduce()
