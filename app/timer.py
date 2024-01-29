

# custom timer class
class Timer:
    def __init__(self, game, duration, callback, loop=True):
        self.game = game
        self.duration = duration
        self.callback = callback
        self.loop = loop

        # timer state
        self.current = self.duration
        self.active = False

    # start the timer
    def start(self):
        self.active = True
        self.current = self.duration

    # update/countdown the timer
    def countdown(self):
        if self.active:
            self.current -= 1
            if self.current <= 0:
                # run callback function
                if self.callback is not None:
                    self.callback()

                # reset (if looping)
                if self.loop:
                    self.current = self.duration
                else:
                    self.current = self.duration
                    self.active = False
