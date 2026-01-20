import arcade
from PauseView import PauseView
from arcade import Camera2D
from pyglet.graphics import Batch

from PlanetFall.constants import TILE_SIZE, CAMERA_LERP, GRAVITY, COYOTE_TIME, JUMP_SPEED, PLAYER_SPEED, MAX_JUMPS, \
    SCREEN_WIDTH, SCREEN_HEIGHT, JUMP_BUFFER


class Level(arcade.View):
    def __init__(self, saved_state):
        super().__init__()
        self.background_texture = arcade.load_texture('images/sky_lvl_1.jpg')
        self.level = saved_state.get('level')
        self.player = saved_state.get('player')
        self.player_list = arcade.SpriteList()

        self.enemies_list = saved_state.get('enemies', arcade.SpriteList())
        self.items_list = saved_state.get('items', arcade.SpriteList())
        self.d_items_list = arcade.SpriteList()

        self.timer = 0
        self.jump_buffer_timer = 0
        self.time_since_ground = 0
        self.jumps_left = MAX_JUMPS

        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.paused = False
        self.game_over = False
        self.win = False

        self.gravity = GRAVITY
        self.coyote_time = COYOTE_TIME
        self.jump_speed = JUMP_SPEED

        self.batch = Batch()
        self.space_text = arcade.Text("Нажмите ESC, чтобы приостановить", 130,
                                      self.window.height - 30,
                                      arcade.color.WHITE, font_size=10, anchor_x="center", batch=self.batch)


        self.scene = None
        self.ground_list = None
        self.water_list = None
        self.stakes_list = None
        self.ladders_list = None
        self.background_list = None
        self.collision_list = None
        self.physics_engine = None

        self.world_camera = None
        self.gui_camera = None

    def setup(self):
        self.paused = False
        self.game_over = False
        self.win = False

        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS
        self.gravity = GRAVITY
        self.coyote_time = COYOTE_TIME
        self.jump_speed = JUMP_SPEED

        if len(self.player_list) == 0:
            self.player_list.append(self.player)

        tile_map = arcade.load_tilemap('levels/level_1.tmx', scaling=3.0)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.ground_list = self.scene['ground']
        self.water_list = self.scene['water']
        self.stakes_list = self.scene['stakes']
        self.ladders_list = self.scene['ladders']
        self.background_list = self.scene['background']
        self.collision_list = self.scene['collision']

        # self.d_items_list.append(arcade.Sprite(''))
        # self.d_items_list.append(arcade.Sprite(''))

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=self.gravity,
            walls=(self.ground_list),
            ladders=self.ladders_list
        )

        self.world_camera = Camera2D(
            viewport=arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            position=(self.player.center_x, self.player.center_y)
        )
        self.gui_camera = Camera2D(
            viewport=arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(
            self.window.width // 2, self.window.height // 2,
            self.window.width, self.window.height)
        )
        self.world_camera.use()

        self.background_list.draw()
        self.ground_list.draw()
        self.water_list.draw()
        self.stakes_list.draw()
        self.ladders_list.draw()
        self.player_list.draw()
        self.enemies_list.draw()
        self.d_items_list.draw()

        self.gui_camera.use()
        self.batch.draw()

    def on_update(self, delta_time):
        if self.paused or self.win or self.game_over:
            return
        if arcade.check_for_collision_with_list(self.player, self.stakes_list):
            self.game_over = True
            from GameOverView import GameOverView
            game_over_view = GameOverView(game_view=self, level=self.level, player=self.player, )
            self.window.show_view(game_over_view)
        if arcade.check_for_collision_with_list(self.player, self.water_list):
            self.gravity = 0.3
            self.coyote_time = 0.04
            self.jump_speed = 15
        else:
            self.gravity = GRAVITY
            self.coyote_time = COYOTE_TIME
            self.jump_speed = JUMP_SPEED
        self.physics_engine.gravity_constant = self.gravity

        move = 0
        if self.left and not self.right:
            move = -PLAYER_SPEED
        elif self.right and not self.left:
            move = PLAYER_SPEED

        self.player.change_x = move

        on_ladder = self.physics_engine.is_on_ladder()
        if on_ladder:
            if self.up and not self.down:
                self.player.change_y = PLAYER_SPEED
            elif self.down and not self.up:
                self.player.change_y = -PLAYER_SPEED
            else:
                self.player.change_y = 0

        grounded = self.physics_engine.can_jump(y_distance=6)
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.time_since_ground += delta_time

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= delta_time

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)

        if want_jump:
            can_coyote = (self.time_since_ground <= self.coyote_time)
            if grounded or can_coyote:
                self.physics_engine.jump(self.jump_speed)
                self.jump_buffer_timer = 0
                self.jumps_left -= 1

        self.physics_engine.update()

        check = arcade.check_for_collision_with_list(self.player, self.d_items_list)
        for item in check:
            item.remove_from_sprite_lists()
            self.items_list.append(item)

        target_x = self.player.center_x
        target_y = self.player.center_y

        cx, cy = self.world_camera.position
        smooth_x = cx + (target_x - cx) * CAMERA_LERP
        smooth_y = cy + (target_y - cy) * CAMERA_LERP

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        world_w = 1932 * 3
        world_h = 1134 * 3

        cam_x = max(half_w, min(world_w - half_w, smooth_x))
        cam_y = max(half_h, min(world_h - half_h, smooth_y))

        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def pause_game(self):
        self.paused = True

        saved_state = {'level': self.level,
                       'player': self.player,
                       'enemies': self.enemies_list,
                       'items': self.items_list}

        pause_view = PauseView(game_view=self, game_state=saved_state)
        self.window.show_view(pause_view)

    def restore_state(self, state):
        self.level = state['level']
        self.player = state['player']
        self.enemies_list = state['enemies']
        self.items_list = state['items']
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
            self.jump_pressed = True
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
        elif key == arcade.key.SPACE:
            self.jump_pressed = False
            if self.player.change_y > 0 and arcade.check_for_collision_with_list(self.player, self.water_list):
                self.player.change_y *= 0.65
            elif self.player.change_y > 0 and not arcade.check_for_collision_with_list(self.player, self.water_list):
                self.player.change_y *= 0.45
