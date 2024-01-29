import pygame


# camera
class Camera:
    def __init__(self, game):
        self.game = game

        # camera coordinates
        self.x = 0
        self.y = 0

        self.zoom = 0.1
        self.minZoom = 0.05
        self.maxZoom = 3

        # camera moving setup
        self.mouseMovingEnabled = True
        self.moveCurrentPos = [0, 0]
        self.moveAmount = 2

    def update(self):
        # clamp zoom
        if self.zoom <= self.minZoom:
            self.zoom = self.minZoom
        if self.zoom >= self.maxZoom:
            self.zoom = self.maxZoom

        # camera movement
        if not self.game.menuGUI.frmMenu.active:
            if self.mouseMovingEnabled:
                if pygame.mouse.get_pressed()[0]:
                    # move camera with mouse
                    # calculate the movement
                    mx, my = pygame.mouse.get_pos()
                    self.x -= (mx - self.moveCurrentPos[0]) * self.moveAmount
                    self.y -= (my - self.moveCurrentPos[1]) * self.moveAmount
                    self.moveCurrentPos = [mx, my]

