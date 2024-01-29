from app.game import *
def main():
    game = Game()

    while game.running:
        game.update()
    


