import arcade

class Item(arcade.Sprite):
    def __init__(self, filename, scale=1, typ=10):
        super().__init__(filename, scale)
        self.typ = typ