import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from MenuView import MenuView


def setup_game(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
    game = arcade.Window(width, height, title)
    return game


def main():
    window = setup_game()
    menu_view = MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
