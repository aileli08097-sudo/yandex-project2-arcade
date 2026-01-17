import arcade

class Level(arcade.View):
    def setup(self, level, player):
        self.level = level
        self.player = player


    def on_draw(self):
        self.clear()