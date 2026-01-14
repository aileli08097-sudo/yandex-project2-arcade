import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, TILE_SIZE
from player import Player


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.SKY_BLUE

        # Спрайты
        self.player = None
        self.tile_list = None
        self.cactus_list = None
        self.physics_engine = None

        # Камера
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        # Игровые переменные
        self.game_over = False
        self.paused = False

    def setup(self):
        ...

    def on_draw(self):
        ...

    def on_update(self, delta_time):
        ...

    def on_key_press(self, key, modifiers):
        ...
