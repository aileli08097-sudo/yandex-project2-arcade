import arcade
from PauseView import PauseView
from pyglet.graphics import Batch


class Level(arcade.View):
    def __init__(self, saved_state):
        super().__init__()
        self.level = saved_state.get('level')
        self.player = saved_state.get('player')
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.enemies_list = saved_state.get('enemies')
        self.items_list = saved_state.get('items')
        self.paused = False
        self.game_over = False
        self.win = False
        self.timer = 0
        self.batch = Batch()
        self.space_text = arcade.Text("Нажмите ESC, чтобы приостановить", 120,
                                      self.window.height - 30,
                                      arcade.color.WHITE, font_size=10, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.enemies_list.draw()
        self.items_list.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        if not self.paused and not self.win and not self.game_over:
            ...

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause_game()

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
