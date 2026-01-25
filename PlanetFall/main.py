import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from LaunchView import LaunchView


def setup_game(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
    game = arcade.Window(width, height, title)
    return game


def main():
    window = setup_game()
    launch_view = LaunchView()
    window.show_view(launch_view)
    arcade.run()


if __name__ == "__main__":
    main()
