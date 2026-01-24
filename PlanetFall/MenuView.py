import random
from dataclasses import dataclass
import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIDropdown
from pyglet.graphics import Batch
from constants import *
from arcade.particles import FadeParticle, Emitter, EmitMaintainCount
from pyglet.event import EVENT_HANDLE_STATE
from StartGameView import StartGameView


def make_trail(attached_sprite, maintain=60):
    emit = Emitter(
        center_xy=(attached_sprite.center_x, attached_sprite.center_y),
        emit_controller=EmitMaintainCount(maintain),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.make_soft_circle_texture(20, arcade.color.WHITE),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.6),
            lifetime=random.uniform(0.35, 0.6),
            start_alpha=220, end_alpha=0,
            scale=random.uniform(0.25, 0.4),
        ),
    )

    emit._attached = attached_sprite
    return emit


@dataclass
class InputState:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False


class Star(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(':resources:images/items/star.png')
        self.scale = 0.3

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_x -= 1
        self.center_y -= 2


class MenuView(arcade.View):
    def __init__(self, items=arcade.SpriteList(), options=['Первый', 'Второй', 'Третий']):
        super().__init__()
        self.background_color = arcade.color.BLACK

        self.batch = Batch()
        self.main_text = arcade.Text("Главное Меню", self.window.width / 2, self.window.height - 50,
                                     arcade.color.WHITE, font_size=30, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Выберите героя", self.window.width / 4,
                                      self.window.height - 100,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.enemies_list = arcade.SpriteList()
        items = items
        self.items_list = arcade.SpriteList()
        for x in set(items):
            self.items_list.append(x)
        self.option_list1 = options
        self.player_textures = [
            'images/aliens/alienBeige_badge1.png',
            'images/aliens/alienBlue_badge1.png',
            'images/aliens/alienGreen_badge1.png',
            'images/aliens/alienPink_badge1.png',
            'images/aliens/alienYellow_badge1.png'
        ]
        self.player_num = random.randint(0, 4)
        self.players = [
            'images/Alien0/alien0_4.png',
            'images/Alien1/alien1_4.png',
            'images/Alien2/alien2_4.png',
            'images/Alien3/alien3_4.png',
            'images/Alien4/alien4_4.png'
        ]
        self.player = arcade.Sprite(self.players[self.player_num])

        self.all_sprites = arcade.SpriteList()

        self.space_text1 = arcade.Text("Выберите уровень", self.window.width * 3 / 4,
                                       self.window.height - 100,
                                       arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.planet_textures = [
            'images/planets/planet00.png',
            'images/planets/planet03.png',
            'images/planets/planet04.png',
            'images/planets/planet06.png',
            'images/planets/planet09.png',
        ]
        self.planet = 0

        self.text = arcade.Text("Нажмите любую клавишу, чтобы начать", self.window.width / 2,
                                self.window.height / 4 - 100,
                                arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)
        self.menu = True

    def setup(self):
        for i in range(5):
            p = arcade.Sprite(self.player_textures[i])
            p.center_x = self.width / 2.5 - 10
            p.center_y = 500 - i * 60
            self.all_sprites.append(p)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout(width=self.width,
                                            height=self.height)
        self.box_layout = UIBoxLayout(vertical=True, space_between=30,
                                      align="center")

        label = UILabel(text="Герой первый",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=40
                        )
        self.box_layout.add(label)
        label = UILabel(text="Герой второй",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=40
                        )
        self.box_layout.add(label)
        label = UILabel(text="Герой третий",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=40
                        )
        self.box_layout.add(label)
        label = UILabel(text="Герой четвёртый",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=40
                        )
        self.box_layout.add(label)
        label = UILabel(text="Герой пятый",
                        font_size=20,
                        text_color=arcade.color.WHITE,
                        width=40
                        )
        self.box_layout.add(label)

        self.option_list = ["Случайный", "Первый", "Второй", "Третий", 'Четвёртый', 'Пятый']
        self.dropdown = UIDropdown(options=self.option_list, width=200)
        self.dropdown.on_change = self.on_change
        self.box_layout.add(self.dropdown)

        self.anchor_layout.add(self.box_layout, anchor_x="center_x",
                               anchor_y="center_y",
                               align_x=-(self.width // 4),
                               align_y=0)
        self.manager.add(self.anchor_layout)

        for i in range(5):
            p = arcade.Sprite(self.planet_textures[i])
            p.center_x = self.width - (self.width / 2.5) + 10
            p.center_y = 500 - i * 60
            p.scale = 0.05
            self.all_sprites.append(p)

        self.manager1 = UIManager()
        self.manager1.enable()

        self.anchor_layout1 = UIAnchorLayout(width=self.width,
                                             height=self.height)
        self.box_layout1 = UIBoxLayout(vertical=True, space_between=30,
                                       align="center")

        label1 = UILabel(text="Уровень первый",
                         font_size=20,
                         text_color=arcade.color.WHITE,
                         width=40
                         )
        self.box_layout1.add(label1)
        label1 = UILabel(text="Уровень второй",
                         font_size=20,
                         text_color=arcade.color.WHITE,
                         width=40
                         )
        self.box_layout1.add(label1)
        label1 = UILabel(text="Уровень третий",
                         font_size=20,
                         text_color=arcade.color.WHITE,
                         width=40
                         )
        self.box_layout1.add(label1)
        label1 = UILabel(text="Уровень четвёртый",
                         font_size=20,
                         text_color=arcade.color.WHITE,
                         width=40
                         )
        self.box_layout1.add(label1)
        label1 = UILabel(text="Уровень пятый",
                         font_size=20,
                         text_color=arcade.color.WHITE,
                         width=40
                         )
        self.box_layout1.add(label1)

        self.dropdown1 = UIDropdown(options=self.option_list1, width=200)
        self.dropdown1.on_change = self.on_change1
        self.box_layout1.add(self.dropdown1)

        self.anchor_layout1.add(self.box_layout1, anchor_x="center_x",
                                anchor_y="center_y",
                                align_x=(self.width // 4),
                                align_y=0)
        self.manager1.add(self.anchor_layout1)

        self.emitters = []
        self.trail = None
        self.trail_list = []
        self.star_sprites = arcade.SpriteList()
        self.input = None
        self.timer = 0

        self.menu = True

    def on_update(self, delta_time):
        if self.menu:
            self.timer += delta_time
            if self.timer >= 0.5:
                self.timer = 0
                player = Star()
                player.center_x, player.center_y = random.choice([
                    (random.randint(0, self.width), self.height + 10),
                    (self.width + 10, random.randint(0, self.height))
                ])
                self.input = InputState()
                self.trail_list.append(self.input)
                self.star_sprites.append(player)
                trail = make_trail(player)
                self.emitters.append(trail)
            v = 280 * delta_time

            players_to_remove = []

            for i in range(len(self.star_sprites) - 1, -1, -1):
                if self.trail_list[i].left:  self.star_sprites[i].center_x -= v
                if self.trail_list[i].right: self.star_sprites[i].center_x += v
                if self.trail_list[i].up:    self.star_sprites[i].center_y += v
                if self.trail_list[i].down:  self.star_sprites[i].center_y -= v

                if i < len(self.emitters):
                    self.emitters[i].center_x = self.star_sprites[i].center_x
                    self.emitters[i].center_y = self.star_sprites[i].center_y

                if self.star_sprites[i].center_y < -50:
                    players_to_remove.append(i)

            for i in sorted(players_to_remove, reverse=True):
                if i < len(self.trail_list):
                    self.trail_list.pop(i)
                if i < len(self.emitters):
                    self.emitters.pop(i)
                if i < len(self.star_sprites):
                    self.star_sprites.pop(i)

            emitters_copy = self.emitters.copy()
            for e in emitters_copy:
                e.update(delta_time)
            for e in emitters_copy:
                if e.can_reap():
                    self.emitters.remove(e)

            self.star_sprites.update()

    def on_draw(self):
        self.clear()
        for e in self.emitters:
            e.draw()
        self.star_sprites.draw()
        self.batch.draw()
        self.manager.draw()
        self.manager1.draw()

        self.all_sprites.draw()

    def on_change(self, event):
        i = self.option_list.index(self.dropdown.value)
        if i:
            self.player_num = i - 1
        self.player = arcade.Sprite(self.players[self.player_num])

    def on_change1(self, event):
        self.planet = self.option_list1.index(self.dropdown1.value)

    def on_key_press(self, key, modifiers):
        self.menu = False
        saved_state = {'level': self.planet,
                       'player': self.player,
                       'player_num': self.player_num,
                       'enemies': self.enemies_list,
                       'items': self.items_list}

        start_game_view = StartGameView(state=saved_state)
        self.window.show_view(start_game_view)
