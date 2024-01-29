from app.gui import *


# reinit/settings gui
class ReinitGUI(GUI):
    def __init__(self, game):
        super().__init__(game)

        self.visible = False

        # gui pos
        self.x = 0
        self.y = 0

        # general settings
        self.frmBackground = Frame(self, x=0, y=0, w=self.game.window.w, h=self.game.window.h, color=(20, 20, 20))
        self.frmForm = Frame(self, x=-525/2, y=-600/2, w=525, h=600, parent=self.frmBackground, color=(35, 35, 35))
        self.frmForm.screenAnchor = [0.5, 0.5]

        self.txtForm = Text(self, x=10, y=10, text="Settings", fontSize=50, parent=self.frmForm)

        self.nibMapWidth = NumberInputBox(self, x=150, y=200, caption="Map Width", minVal=17, maxVal=999999)
        self.nibMapHeight = NumberInputBox(self, x=400, y=200, caption="Map Height", minVal=17, maxVal=999999)

        self.nibBobs = NumberInputBox(self, x=150, y=270, caption="Bobs", minVal=1, maxVal=999999, parent=self.frmBackground)
        self.nibFood = NumberInputBox(self, x=400, y=270, caption="Food", minVal=1, maxVal=999999, parent=self.frmBackground)

        self.nibDayLength = NumberInputBox(self, x=150, y=340, caption="Day Length", minVal=5, maxVal=100000)

        self.chkParthenoRepr = Checkbox(self, x=150, y=420, text="Parthenogenesis Reproduction", parent=self.frmBackground)
        self.chkSexualRepr = Checkbox(self, x=150, y=480, text="Sexual Reproduction", parent=self.frmBackground)

        # set values
        self.nibMapWidth.set_value(50)
        self.nibMapHeight.set_value(50)
        self.nibFood.set_value(200)
        self.nibBobs.set_value(50)
        self.nibDayLength.set_value(100)

        # genetic settings
        self.txtValueRange = Text(self, x=150, y=185, text="Bob Genetics Settings")
        self.nibMinVel = NumberInputBox(self, x=150, y=200+30, caption="Min Velocity", minVal=0, maxVal=999999)
        self.nibMaxVel = NumberInputBox(self, x=450, y=200+30, caption="Max Velocity", minVal=0, maxVal=999999)
        self.nibMinMass = NumberInputBox(self, x=150, y=300+30, caption="Min Mass", minVal=0, maxVal=999999)
        self.nibMaxMass = NumberInputBox(self, x=450, y=300+30, caption="Max Mass", minVal=0, maxVal=999999)
        self.nibMinPerc = NumberInputBox(self, x=150, y=400+30, caption="Min Perception", minVal=0, maxVal=999999)
        self.nibMaxPerc = NumberInputBox(self, x=450, y=400+30, caption="Max Perception", minVal=0, maxVal=999999)

        self.nibMinVel.set_value(0.8)
        self.nibMaxVel.set_value(2.0)
        self.nibMinMass.set_value(0.4)
        self.nibMaxMass.set_value(2.5)
        self.nibMinPerc.set_value(3)
        self.nibMaxPerc.set_value(18)

        # buttons
        self.btnApply = Button(self, 470, 640, text="Apply", onLeftClick=self.apply, parent=self.frmBackground)
        self.btnClose = Button(self, 280, 640, text="Close", onLeftClick=self.close, bg=(200, 30, 80), hbg=(220, 140, 30), parent=self.frmBackground)
        self.btnSwitch = Button(self, x=470, y=110, text="Genetics", onLeftClick=self.switch_tab, parent=self.frmBackground)

        # current settings
        self.current = "general"

    # switch tabs
    def switch_tab(self):
        if self.current == "general":
            self.current = "genetic"
            self.btnSwitch.set_text("General")
            return
        else:
            self.current = "general"
            self.btnSwitch.set_text("Genetics")
            return

    # button event for applying the new settings and reiniting the game
    def apply(self):
        mapW = int(self.nibMapWidth.value)
        mapH = int(self.nibMapHeight.value)
        bobsAm = int(self.nibBobs.value)
        foodAm = int(self.nibFood.value)
        dayL = int(self.nibDayLength.value)
        parth = self.chkParthenoRepr.value
        sex = self.chkSexualRepr.value

        minVel = self.nibMinVel.value
        maxVel = self.nibMaxVel.value
        minMass = self.nibMinMass.value
        maxMass = self.nibMaxMass.value
        minPerc = int(self.nibMinPerc.value)
        maxPerc = int(self.nibMaxPerc.value)

        self.game.reinit(mapW, mapH, bobsAm, foodAm, dayL, parth, sex, minVel, maxVel, minMass, maxMass, minPerc, maxPerc)
        self.close()

    # close this gui
    def close(self):
        self.visible = False
        self.game.menuGUI.visible = True

    # update this gui
    def update(self):
        # draw all elements
        self.draw_element(self.frmBackground)
        self.draw_element(self.frmForm)
        self.draw_element(self.txtForm)

        if self.current == "general":
            self.draw_element(self.nibMapWidth)
            self.draw_element(self.nibMapHeight)

            self.draw_element(self.nibBobs)
            self.draw_element(self.nibFood)

            self.draw_element(self.nibDayLength)

            self.draw_element(self.chkParthenoRepr)
            self.draw_element(self.chkSexualRepr)

        if self.current == "genetic":
            self.draw_element(self.txtValueRange)
            self.draw_element(self.nibMinVel)
            self.draw_element(self.nibMaxVel)
            self.draw_element(self.nibMinMass)
            self.draw_element(self.nibMaxMass)
            self.draw_element(self.nibMinPerc)
            self.draw_element(self.nibMaxPerc)

        self.draw_element(self.btnApply)
        self.draw_element(self.btnClose)
        self.draw_element(self.btnSwitch)
