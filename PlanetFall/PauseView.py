import arcade
from pyglet.graphics import Batch


class PauseView(arcade.View):
    def __init__(self, game_view, game_state):
        super().__init__()
        self.background_music = None
        self.background_player = None
        self.game_view = game_view
        self.game_state = game_state
        self.background_view = game_view
        self.batch = Batch()

    def on_draw(self):
        self.clear()
        self.background_view.on_draw()
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.window.width // 2,
                             self.window.height // 2,
                             self.window.width,
                             self.window.height),
            (0, 0, 0, 180)
        )
        self.main_text = arcade.Text("Уровень приостановлен", self.window.width / 2, self.window.height / 2,
                                     arcade.color.WHITE, font_name='Times New Roman', font_size=30, anchor_x="center",
                                     batch=self.batch)
        self.space_text = arcade.Text("Чтобы продолжить, нажмите P", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                      batch=self.batch)
        self.space_text1 = arcade.Text("Чтобы выйти в меню, нажмите ESC", self.window.width / 2,
                                       self.window.height / 2 - 100,
                                       arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                       batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.stop_sound(self.background_player)
            from MenuView import MenuView
            menu_view = MenuView(items=self.game_state['items'])
            menu_view.setup()
            self.window.show_view(menu_view)
        elif key == arcade.key.P:
            arcade.stop_sound(self.background_player)
            self.game_view.restore_state(self.game_state)
            self.window.show_view(self.game_view)

    def on_show_view(self):
        super().on_show_view()
        self.background_music = arcade.load_sound(f'sounds/pause.mp3')
        self.background_player = self.background_music.play(loop=True, volume=0.5)
