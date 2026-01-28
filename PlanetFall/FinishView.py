import os
import sqlite3

import arcade
from pyglet.graphics import Batch

from PlanetFall.items import Item


class FinishView(arcade.View):
    def __init__(self, time, state):
        super().__init__()
        self.con = sqlite3.connect('planetfall_db.sqlite')
        self.background_music = None
        self.background_player = None
        self.time = time
        self.level = state['level']
        self.all_sprites = arcade.SpriteList()
        self.player_num = state['player_num']
        self.items = state['items']
        self.coll_items = state['coll_items']
        tile_map = arcade.load_tilemap(f'maps/finish.tmx')
        self.scene = arcade.Scene.from_tilemap(tile_map)
        self.ground = self.scene['ground']
        self.batch = Batch()
        for x in self.items:
            if x > 7:
                fire = arcade.Sprite('images/rocket_fire.png', 0.7)
                fire.center_x = self.width // 2 - 200
                fire.center_y = self.height // 2 + 64
                fire.angle = 45
                self.all_sprites.append(fire)
        shadow = arcade.Sprite('images/rocket_shadow.png', 0.7)
        shadow.center_x = self.width // 2 - 200
        shadow.center_y = self.height // 2 + 100
        self.all_sprites.append(shadow)
        for x in self.items:
            if x < 8:
                item = Item(f'images/items/item_{x}.png', typ=x)
                item.scale = 0.7
                item.center_x = self.width // 2 - 200
                item.center_y = self.height // 2 + 100
                item.angle = 0
                self.all_sprites.append(item)
        for x in self.coll_items:
            if x < 8:
                item = Item(f'images/items/item_{x}.png', typ=x)
                item.scale = 0.7
                item.center_x = self.width // 2 - 200
                item.center_y = self.height // 2 + 100
                item.angle = 0
                self.all_sprites.append(item)
        self.items += self.coll_items
        self.items = list(set(self.items))

        self.player_list = arcade.SpriteList()
        self.player = arcade.Sprite(f'images/Alien{self.player_num}/alien{self.player_num}_4.png')
        self.player.center_x = self.window.width // 2 - 100
        self.player.center_y = self.window.height // 2
        self.player_list.append(self.player)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=0.7,
            walls=self.ground
        )

    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_draw(self):
        self.clear()
        self.ground.draw()
        self.all_sprites.draw()
        self.player_list.draw()
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.window.width // 2,
                             self.window.height // 2,
                             self.window.width,
                             self.window.height),
            (0, 0, 0, 150)
        )
        self.main_text = arcade.Text("ПОБЕДА", self.window.width / 2, self.window.height / 2,
                                     arcade.color.WHITE, font_name='Times New Roman', font_size=30, anchor_x="center",
                                     batch=self.batch)
        if len(self.items) == 10:
            self.main_text2 = arcade.Text("Вы прошли все уровни и собрали все части корабля!", self.window.width / 2, self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                          batch=self.batch)
        else:
            self.main_text2 = arcade.Text("Вы прошли все уровни, но не собрали все части корабля!", self.window.width / 2,
                                          self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_name='Lucida console', font_size=15,
                                          anchor_x="center",
                                          batch=self.batch)
        self.main_text1 = arcade.Text(
            f"Время прохождения: {self.time} сек  Собрано элементов корабля за этот уровень: {len(self.coll_items)}/2",
            self.window.width / 2, self.window.height / 2 + 100,
            arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center", batch=self.batch)

        self.main_text3 = arcade.Text(f"Собрано элементов корабля всего: {len(self.items)}/10",
                                      self.window.width / 2, self.window.height / 2 + 50,
                                      arcade.color.WHITE, font_size=15, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Чтобы сбросить прогресс, нажмите P", self.window.width / 2,
                                      self.window.height / 2 - 150,
                                      arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                      batch=self.batch)
        self.space_text1 = arcade.Text("Чтобы выйти в меню, нажмите ESC", self.window.width / 2,
                                       self.window.height / 2 - 200,
                                       arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                       batch=self.batch)
        self.space_text2 = arcade.Text("Чтобы переиграть, нажмите Q", self.window.width / 2,
                                       self.window.height / 2 - 100,
                                       arcade.color.WHITE, font_name='Lucida console', font_size=15, anchor_x="center",
                                       batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.stop_sound(self.background_player)
            for x in self.coll_items:
                if x not in self.items:
                    self.items.append(x)
                    query = f"INSERT INTO collected_items(type) VALUES ('{x}')"
                    cur = self.con.cursor()
                    cur.execute(query)
                    self.con.commit()
            from MenuView import MenuView
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)
        elif key == arcade.key.P:
            arcade.stop_sound(self.background_player)
            self.con.close()
            os.remove('planetfall_db.sqlite')
            from MenuView import MenuView
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)
        elif key == arcade.key.Q:
            state = {'level': self.level,
                     'player': self.player,
                     'player_num': self.player_num,
                     'enemies': arcade.SpriteList(),
                     'items': self.items,
                     'coll_items': arcade.SpriteList()}
            arcade.stop_sound(self.background_player)
            from StartGameView import StartGameView
            start_game_view = StartGameView(state=state)
            self.window.show_view(start_game_view)

    def on_show_view(self):
        super().on_show_view()
        self.background_music = arcade.load_sound(f'sounds/finish.mp3')
        self.background_player = self.background_music.play(loop=True, volume=0.5)
