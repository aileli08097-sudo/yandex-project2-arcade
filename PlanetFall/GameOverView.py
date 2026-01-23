import arcade
from pyglet.graphics import Batch


class GameOverView(arcade.View):
    def __init__(self, game_view, state):
        super().__init__()
        self.level = state['level']
        self.player = state['player']
        self.player_num = state['player_num']
        self.items = state['items']
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
        self.space_text = arcade.Text("Чтобы начать заново, нажмите P", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.space_text1 = arcade.Text("Чтобы выйти в меню, нажмите ESC", self.window.width / 2,
                                       self.window.height / 2 - 100,
                                       arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from MenuView import MenuView
            menu_view = MenuView(items=self.items)
            menu_view.setup()
            self.window.show_view(menu_view)
        elif key == arcade.key.P:
            state = {'level': self.level,
                     'player': self.player,
                     'player_num': self.player_num,
                     'enemies': arcade.SpriteList(),
                     'items': self.items,
                     'coll_items': arcade.SpriteList()}
            from StartGameView import StartGameView
            start_game_view = StartGameView(state=state)
            self.window.show_view(start_game_view)
