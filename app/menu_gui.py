import os

from app.gui import *


# GUI for the Menu
class MenuGUI(GUI):
    def __init__(self, game):
        super().__init__(game)

        # gui pos
        self.x = 0
        self.y = 0

        # elements
        self.txtMultiplier = Text(self, x=self.game.window.w-60, y=10, text="1.0x")

        self.btnOpen = Button(self, 10, 10, text="Menu", onLeftClick=self.open)

        self.frmMenu = Frame(self, x=0, y=0, w=300, h=self.game.window.h, color=(80, 80, 80))
        self.frmMenu.active = False

        self.txtDay = Text(self, x=10, y=120 + 80, text="Day: 0", parent=self.frmMenu)
        self.txtBobs = Text(self, x=10, y=120 + 110, text="Bobs: 0", parent=self.frmMenu)
        self.txtFood = Text(self, x=10, y=120 + 140, text="Food: 0", parent=self.frmMenu)

        self.sldSpeed = Slider(self, x=10, y=120 + 180, w=275, caption="Tick Speed", parent=self.frmMenu, minVal=0.1, maxVal=15)
        self.sldSpeed.curVal = 1

        self.btnClose = Button(self, 10, 10, text="Close", onLeftClick=self.close, bg=(200, 30, 80), hbg=(220, 140, 30), parent=self.frmMenu)

        self.btnPause = Button(self, 10, 70, text="Pause", onLeftClick=self.pause, parent=self.frmMenu)
        self.btnReinit = Button(self, x=10, y=130, text="Reinit", onLeftClick=self.reinit_open, parent=self.frmMenu, bg=(200, 30, 200), hbg=(140, 30, 220))

        # file
        self.txtFile = Text(self, x=10, y=-250, text="File", parent=self.frmMenu)
        self.txtFile.screenAnchor = [0, 1]
        self.btnOpenFile = Button(self, x=10, y=-220, text="Open", onLeftClick=self.game.savefile.ask_file, parent=self.frmMenu)
        self.btnOpenFile.screenAnchor = [0, 1]
        self.btnSaveFile = Button(self, x=10, y=-160, text="Save As", onLeftClick=self.game.savefile.save_as, parent=self.frmMenu)
        self.btnSaveFile.screenAnchor = [0, 1]
        self.btnManualSaveFile = Button(self, x=10, y=-100, text="Save", onLeftClick=self.game.savefile.save, parent=self.frmMenu)
        self.btnManualSaveFile.screenAnchor = [0, 1]

    # pause the game button function
    def pause(self):
        if self.game.pauseTick:
            self.game.pauseTick = False
            return
        else:
            self.game.pauseTick = True
            return

    # close menu
    def close(self):
        self.btnOpen.active = True
        self.frmMenu.active = False
        self.btnOpen.cant_click()

    # open menu
    def open(self):
        self.btnOpen.active = False
        self.frmMenu.active = True
        self.btnClose.cant_click()

    # open the settings/reinit menu
    def reinit_open(self):
        self.game.reinitGUI.visible = True
        self.visible = False

    # update the menu gui
    def update(self):
        # draw elements
        self.draw_element(self.btnOpen)

        self.draw_element(self.frmMenu)
        self.draw_element(self.btnClose)
        self.draw_element(self.btnPause)
        self.draw_element(self.btnReinit)

        # set text
        self.txtDay.set_text(f"Day: {self.game.currentDay} ({self.game.dayTimer.current}/{self.game.dayTimer.duration})")
        self.txtBobs.set_text(f"Bobs: {self.game.tilemap.get_bobs_count()}")
        self.txtFood.set_text(f"Food: {len(self.game.tilemap.foods)}")

        # draw
        self.draw_element(self.txtDay)
        self.draw_element(self.txtBobs)
        self.draw_element(self.txtFood)

        self.draw_element(self.sldSpeed)

        # set the time multiplier text
        if not self.game.pauseTick:
            self.txtMultiplier.x = self.game.window.w - 60
            self.txtMultiplier.set_text(f"{str(self.game.tickSpeedMult)[:3]}x")
        else:
            self.txtMultiplier.x = self.game.window.w - 130
            self.txtMultiplier.set_text("PAUSED")
        self.draw_element(self.txtMultiplier)

        # save file
        if self.game.savefile.current is None:
            self.txtFile.set_text(f"File: None")
        else:
            fname = self.game.savefile.current.path
            fname = os.path.basename(fname)
            fname = fname.replace(f".{self.game.extension}", "")
            self.txtFile.set_text(f"File: {fname}")
        self.draw_element(self.txtFile)
        self.draw_element(self.btnOpenFile)
        self.draw_element(self.btnSaveFile)
        self.draw_element(self.btnManualSaveFile)

        # tick speed
        self.game.tickSpeedMult = self.sldSpeed.curVal
