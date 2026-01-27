import arcade
import random

from PlanetFall.items import Item
from PlanetFall.levels.level import Level, DustParticle
from PlanetFall.constants import *


class Level_1(Level):
    def __init__(self, saved_state):
        super().__init__(saved_state)
        self.ground_list = None
        self.water_list = None
        self.cactus_list = None
        self.ladders_list = None
        self.background_list = None
        self.platforms_list = None
        self.collision_list = None

    def setup(self):
        super().setup()
        self.gravity = 0.7
        self.jump_speed = 25
        self.player_speed = PLAYER_SPEED
        self.enemy_speed = ENEMY_SPEED

        self.ground_list = self.scene['ground']
        self.water_list = self.scene['water']
        self.cactus_list = self.scene['cactus']
        self.ladders_list = self.scene['ladders']
        self.background_list = self.scene['background']
        self.platforms_list = self.scene['platforms']
        self.collision_list = self.scene['collision']

        item = Item('images/items/item_2.png', 0.5, 2)
        item.center_x = 30 * 21 * 3
        item.center_y = 30 * 21 * 3
        item.scale = 0.7
        item.angle = 90
        self.dont_items_list.append(item)
        item = Item('images/items/item_3.png', 0.5, 3)
        item.center_x = 92 * 21 * 3
        item.center_y = 30.5 * 21 * 3
        item.angle = 90
        self.dont_items_list.append(item)

        self.snakes = ['images/enemies/snake.png', 'images/enemies/snake_walk.png']

        if not self.enemies_list:
            for i in range(5):
                piranha = arcade.Sprite('images/enemies/piranha.png')
                piranha.typ = 'piranha'
                piranha.center_x = (10 + i * 8) * 21 * 3
                piranha.center_y = random.randint(14 * 21 * 3, 24 * 21 * 3)
                piranha.speed = self.enemy_speed * random.choice([-1, 1])
                self.enemies_list.append(piranha)
            for i in range(5):
                snake = arcade.Sprite('images/enemies/snake.png', 1.5)
                snake.typ = 'snake'
                snake.center_x = random.randint(73 * 21 * 3, 78 * 21 * 3)
                snake.center_y = 15 * 21 * 3 + snake.height // 2
                snake.speed = self.enemy_speed * random.choice([-1, 1])
                self.enemies_list.append(snake)
            for i in range(6):
                snail = arcade.Sprite('images/enemies/snail.png')
                snail.typ = 'snail'
                snail.x = random.choice([(56 * 21 * 3, 64 * 21 * 3),
                                         (66 * 21 * 3, 70 * 21 * 3),
                                         (84 * 21 * 3, 91 * 21 * 3)])
                snail.center_x = random.randint(snail.x[0], snail.x[1])
                snail.center_y = 24 * 21 * 3 + snail.height // 2
                snail.speed = self.enemy_speed * random.choice([-1, 1])
                self.enemies_list.append(snail)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=self.gravity,
            walls=self.ground_list,
            platforms=self.platforms_list,
            ladders=self.ladders_list
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(
            self.window.width // 2, self.window.height // 2,
            self.window.width, self.window.height)
                                 )
        self.world_camera.use()


        self.dust_particles.draw()
        self.ground_list.draw()
        self.water_list.draw()
        self.cactus_list.draw()
        self.background_list.draw()
        self.ladders_list.draw()
        self.platforms_list.draw()
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
            if enemy.typ == 'piranha':
                if enemy.bottom < 14 * 21 * 3:
                    enemy.bottom = 14 * 21 * 3 + 3
                    enemy.speed *= -1
                elif enemy.top > 24 * 21 * 3:
                    enemy.top = 24 * 21 * 3 - 3
                    enemy.speed *= -1
                enemy.center_y += enemy.speed * delta_time
                if enemy.speed < 0:
                    enemy.texture = arcade.load_texture('images/enemies/piranha_down.png')
                else:
                    enemy.texture = arcade.load_texture('images/enemies/piranha.png')
            elif enemy.typ == 'snake':
                if enemy.left < 73 * 21 * 3:
                    enemy.left = 73 * 21 * 3 + 3
                    enemy.speed *= -1
                elif enemy.right > 78 * 21 * 3:
                    enemy.right = 78 * 21 * 3 - 3
                    enemy.speed *= -1
                enemy.center_x += enemy.speed * delta_time
                if enemy.speed < 0:
                    enemy.texture = arcade.load_texture(self.snakes[self.i])
                else:
                    enemy.texture = arcade.load_texture(self.snakes[self.i]).flip_horizontally()
            elif enemy.typ == 'snail':
                if enemy.left < enemy.x[0]:
                    enemy.left = enemy.x[0] + 3
                    enemy.speed *= -1
                elif enemy.right > enemy.x[1]:
                    enemy.right = enemy.x[1] - 3
                    enemy.speed *= -1
                enemy.center_x += enemy.speed * delta_time
                if enemy.speed < 0:
                    enemy.texture = arcade.load_texture('images/enemies/snail.png')
                else:
                    enemy.texture = arcade.load_texture('images/enemies/snail.png').flip_horizontally()

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
            from PlanetFall.WinView import WinView
            win_view = WinView(game_view=self, time=round(self.timer), state=state)
            self.window.show_view(win_view)

        if arcade.check_for_collision_with_list(self.player, self.cactus_list) or arcade.check_for_collision_with_list(
                self.player, self.enemies_list) or arcade.check_for_collision_with_list(self.player, self.water_list):
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
            if self.player.change_y > 0 and arcade.check_for_collision_with_list(self.player, self.water_list):
                self.player.change_y *= 0.65
            elif self.player.change_y > 0 and not arcade.check_for_collision_with_list(self.player, self.water_list):
                self.player.change_y *= 0.45
