import arcade
from PlanetFall.PauseView import PauseView
from arcade import Camera2D
from pyglet.graphics import Batch
import random
from PlanetFall.constants import *


class DustParticle(arcade.SpriteCircle):
    """Частица пыли для эффекта приземления"""

    def __init__(self, x, y):
        color = random.choice([
            (255, 255, 255, 200),
            (196, 196, 196, 200),
            (212, 212, 212, 200),
            (156, 156, 156, 200)
        ])
        size = random.randint(3, 8)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        self.change_x = random.uniform(-1.5, 1.5)
        self.change_y = random.uniform(0, 2)
        self.scale = 1.0
        self.alpha = 200
        self.lifetime = random.uniform(0.5, 1.2)
        self.time_alive = 0

    def update(self, delta_time):
        # Движение частицы
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Замедление
        self.change_x *= 0.95
        self.change_y *= 0.95

        # Изменение масштаба
        self.scale_x *= 1.02
        self.scale_y *= 1.005

        # Уменьшение прозрачности
        self.alpha -= 2

        # Увеличение времени жизни
        self.time_alive += delta_time

        # Проверка на окончание времени жизни
        if self.time_alive >= self.lifetime:
            self.remove_from_sprite_lists()


class Level(arcade.View):
    def __init__(self, saved_state):
        super().__init__()
        self.level = saved_state.get('level')
        self.background_texture = arcade.load_texture(f'images/skies/sky_lvl_{self.level}.jpg')
        self.player = saved_state.get('player')
        self.player_num = saved_state.get('player_num')
        self.background_music = None
        self.background_player = None
        self.jump_sound = arcade.load_sound("sounds/jump.wav")
        self.land_sound = arcade.load_sound("sounds/land.wav")
        self.collect_sound = arcade.load_sound("sounds/collect.wav")
        self.player_list = arcade.SpriteList()

        self.enemies_list = saved_state.get('enemies', arcade.SpriteList())
        self.items_list = saved_state.get('items', [])
        self.coll_items_list = saved_state.get('coll_items', [])
        self.dont_items_list = arcade.SpriteList()
        self.textures = [f'images/Alien{self.player_num}/alien{self.player_num}_{i}.png' for i in range(10)]

        self.timer = 0
        self.jump_buffer_timer = 0
        self.time_since_ground = 0
        self.jumps_left = MAX_JUMPS
        self.animation_timer = 0
        self.i = 0
        self.land_timer = 0

        self.left = self.right = self.up = self.down = False
        self.is_jumping = False
        self.was_jumping = False
        self.paused = False
        self.game_over = False
        self.win = False

        self.gravity = GRAVITY
        self.coyote_time = COYOTE_TIME
        self.jump_speed = JUMP_SPEED
        self.anim_time = ANIMATION_TIMER
        self.player_speed = 0
        self.enemy_speed = 0

        self.batch = Batch()
        self.space_text = arcade.Text("Нажмите ESC, чтобы приостановить", 170,
                                      self.window.height - 30,
                                      arcade.color.WHITE, font_name='Times New Roman', font_size=15, anchor_x="center",
                                      batch=self.batch)

        self.scene = None
        self.physics_engine = None
        self.dust_particles = None

        self.world_camera = None
        self.gui_camera = None

    def setup(self):
        self.paused = False
        self.game_over = False
        self.win = False

        self.timer = 0
        self.animation_timer = 0
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.i = 0
        self.land_timer = 0
        self.jumps_left = MAX_JUMPS
        self.coyote_time = COYOTE_TIME
        self.anim_time = ANIMATION_TIMER

        if len(self.player_list) == 0:
            self.player_list.append(self.player)

        tile_map = arcade.load_tilemap(f'maps/level_{self.level}.tmx', scaling=3.0)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.dust_particles = arcade.SpriteList()

        self.world_camera = Camera2D(
            viewport=arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            position=(self.player.center_x, self.player.center_y)
        )
        self.gui_camera = Camera2D(
            viewport=arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )

    def on_update(self, delta_time):
        if self.paused or self.win or self.game_over:
            return
        self.timer += delta_time
        self.animation_timer += delta_time

        for e in self.dust_particles:
            e.update(delta_time)
        if self.player.center_x < self.player.width - 10:
            self.player.center_x = self.player.width - 10

    def pause_game(self):
        self.paused = True
        arcade.stop_sound(self.background_player)
        saved_state = {'level': self.level,
                       'player': self.player,
                       'player_num': self.player_num,
                       'enemies': self.enemies_list,
                       'items': self.items_list,
                       'coll_items': self.coll_items_list}

        pause_view = PauseView(game_view=self, game_state=saved_state)
        self.window.show_view(pause_view)

    def restore_state(self, state):
        self.level = state['level']
        self.player = state['player']
        self.player_num = state['player_num']
        self.enemies_list = state['enemies']
        self.items_list = state['items']
        self.coll_items_list = state['coll_items']
        self.paused = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause_game()
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key == arcade.key.SPACE:
            self.is_jumping = True
            self.jump_buffer_timer = JUMP_BUFFER

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False

    def on_show_view(self):
        super().on_show_view()
        self.background_music = arcade.load_sound(f'sounds/level_{self.level}.mp3')
        self.background_player = self.background_music.play(loop=True, volume=0.3)
