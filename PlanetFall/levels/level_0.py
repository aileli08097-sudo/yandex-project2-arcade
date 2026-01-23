import arcade
import random
from PlanetFall.levels.level import Level, DustParticle
from PlanetFall.constants import *


class Level_0(Level):
    def __init__(self, saved_state):
        super().__init__(saved_state)
        self.ground_list = None
        self.water_list = None
        self.stakes_list = None
        self.ladders_list = None
        self.background_list = None
        self.collision_list = None

    def setup(self):
        super().setup()
        self.gravity = GRAVITY
        self.jump_speed = JUMP_SPEED

        self.ground_list = self.scene['ground']
        self.water_list = self.scene['water']
        self.stakes_list = self.scene['stakes']
        self.ladders_list = self.scene['ladders']
        self.background_list = self.scene['background']
        self.collision_list = self.scene['collision']

        item = arcade.Sprite('images/items/item_0.png', 0.5)
        item.center_x = 44 * 21 * 3
        item.center_y = 12 * 21 * 3
        self.dont_items_list.append(item)
        item = arcade.Sprite('images/items/item_1.png', 0.5)
        item.center_x = 65 * 21 * 3
        item.center_y = 31 * 21 * 3
        self.dont_items_list.append(item)

        if not self.enemies_list:
            self.ghost = arcade.Sprite('images/enemies/ghost.png')
            self.ghost.center_x = random.randint(78 * 21 * 3, 88 * 21 * 3)
            self.ghost.center_y = 24 * 21 * 3 + self.ghost.height
            self.ghost.speed = ENEMY_SPEED * random.choice([-1, 1])
            self.enemies_list.append(self.ghost)
            self.fish = arcade.Sprite('images/enemies/fishPink.png')
            self.fish.center_x = random.randint(24 * 21 * 3, 43 * 21 * 3)
            self.fish.center_y = 12 * 21 * 3 + self.fish.height
            self.fish.speed = ENEMY_SPEED * random.choice([-1, 1])
            self.enemies_list.append(self.fish)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=self.gravity,
            walls=self.ground_list,
            ladders=self.ladders_list
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
        self.water_list.draw()
        self.stakes_list.draw()
        self.ladders_list.draw()
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
        if self.ghost.left < 78 * 21 * 3:
            self.ghost.left = 78 * 21 * 3 + 1
            self.ghost.speed *= -1
        elif self.ghost.right > 88 * 21 * 3:
            self.ghost.right = 88 * 21 * 3 - 1
            self.ghost.speed *= -1
        self.ghost.center_x += self.ghost.speed * delta_time
        if self.ghost.speed < 0:
            self.ghost.texture = arcade.load_texture('images/enemies/ghost.png')
        else:
            self.ghost.texture = arcade.load_texture('images/enemies/ghost.png').flip_horizontally()
        if self.fish.left < 24 * 21 * 3:
            self.fish.left = 24 * 21 * 3 + 1
            self.fish.speed *= -1
        elif self.fish.right > 43 * 21 * 3:
            self.fish.right = 43 * 21 * 3 - 1
            self.fish.speed *= -1
        self.fish.center_x += self.fish.speed * delta_time
        if self.fish.speed < 0:
            self.fish.texture = arcade.load_texture('images/enemies/fishPink.png')
        else:
            self.fish.texture = arcade.load_texture('images/enemies/fishPink.png').flip_horizontally()

        if self.player.center_x > (1932 * 3) - self.player.width:
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
                self.player, self.enemies_list):
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
        if arcade.check_for_collision_with_list(self.player, self.water_list):
            self.gravity = 0.3
            self.jump_speed = 15
            if self.left and not self.is_jumping:
                self.player.texture = arcade.load_texture(self.textures[self.i + 5]).flip_horizontally()
            elif not self.is_jumping:
                self.player.texture = arcade.load_texture(self.textures[self.i + 5])
        else:
            self.gravity = GRAVITY
            self.jump_speed = JUMP_SPEED
        self.physics_engine.gravity_constant = self.gravity

        on_ladder = self.physics_engine.is_on_ladder()
        if on_ladder:
            self.player.texture = arcade.load_texture(self.textures[0])
            if self.up and not self.down:
                self.player.change_y = PLAYER_SPEED
                self.player.texture = arcade.load_texture(self.textures[self.i])
            elif self.down and not self.up:
                self.player.change_y = -PLAYER_SPEED
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


        elif not self.is_jumping and not self.was_jumping and not on_ladder and not arcade.check_for_collision_with_list(
                self.player,
                self.water_list):
            if self.left:
                self.player.texture = arcade.load_texture(self.textures[self.i + 7]).flip_horizontally()
            elif self.right:
                self.player.texture = arcade.load_texture(self.textures[self.i + 7])
            else:
                self.player.texture = arcade.load_texture(self.textures[4])

        self.physics_engine.update()

        check = arcade.check_for_collision_with_list(self.player, self.dont_items_list)
        for item in check:
            item.remove_from_sprite_lists()
            self.coll_items_list.append(item)

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

    def create_dust_effect(self):
        for i in range(random.randint(15, 21)):
            e = DustParticle(self.player.center_x, self.player.bottom)
            self.dust_particles.append(e)
