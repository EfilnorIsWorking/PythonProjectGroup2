import pygame
import pygame._sdl2 as sdl2


class Food:
    def __init__(self, game, x, y):
        self.game = game

        # position
        self.x = x
        self.y = y

        # properties
        self.initialEnergyGive = 100
        self.energyGive = self.initialEnergyGive
        self.rect = pygame.Rect(self.x, self.y, 48, 48)

        self.active = True

    # update rectangle (for collisions)
    def update_rect(self):
        x = self.x
        y = self.y

        x, y = self.game.tilemap.to_isometric(x, y)
        y = y - self.game.camera.y
        x = x - self.game.camera.x
        x = x * self.game.camera.zoom
        y = y * self.game.camera.zoom
        x -= (24 * self.game.camera.zoom)
        y -= (24 * self.game.camera.zoom)

        w = 48 * self.game.camera.zoom
        h = 48 * self.game.camera.zoom

        # set pygame rect
        self.rect = pygame.Rect(x, y, w, h)

    # init function
    def init(self):
        pass

    # draw
    def draw(self):
        if not self.active: return

        x = self.x
        y = self.y

        # position to isometric screen position
        x, y = self.game.tilemap.to_isometric(x, y)
        x -= 4
        y -= 6

        # draw if this is leftover or not
        if self.energyGive == self.initialEnergyGive:
            self.game.imgFoodShadow.draw(x+5, y+5)
            self.game.imgFood.draw(x, y)
        else:
            self.game.imgFoodLeftoverShadow.draw(x+5, y+5)
            self.game.imgFoodLeftover.draw(x, y)

    def update(self):
        if not self.active: return

        self.update_rect()
        if self.game.renderingEnabled: self.draw()
