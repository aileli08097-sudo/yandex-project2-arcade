import arcade
from pyglet.graphics import Batch


class GameOverView(arcade.View):
    def __init__(self, game_view, level, player):
        super().__init__()
        self.level = level
        self.player = player
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
        self.main_text = arcade.Text("ПОРАЖЕНИЕ", self.window.width / 2, self.window.height / 2,
                                     arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Чтобы продолжить, нажмите SPACE", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.space_text1 = arcade.Text("Чтобы выйти в меню, нажмите ESC", self.window.width / 2,
                                       self.window.height / 2 - 100,
                                       arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from MenuView import MenuView
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)
        elif key == arcade.key.SPACE:
            from StartGameView import StartGameView
            start_game_view = StartGameView(level=self.level, player=self.player)
            self.window.show_view(start_game_view)