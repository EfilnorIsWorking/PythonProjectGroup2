import pygame
import pygame._sdl2 as sdl2

from app.timer import Timer

pygame.font.init()

# custom GUI elements:
# text, frame, button, slider, checkbox


# GUI class
class GUI:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0

        self.visible = True

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw_element(self, element):
        if not self.visible: return
        element.update()


# gui element parent class
class Element:
    def __init__(self, gui, x=0, y=0, w=32, h=32, parent=None):
        self.gui = gui
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.parent = parent

        self.screenAnchor = [0, 0]

        self.game = self.gui.game

        self.hovered = False

        self.active = True

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update_rect(self):
        x = self.x + self.gui.x
        y = self.y + self.gui.y

        if self.parent is not None:
            x += self.parent.rect.x
            y += self.parent.rect.y

        x = (self.screenAnchor[0] * self.game.window.w) + x
        y = (self.screenAnchor[1] * self.game.window.h) + y

        self.rect = pygame.Rect(x, y, self.w, self.h)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, w, h):
        self.w = w
        self.h = h

    '''def gpu_render(self, surf, x, y):
        tex = sdl2.Texture.from_surface(self.game.renderer, surf)
        tex.draw(dstrect=(x, y))'''

    def set_parent(self, parent):
        self.parent = parent

    def update(self):
        self.update_rect()

        if self.parent is not None:
            self.active = self.parent.active

        mx, my = pygame.mouse.get_pos()
        if pygame.Rect(mx-5, my-5, 10, 10).colliderect(self.rect):
            self.hovered = True
        else:
            self.hovered = False


class Frame(Element):
    def __init__(self, gui, x=0, y=0, w=0, h=0, color=(255, 255, 255), parent=None):
        super().__init__(gui, x, y, w, h, parent)
        self.color = color

    def set_color(self, color):
        self.color = color

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)


    def update(self):
        if not self.active: return

        super().update()
        self.draw()


class Slider(Element):
    def __init__(self, gui, x=0, y=0, w=300, h=17, caption="Slider", parent=None, minVal=0, maxVal=100, varType=float):
        super().__init__(gui, x, y, w, h, parent)
        self.caption = caption
        self.minVal = minVal
        self.maxVal = maxVal
        self.varType = varType

        self.game = self.gui.game

        self.txtCaption = Text(self.gui, text=self.caption, x=self.x, y=self.y)

        self.bg = (50, 50, 50)
        self.color = (0, 200, 0)

        self.curVal = maxVal/2

        self.valueRect = pygame.Rect(0, 0, 10, 10)

    def draw(self):
        self.txtCaption.update()

        slider = pygame.Rect(self.x, self.y+40, self.w, self.h)

        x = (self.curVal - self.minVal) / (self.maxVal - self.minVal)
        x = self.w * x
        self.valueRect = pygame.Rect(self.x + x - self.h/2, self.y+40 - self.h/2, self.h*2, self.h*2)

        pygame.draw.rect(self.game.screen, self.bg, slider, 0, 5)
        pygame.draw.rect(self.game.screen, self.color, self.valueRect, 0, 16)


    def update(self):
        super().update()

        if not self.active: return

        mx, my = pygame.mouse.get_pos()
        if pygame.Rect(mx-30, my-5, 60, 10).colliderect(self.valueRect):
            if pygame.mouse.get_pressed()[0]:
                x = mx
                if x <= self.x:
                    x = self.x
                if x >= self.x+self.w:
                    x = self.x + self.w

                x = x - self.x
                x = (x - 0) / (self.w - 0)
                self.curVal = (x * self.maxVal)
                if self.curVal <= self.minVal:
                    self.curVal = self.minVal

        if self.varType == float:
            self.txtCaption.set_text(f"{self.caption} ({str(self.curVal)[:4]})")
        if self.varType == int:
            self.txtCaption.set_text(f"{self.caption} ({int(self.curVal)})")

        self.draw()


# gui text element
class Text(Element):
    def __init__(self, gui, x=0, y=0, color=(255, 255, 255), fontSize=28, text="Text", parent=None):
        super().__init__(gui, x, y, 0, 0, parent)
        self.color = color
        self.fontSize = fontSize
        self.text = text

        self.update_font()

        # state
        self.hovered = False

    # update the font (updating it every second will lag)
    def update_font(self):
        self.font = pygame.font.SysFont("Arial", self.fontSize)

    def set_color(self, color):
        self.color = color

    def get_width(self):
        w = self.font.size(self.text)[0]
        if w == 0:
            w = 1
        return w

    def get_height(self):
        h = self.font.size(self.text)[1]
        if h == 0:
            h = 1
        return h

    def set_font_size(self, size):
        self.fontSize = size
        self.update_font()

    def set_text(self, text):
        if len(text) == 0:
            text = " "
        self.text = text

    def draw(self):
        surface = self.font.render(self.text, False, self.color)

        self.gui.game.screen.blit(surface, (self.rect.x, self.rect.y))


    def update(self):
        super().update()

        if not self.active: return

        self.draw()


# check box (true/false)
class Checkbox(Element):
    def __init__(self, gui, x=0, y=0, w=180, h=50, text="Checkbox", parent=None):
        super().__init__(gui, x, y, w, h, parent)
        self.text = text

        self.game = self.gui.game

        # state
        self.currentState = False

        self.canClick = False
        self.canClickTimer = Timer(self.game, 20, self.can_click, False)
        self.game.add_timer_not_tick(self.canClickTimer)
        self.canClickTimer.start()

        # text
        self.textW = Text(self.gui, x=self.x+40, y=self.y, text=self.text)

    @property
    def value(self):
        return self.currentState

    def draw(self):
        if not self.active: return

        box = pygame.Rect(self.rect.x, self.rect.y, 50, 50)

        if not self.currentState:
            pygame.draw.rect(self.game.screen, (255, 200, 200), box, 3)
        else:
            surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            box.x = 0
            box.y = 0
            if not self.currentState:
                pygame.draw.rect(surf, (255, 200, 200), box, 3)
            else:
                pygame.draw.rect(surf, (200, 255, 200), box)
            #self.gpu_render(surf, self.rect.x, self.rect.y)

        self.textW.screenAnchor = self.screenAnchor
        self.textW.set_text(self.text)
        textX = self.x + 60
        textY = self.y + 25 - self.textW.get_height()/2
        self.textW.set_position(textX, textY)
        self.textW.update()

    def switch(self):
        if self.currentState:
            self.currentState = False
            return
        else:
            self.currentState = True
            return

    def can_click(self):
        self.canClick = True

    def update(self):
        super().update()

        if not self.active: return

        if self.hovered:
            if self.canClick:
                if pygame.mouse.get_pressed()[0]:
                    self.switch()
                    self.canClick = False
                    self.canClickTimer.start()

        self.draw()


# numberinputbox gui class
class NumberInputBox(Element):
    def __init__(self, gui, x=0, y=0, w=150, h=35, minVal=0, maxVal=50, caption="Input", parent=None):
        super().__init__(gui, x, y, w, h, parent)
        self.game = self.gui.game
        self.minVal = minVal
        self.maxVal = maxVal
        self.caption = caption

        # color
        self.bg = (80, 80, 80)
        self.focusColor = (110, 110, 110)
        self.color = self.bg

        # state
        self.focused = False
        self.currentInput = "0"

        # text
        self.textC = Text(self.gui, x=0, y=0, text=self.caption)
        self.textW = Text(self.gui, x=0, y=0, text=self.currentInput)

    @property
    def value(self):
        if self.currentInput == "":
            return 0
        return float(self.currentInput)

    def set_value(self, new):
        self.currentInput = str(new)

    def draw(self):
        if not self.active: return

        main = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

        pygame.draw.rect(self.game.screen, self.color, main)


        # draw text
        self.textW.set_text(self.currentInput)
        self.textW.screenAnchor = self.screenAnchor
        w = self.textW.get_width()
        h = self.textW.get_height()
        tx = self.x + 10 # (self.w/2) - (w/2)
        ty = self.y + (self.h/2) - (h/2) + 40

        self.textW.screenAnchor = self.screenAnchor
        self.textW.set_position(tx, ty)
        self.textW.update()

        self.textC.set_text(self.caption)
        self.textC.screenAnchor = self.screenAnchor
        tx = self.x
        ty = self.y
        self.textC.set_position(tx, ty)
        self.textC.update()

    def update(self):
        super().update()

        if not self.active: return

        # focus/unfocus
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h*2)
            if pygame.Rect(mx-15, my-15, 30, 30).colliderect(rect):
                self.focused = True
            else:
                self.focused = False

                if self.value <= self.minVal:
                    self.set_value(self.minVal)
                if self.value >= self.maxVal:
                    self.set_value(self.maxVal)

        # decide color
        if self.focused:
            self.color = self.focusColor
        else:
            self.color = self.bg

        # input
        if self.focused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if not event.key == pygame.K_BACKSPACE and len(self.currentInput) < 6:
                        strk = pygame.key.name(event.key)
                        if strk in "0123456789":
                            self.currentInput += strk

                        if strk == ".":
                            if "." not in self.currentInput:
                                self.currentInput += "."

                    elif event.key == pygame.K_BACKSPACE:
                        self.currentInput = self.currentInput[:-1]

        # draw
        self.draw()


# button gui class
class Button(Element):
    def __init__(self, gui, x=0, y=0, w=180, h=50, bg=(30, 200, 80), hbg=(30, 220, 140), fg=(255, 255, 255), text="Button", onLeftClick=None, parent=None):
        super().__init__(gui, x, y, w, h, parent)
        self.bg = bg
        self.hbg = hbg
        self.fg = fg
        self.text = text

        self.game = self.gui.game

        # style configure
        self.shadowDepth = 6
        self.dropSpeed = 0.1

        # state
        self.pressed = False
        self.currentDrop = 0
        self.currentColor = self.bg

        # text
        self.textW = Text(self.gui, x=self.x, y=self.y, text=self.text)

        # click
        self.canClick = False
        self.canClickTimer = Timer(self.game, 60, self.can_click, False)
        self.game.add_timer_not_tick(self.canClickTimer)
        self.canClickTimer.start()

        self.onClickTimer = Timer(self.game, 5, None, False)
        self.game.add_timer_not_tick(self.onClickTimer)

        self.onLeftClick = onLeftClick

    def can_click(self):
        self.canClick = True

    def cant_click(self):
        self.canClick = False
        self.canClickTimer.start()

    def on_click(self):
        self.canClickTimer.start()
        if self.onLeftClick is not None:
            self.onLeftClick()
        self.canClick = False

    def set_text(self, text):
        self.text = text
        self.textW.set_text(text)

    def set_on_click(self, func):
        self.onClickTimer.callback = func

    def draw(self):
        if not self.active: return

        main = pygame.Rect(self.rect.x, self.rect.y+self.currentDrop, self.rect.w, self.rect.h)
        shadow = pygame.Rect(self.rect.x, self.rect.y+self.shadowDepth, self.rect.w, self.rect.h)

        pygame.draw.rect(self.game.screen, (0, 0, 0), shadow, 0, 5)
        pygame.draw.rect(self.game.screen, self.currentColor, main, 0, 5)


        # text
        self.textW.set_text(self.text)
        self.textW.screenAnchor = self.screenAnchor
        w = self.textW.get_width()
        h = self.textW.get_height()
        tx = self.x + (self.w/2) - (w/2)
        ty = self.y + (self.h/2) - (h/2) + self.currentDrop

        self.textW.screenAnchor = self.screenAnchor
        self.textW.set_position(tx, ty)
        self.textW.update()

    def update(self):
        super().update()

        if not self.active: return

        # draw
        self.draw()

        # animation
        if self.hovered:
            self.currentColor = self.hbg

            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.currentColor = self.bg
            self.pressed = False

        if self.pressed:
            self.currentDrop += self.dropSpeed * self.game.dt
        else:
            self.currentDrop -= self.dropSpeed * self.game.dt

        if self.currentDrop >= self.shadowDepth:
            self.currentDrop = self.shadowDepth
        if self.currentDrop <= 0:
            self.currentDrop = 0

        # on click
        if self.canClick:
            if self.hovered:
                if pygame.mouse.get_pressed()[0]:
                    self.on_click()
                    self.canClick = False
