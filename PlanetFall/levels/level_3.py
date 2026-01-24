import arcade
import random
from PlanetFall.levels.level import Level, DustParticle
from PlanetFall.constants import *


class Level_3(Level):
    def __init__(self, saved_state):
        super().__init__(saved_state)
        self.background_list = None
        self.ground_list = None
        self.stakes_list = None
        self.moving_platforms_list = None
        self.juice_list = None
        self.collision_list = None

    def setup(self):
        super().setup()
        self.gravity = 0.7
        self.jump_speed = 20
        self.player_speed = PLAYER_SPEED
        self.enemy_speed = 55

        self.background_list = self.scene['background']
        self.ground_list = self.scene['ground']
        self.stakes_list = self.scene['stakes']
        self.moving_platforms_list = self.scene['moving platforms']
        self.juice_list = self.scene['juice']
        self.collision_list = self.scene['collision']

        item = arcade.Sprite('images/items/item_4.png', 0.5)
        item.name = 'item'
        item.center_x = 14 * 21 * 3 + 50
        item.center_y = 26.5 * 21 * 3 + 40
        item.angle = 90
        self.dont_items_list.append(item)
        item = arcade.Sprite('images/items/item_5.png', 0.5)
        item.name = 'item'
        item.center_x = 50 * 21 * 3
        item.center_y = 29 * 21 * 3
        self.dont_items_list.append(item)

        self.slimes = ['images/enemies/slime.png', 'images/enemies/slime_walk.png']
        self.barnacles = ['images/enemies/barnacle.png', 'images/enemies/barnacle_bite.png']
        self.bees = ['images/enemies/bee.png', 'images/enemies/bee_fly.png']

        if not self.enemies_list:
            for i in range(3):
                barnacle = arcade.Sprite('images/enemies/barnacle.png')
                barnacle.typ = 'barnacle'
                barnacle.center_x = (44.5 + i * 7) * 21 * 3
                barnacle.center_y = 24 * 21 * 3 + barnacle.height // 2
                barnacle.speed = 0
                self.enemies_list.append(barnacle)

            for i in range(2):
                bee = arcade.Sprite('images/enemies/bee.png')
                bee.typ = 'bee'
                bee.center_x = random.randint(40 * 21 * 3, 60 * 21 * 3)
                bee.center_y = 34 * 21 * 3
                bee.speed = self.enemy_speed * random.choice([-1, 1])
                self.enemies_list.append(bee)

            self.slime1 = arcade.Sprite('images/enemies/slime.png')
            self.slime1.typ = 'slime'
            self.slime1.center_x = random.randint(66 * 21 * 3, 72 * 21 * 3)
            self.slime1.center_y = 24 * 21 * 3 + self.slime1.height // 2
            self.slime1.speed = self.enemy_speed * random.choice([-1, 1])
            self.enemies_list.append(self.slime1)

            self.slime2 = arcade.Sprite('images/enemies/slime.png')
            self.slime2.typ = 'slime'
            self.slime2.center_x = random.randint(81 * 21 * 3, 88 * 21 * 3)
            self.slime2.center_y = 24 * 21 * 3 + self.slime2.height // 2
            self.slime2.speed = self.enemy_speed * random.choice([-1, 1])
            self.enemies_list.append(self.slime2)

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

        self.background_list.draw()
        self.dust_particles.draw()
        self.ground_list.draw()
        self.stakes_list.draw()
        self.moving_platforms_list.draw()
        self.juice_list.draw()
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
            if enemy.typ == 'bee':
                if enemy.left < 40 * 21 * 3:
                    enemy.left = 40 * 21 * 3 + 3
                    enemy.speed *= -1
                elif enemy.right > 60 * 21 * 3:
                    enemy.right = 60 * 21 * 3 - 3
                    enemy.speed *= -1
                enemy.center_x += enemy.speed * delta_time
                if enemy.speed < 0:
                    enemy.texture = arcade.load_texture(self.bees[self.i])
                else:
                    enemy.texture = arcade.load_texture(self.bees[self.i]).flip_horizontally()
            elif enemy.typ == 'barnacle':
                enemy.texture = arcade.load_texture(self.barnacles[self.i])

        if self.slime1.left < 65 * 21 * 3:
            self.slime1.left = 65 * 21 * 3 + 3
            self.slime1.speed *= -1
        elif self.slime1.right > 73 * 21 * 3:
            self.slime1.right = 73 * 21 * 3 - 3
            self.slime1.speed *= -1

        self.slime1.center_x += self.slime1.speed * delta_time
        if self.slime1.speed < 0:
            self.slime1.texture = arcade.load_texture(self.slimes[self.i])
        else:
            self.slime1.texture = arcade.load_texture(self.slimes[self.i]).flip_horizontally()

        if self.slime2.left < 80 * 21 * 3:
            self.slime2.left = 80 * 21 * 3 + 3
            self.slime2.speed *= -1
        elif self.slime2.right > 89 * 21 * 3:
            self.slime2.right = 89 * 21 * 3 - 3
            self.slime2.speed *= -1

        self.slime2.center_x += self.slime2.speed * delta_time
        if self.slime2.speed < 0:
            self.slime2.texture = arcade.load_texture(self.slimes[self.i])
        else:
            self.slime2.texture = arcade.load_texture(self.slimes[self.i]).flip_horizontally()


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
            from PlanetFall.WinView import WinView
            win_view = WinView(game_view=self, time=round(self.timer), state=state)
            self.window.show_view(win_view)

        if arcade.check_for_collision_with_list(self.player, self.stakes_list) or arcade.check_for_collision_with_list(
                self.player, self.enemies_list) or arcade.check_for_collision_with_list(self.player,
                                                                                        self.juice_list):
            self.game_over = True
            state = {'level': self.level,
                     'player': self.player,
                     'player_num': self.player_num,
                     'enemies': arcade.SpriteList(),
                     'items': self.items_list,
                     'coll_items': arcade.SpriteList()}
            self.jump_buffer_timer = 0
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
                self.is_jumping = False
                self.was_jumping = True
                self.jump_buffer_timer = 0
                self.jumps_left -= 1

        elif self.physics_engine.can_jump(y_distance=6) and self.was_jumping:
            self.land_timer += delta_time
            if self.land_timer <= 0.15:
                if self.left:
                    self.player.texture = arcade.load_texture(self.textures[9]).flip_horizontally()
                else:
                    self.player.texture = arcade.load_texture(self.textures[9])

                self.create_dust_effect()
            else:
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
            item.angle = 0
            item.remove_from_sprite_lists()
            self.coll_items_list.append(item)

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
