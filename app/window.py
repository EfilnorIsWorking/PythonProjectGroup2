import pygame
import pygame._sdl2 as sdl2
from pygame.locals import QUIT
import sys

# window class
class Window:
    def __init__(self, game):
        self.game = game

        # win settings
        self.title = "Isometric Bob Game"
        self.icon = pygame.image.load("src/img/icon.png")
        self.w = 1920
        self.h = 1080

        # init window
        self.normal_init()


        # setup game clock
        self.clock = pygame.time.Clock()
        self.tickFPS = 360
        self.fps = 0
        self.deltaTime = 0

        # mouse position saving
        self.mouseDownPos = [0, 0]
        self.mouseUpPos = [0, 0]

        # surfaces
        self.gameSurf = pygame.Surface((self.w, self.h))

        # input
        self.lastKey = ""

    # legacy pygame window init
    def normal_init(self):
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE | pygame.WINDOWPOS_CENTERED)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)



    # handle events for window: quit, keyboard, mouse etc
    def handle_events(self):
        if not self.game.running: return

        for event in pygame.event.get():
            # quit the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # keyboard events
            if event.type == pygame.KEYDOWN:
                self.lastKey = pygame.key.name(event.key)

            # keyboard events
            if event.type == pygame.KEYDOWN:
                self.lastKey = pygame.key.name(event.key)

            # mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    self.mouseDownPos = [mx, my]

                    # update move pos in camera
                    self.game.camera.moveCurrentPos = [mx, my]

            # scroll events
            if event.type == pygame.MOUSEWHEEL:
                self.game.camera.zoom += 0.02 * event.y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    self.mouseUpPos = [mx, my]

        # clear screen
        color = (156, 213, 226)
        if not self.game.renderingEnabled:
            color = (0, 0, 0)

        self.screen.fill(color)


    # update the window
    def update(self):
        # update the window
        # legacy pygame
        pygame.display.update()


        # tick clock
        self.deltaTime = self.clock.tick(self.tickFPS)
        self.fps = self.clock.get_fps()

        # DEBUG: framerate in caption
        # pygame.display.set_caption(f"FPS: {int(self.fps)}")
