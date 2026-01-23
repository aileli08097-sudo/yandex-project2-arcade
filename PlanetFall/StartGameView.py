import arcade
from pyglet.graphics import Batch


class StartGameView(arcade.View):
    def __init__(self, state):
        super().__init__()
        self.timer = 0
        self.level = state['level']
        self.player = state['player']
        self.player_num = state['player_num']
        self.items_list = arcade.SpriteList()
        items = state['items']
        for x in set(items):
            self.items_list.append(x)
        self.player.center_x = 100
        self.player.center_y = 1700
        self.batch = Batch()
        self.planet_textures = [
            'images/planets/planet00.png',
            'images/planets/planet03.png',
            'images/planets/planet04.png',
            'images/planets/planet06.png',
            'images/planets/planet09.png',
        ]
        self.planet_list = arcade.SpriteList()
        self.start = False
        if self.level == 0:
            self.main_text = arcade.Text("Уровень первый", self.window.width / 2, self.window.height / 2,
                                         arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
            self.space_text = arcade.Text("Планета Cryon(Крион)", self.window.width / 2,
                                          self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
            self.planet_list.append(arcade.Sprite(self.planet_textures[0]))
        elif self.level == 1:
            self.main_text = arcade.Text("Уровень второй", self.window.width / 2, self.window.height / 2,
                                         arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
            self.space_text = arcade.Text("Планета Silvana(Сильвана)", self.window.width / 2,
                                          self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

            self.planet_list.append(arcade.Sprite(self.planet_textures[1]))
        elif self.level == 2:
            self.main_text = arcade.Text("Уровень третий", self.window.width / 2, self.window.height / 2,
                                         arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
            self.space_text = arcade.Text("Планета Ash-7(Аш-7)", self.window.width / 2,
                                          self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

            self.planet_list.append(arcade.Sprite(self.planet_textures[2]))
        elif self.level == 3:
            self.main_text = arcade.Text("Уровень четвёртый", self.window.width / 2, self.window.height / 2,
                                         arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
            self.space_text = arcade.Text("Планета Konfetti(Конфетти)", self.window.width / 2,
                                          self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

            self.planet_list.append(arcade.Sprite(self.planet_textures[3]))
        elif self.level == 4:
            self.main_text = arcade.Text("Уровень пятый", self.window.width / 2, self.window.height / 2,
                                         arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
            self.space_text = arcade.Text("Планета Arcanus(Арканус)", self.window.width / 2,
                                          self.window.height / 2 - 50,
                                          arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

            self.planet_list.append(arcade.Sprite(self.planet_textures[4]))
        for sprite in self.planet_list:
            sprite.center_x = self.width // 2
            sprite.center_y = self.height // 2
            sprite.alpha = 191
            sprite.scale = 0.5

        self.saved_state = {'level': self.level,
                            'player': self.player,
                            'player_num': self.player_num,
                            'enemies': arcade.SpriteList(),
                            'items': self.items_list,
                            'coll_items': arcade.SpriteList()}

    def on_draw(self):
        self.clear()

        self.planet_list.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        if not self.start:
            self.timer += delta_time
            if self.timer > 2.0:
                self.start = True
                if self.level == 0:
                    from PlanetFall.levels.level_0 import Level_0
                    level_view = Level_0(saved_state=self.saved_state)
                    level_view.setup()
                    self.window.show_view(level_view)
                elif self.level == 1:
                    from PlanetFall.levels.level_1 import Level_1
                    level_view = Level_1(saved_state=self.saved_state)
                    level_view.setup()
                    self.window.show_view(level_view)
                elif self.level == 2:
                    from PlanetFall.levels.level_2 import Level_2
                    level_view = Level_2(saved_state=self.saved_state)
                    level_view.setup()
                    self.window.show_view(level_view)
                elif self.level == 3:
                    from PlanetFall.levels.level_3 import Level_3
                    level_view = Level_3(saved_state=self.saved_state)
                    level_view.setup()
                    self.window.show_view(level_view)
                elif self.level == 4:
                    from PlanetFall.levels.level_4 import Level_4
                    level_view = Level_4(saved_state=self.saved_state)
                    level_view.setup()
                    self.window.show_view(level_view)
