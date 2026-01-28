import arcade
import random

from PlanetFall.items import Item
from PlanetFall.levels.level import Level, DustParticle
from PlanetFall.constants import *


class Level_4(Level):
    def __init__(self, saved_state):
        super().__init__(saved_state)
        self.background_list = None
        self.background2_list = None
        self.ground_list = None
        self.moving_platforms_list = None
        self.mushrooms_list = None
        self.collision_list = None

    def setup(self):
        super().setup()
        self.gravity = 0.7
        self.jump_speed = 22
        self.player_speed = 5
        self.enemy_speed = 52

        self.background_list = self.scene['background']
        self.background2_list = self.scene['background2']
        self.ground_list = self.scene['ground']
        self.moving_platforms_list = self.scene['moving platforms']
        self.mushrooms_list = self.scene['mushrooms']
        self.collision_list = self.scene['collision']

        item = Item('images/items/item_6.png', typ=6)
        item.center_x = 25 * 21 * 3
        item.center_y = 27.7 * 21 * 3
        self.dont_items_list.append(item)
        item = Item('images/items/item_7.png', 0.5, 7)
        item.center_x = 64 * 21 * 3
        item.center_y = 31 * 21 * 3
        self.dont_items_list.append(item)

        self.flies = ['images/enemies/fly.png', 'images/enemies/fly_fly.png']
        self.mice = ['images/enemies/mouse.png', 'images/enemies/mouse_walk.png']

        if not self.enemies_list:
            for i in range(3):
                fly = arcade.Sprite('images/enemies/fly.png')
                fly.typ = 'fly'
                fly.x = [(12 * 21 * 3, 21 * 21 * 3),
                         (36 * 21 * 3, 42 * 21 * 3),
                         (59 * 21 * 3, 69 * 21 * 3)][i]
                fly.center_x = random.randint(fly.x[0], fly.x[1])
                fly.center_y = 32 * 21 * 3
                fly.speed = self.enemy_speed * random.choice([-1, 1])
                self.enemies_list.append(fly)

            for i in range(2):
                fly = arcade.Sprite('images/enemies/fly.png')
                fly.typ = 'fly'
                fly.x = [(23 * 21 * 3, 30 * 21 * 3),
                         (50 * 21 * 3, 57 * 21 * 3)][i]
                fly.center_x = random.randint(fly.x[0], fly.x[1])
                fly.center_y = 34 * 21 * 3
                fly.speed = self.enemy_speed * random.choice([-1, 1])
                self.enemies_list.append(fly)

            for i in range(2):
                for j in range(3):
                    mouse = arcade.Sprite('images/enemies/mouse.png')
                    mouse.typ = 'mouse'
                    mouse.x = [(71 * 21 * 3, 83 * 21 * 3),
                               (85 * 21 * 3, 95 * 21 * 3)][i]
                    mouse.center_x = random.randint(mouse.x[0], mouse.x[1])
                    mouse.center_y = 24 * 21 * 3 + mouse.height // 2
                    mouse.speed = self.enemy_speed * random.choice([-1, 1])
                    self.enemies_list.append(mouse)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=self.gravity,
            walls=self.ground_list,
            platforms=self.moving_platforms_list
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(
            self.window.width // 2, self.window.height // 2,
            self.window.width, self.window.height)
                                 )
        self.world_camera.use()

        self.background2_list.draw()
        self.dust_particles.draw()
        self.ground_list.draw()
        self.background_list.draw()
        self.moving_platforms_list.draw()
        self.mushrooms_list.draw()
        self.player_list.draw()
        self.enemies_list.draw()
        self.dont_items_list.draw()

        self.gui_camera.use()
        self.batch.draw()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.animation_timer >= self.anim_time:
            self.animation_timer = 0
            self.i += 1
            self.i %= 2

        for enemy in self.enemies_list:
            if enemy.left < enemy.x[0]:
                enemy.left = enemy.x[0] + 3
                enemy.speed *= -1
            elif enemy.right > enemy.x[1]:
                enemy.right = enemy.x[1] - 3
                enemy.speed *= -1
            enemy.center_x += enemy.speed * delta_time
            if enemy.typ == 'fly':
                if enemy.speed < 0:
                    enemy.texture = arcade.load_texture(self.flies[self.i])
                else:
                    enemy.texture = arcade.load_texture(self.flies[self.i]).flip_horizontally()
            elif enemy.typ == 'mouse':
                if enemy.speed < 0:
                    enemy.texture = arcade.load_texture(self.mice[self.i])
                else:
                    enemy.texture = arcade.load_texture(self.mice[self.i]).flip_horizontally()

        move = 0
        if self.left and not self.right:
            move = -self.player_speed
        elif self.right and not self.left:
            move = self.player_speed

        self.player.change_x = move

        if self.player.center_x > (2121 * 3) - self.player.width // 2:
            self.win = True
            state = {'level': self.level,
                     'player': self.player,
                     'player_num': self.player_num,
                     'enemies': arcade.SpriteList(),
                     'items': self.items_list,
                     'coll_items': self.coll_items_list}
            arcade.stop_sound(self.background_player)
            from PlanetFall.FinishView import FinishView
            finish_view = FinishView(time=round(self.timer), state=state)
            self.window.show_view(finish_view)

        if arcade.check_for_collision_with_list(self.player,
                                                self.mushrooms_list) or arcade.check_for_collision_with_list(
                self.player, self.enemies_list):
            self.game_over = True
            state = {'level': self.level,
                     'player': self.player,
                     'player_num': self.player_num,
                     'enemies': arcade.SpriteList(),
                     'items': self.items_list,
                     'coll_items': arcade.SpriteList()}
            self.jump_buffer_timer = 0
            arcade.stop_sound(self.background_player)
            from PlanetFall.GameOverView import GameOverView
            game_over_view = GameOverView(game_view=self, state=state)
            self.window.show_view(game_over_view)

        on_ladder = self.physics_engine.is_on_ladder()
        if on_ladder:
            self.player.texture = arcade.load_texture(self.textures[0])
            if self.up and not self.down:
                self.player.change_y = self.player_speed
                self.player.texture = arcade.load_texture(self.textures[self.i])
            elif self.down and not self.up:
                self.player.change_y = -self.player_speed
                self.player.texture = arcade.load_texture(self.textures[self.i])
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

        want_jump = self.is_jumping or (self.jump_buffer_timer > 0)

        if want_jump:
            can_coyote = (self.time_since_ground <= self.coyote_time)
            if grounded or can_coyote:
                if self.left:
                    self.player.texture = arcade.load_texture(self.textures[3]).flip_horizontally()
                else:
                    self.player.texture = arcade.load_texture(self.textures[3])
                self.physics_engine.jump(self.jump_speed)
                self.jump_sound.play(volume=0.5)
                self.is_jumping = False
                self.was_jumping = True
                self.jump_buffer_timer = 0
                self.jumps_left -= 1

        elif self.physics_engine.can_jump(y_distance=6) and self.was_jumping:
            self.land_timer += delta_time
            if self.land_timer <= 0.11:
                if self.left:
                    self.player.texture = arcade.load_texture(self.textures[9]).flip_horizontally()
                else:
                    self.player.texture = arcade.load_texture(self.textures[9])
            else:
                self.land_sound.play(volume=1)
                self.create_dust_effect()
                self.land_timer = 0
                self.was_jumping = False

        elif self.was_jumping and not self.physics_engine.can_jump(y_distance=6):
            if self.left:
                self.player.texture = arcade.load_texture(self.textures[3]).flip_horizontally()
            else:
                self.player.texture = arcade.load_texture(self.textures[3])


        elif not self.is_jumping and not self.was_jumping and not on_ladder:
            if self.left:
                self.player.texture = arcade.load_texture(self.textures[self.i + 7]).flip_horizontally()
            elif self.right:
                self.player.texture = arcade.load_texture(self.textures[self.i + 7])
            else:
                self.player.texture = arcade.load_texture(self.textures[4])

        self.physics_engine.update()

        check = arcade.check_for_collision_with_list(self.player, self.dont_items_list)
        for item in check:
            self.collect_sound.play(volume=1)
            item.remove_from_sprite_lists()
            self.coll_items_list.append(item.typ)

        target_x = self.player.center_x
        target_y = self.player.center_y

        cx, cy = self.world_camera.position
        smooth_x = cx + (target_x - cx) * CAMERA_LERP
        smooth_y = cy + (target_y - cy) * CAMERA_LERP

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        world_w = 2121 * 3
        world_h = 1134 * 3

        cam_x = max(half_w, min(world_w - half_w, smooth_x))
        cam_y = max(half_h, min(world_h - half_h, smooth_y))

        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def create_dust_effect(self):
        for i in range(random.randint(15, 21)):
            e = DustParticle(self.player.center_x, self.player.bottom)
            self.dust_particles.append(e)

    def on_key_release(self, key, modifiers):
        super().on_key_release(key, modifiers)
        if key == arcade.key.SPACE:
            if self.player.change_y > 0:
                self.player.change_y *= 0.45
