import arcade
import sqlite3
import os
from pyglet.graphics import Batch


class LaunchView(arcade.View):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.start = False
        self.background_player = None
        self.background_music = None
        self.batch = Batch()
        self.main_text = arcade.Text("Вы - пришелец-космонавт, полетевший изучать свою вселенную.",
                                     self.window.width / 2, self.window.height / 2,
                                     arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                     batch=self.batch)
        self.main_text1 = arcade.Text("При приземлении ваш корабль разбился, а все его части разлетелись по планетам.",
                                      self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                      batch=self.batch)
        self.main_text2 = arcade.Text("Соберите их, чтобы вернуться домой!",
                                      self.window.width / 2, self.window.height / 2 - 100,
                                      arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                      batch=self.batch)
        self.main_text3 = arcade.Text("PlanetFall",
                                      self.window.width / 2, self.window.height / 2 + 50,
                                      arcade.color.WHITE, font_name='Algerian', font_size=30, anchor_x="center",
                                      batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_update(self, delta_time):
        if not self.start:
            self.timer += delta_time
            if self.timer > 4.0:
                self.start = True
                from MenuView import MenuView
                menu_view = MenuView()
                menu_view.setup()
                self.window.show_view(menu_view)
                arcade.stop_sound(self.background_player)

    def on_show_view(self):
        super().on_show_view()
        self.background_music = arcade.load_sound(f'sounds/launch.mp3')
        self.background_player = self.background_music.play(volume=0.5)
