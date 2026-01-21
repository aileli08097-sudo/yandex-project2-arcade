import arcade
from pyglet.graphics import Batch


class WinView(arcade.View):
    def __init__(self, game_view, time, level, player, player_num, items):
        super().__init__()
        self.time = time
        self.level = level
        self.player = player
        self.player_num = player_num
        self.items = items
        self.background_view = game_view
        self.batch = Batch()
        self.all_sprites = arcade.SpriteList()
        shadow = arcade.Sprite('images/rocket_shadow.png', 0.3)
        shadow.center_x = self.width // 2
        shadow.center_y = self.height // 2 + 200
        self.all_sprites.append(shadow)
        for item in self.items:
            item.scale = 0.3
            item.center_x = self.width // 2
            item.center_y = self.height // 2 + 200
            self.all_sprites.append(item)

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
        self.all_sprites.draw()
        self.main_text = arcade.Text("ПОБЕДА", self.window.width / 2, self.window.height / 2,
                                     arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
        self.main_text1 = arcade.Text(
            f"Время прохождения: {self.time} секунд  Собрано элементов корабля: {len(self.items)}/2",
            self.window.width / 2, self.window.height / 2 + 50,
            arcade.color.WHITE, font_size=15, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Чтобы перейти к следующему уровню, нажмите P", self.window.width / 2,
                                      self.window.height / 2 - 100,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.space_text1 = arcade.Text("Чтобы выйти в меню, нажмите ESC", self.window.width / 2,
                                       self.window.height / 2 - 150,
                                       arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.space_text2 = arcade.Text("Чтобы переиграть, нажмите Q", self.window.width / 2,
                                       self.window.height / 2 - 50,
                                       arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from MenuView import MenuView
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)
        elif key == arcade.key.P:
            from StartGameView import StartGameView
            start_game_view = StartGameView(level=self.level + 1, player=self.player, player_num=self.player_num)
            self.window.show_view(start_game_view)
        elif key == arcade.key.Q:
            from StartGameView import StartGameView
            start_game_view = StartGameView(level=self.level, player=self.player, player_num=self.player_num)
            self.window.show_view(start_game_view)
