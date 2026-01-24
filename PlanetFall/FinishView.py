import arcade
from pyglet.graphics import Batch


class FinishView(arcade.View):
    def __init__(self, time, state):
        super().__init__()
        self.time = time
        self.level = state['level']
        self.player = state['player']
        self.player.center_x = self.window.width // 2
        self.player.center_y = self.window.height // 2
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.player)
        self.player_num = state['player_num']
        self.items = state['items']
        self.coll_items = state['coll_items']
        tile_map = arcade.load_tilemap(f'maps/finish.tmx')
        self.scene = arcade.Scene.from_tilemap(tile_map)
        self.ground = self.scene['ground']
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=0.7,
            walls=self.ground
        )
        self.batch = Batch()
        fire = arcade.Sprite('images/rocket_fire.png', 0.7)
        fire.center_x = self.width // 2 - 200
        fire.center_y = self.height // 2 + 100
        fire.angle = 45
        self.all_sprites.append(fire)
        shadow = arcade.Sprite('images/rocket_shadow.png', 0.7)
        shadow.center_x = self.width // 2 - 200
        shadow.center_y = self.height // 2 + 100
        self.all_sprites.append(shadow)
        for item in self.items:
            if item.name == 'item':
                item.scale = 0.7
                item.center_x = self.width // 2 - 200
                item.center_y = self.height // 2 + 100
                item.angle = 0
                self.all_sprites.append(item)
        for item in self.coll_items:
            if item.name == 'item':
                item.scale = 0.7
                item.center_x = self.width // 2 - 200
                item.center_y = self.height // 2 + 100
                item.angle = 0
                self.all_sprites.append(item)

    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_draw(self):
        self.clear()
        self.ground.draw()
        self.all_sprites.draw()
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.window.width // 2,
                             self.window.height // 2,
                             self.window.width,
                             self.window.height),
            (0, 0, 0, 150)
        )
        self.main_text = arcade.Text("ПОБЕДА", self.window.width / 2, self.window.height / 2,
                                     arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
        self.main_text2 = arcade.Text("Вы прошли все уровни!", self.window.width / 2, self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.main_text1 = arcade.Text(
            f"Время прохождения: {self.time} сек  Собрано элементов корабля за этот уровень: {len(self.coll_items)}/2",
            self.window.width / 2, self.window.height / 2 + 100,
            arcade.color.WHITE, font_size=15, anchor_x="center", batch=self.batch)


        self.main_text3 = arcade.Text(f"Собрано элементов корабля всего: {len(self.coll_items) + len(self.items)}/10",
                           self.window.width / 2, self.window.height / 2 + 50,
                           arcade.color.WHITE, font_size=15, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Чтобы сбросить прогресс, нажмите P", self.window.width / 2,
                                      self.window.height / 2 - 150,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.space_text1 = arcade.Text("Чтобы выйти в меню, нажмите ESC", self.window.width / 2,
                                       self.window.height / 2 - 200,
                                       arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.space_text2 = arcade.Text("Чтобы переиграть, нажмите Q", self.window.width / 2,
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
            ...
        elif key == arcade.key.Q:
            state = {'level': self.level,
                     'player': self.player,
                     'player_num': self.player_num,
                     'enemies': arcade.SpriteList(),
                     'items': self.items,
                     'coll_items': arcade.SpriteList()}
            from StartGameView import StartGameView
            start_game_view = StartGameView(state=state)
            self.window.show_view(start_game_view)
