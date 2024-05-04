import pickle
import argparse
from sys import exit
from enum import Enum, auto
import layouts
from sounds import *
from board_class import Board
from graphics import *
from options import Options
from ui_elements import InitializeButtons, InitializeDialogWindows, InitializeToggles


def main():
    # Processes command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scale", type=int, choices=range(1, 11), default=3,
                        help="Sets the scaling factor. Must be a value between 1 and 10.")
    args = parser.parse_args()
    # Instantiates a Game object.
    game = Game(args)
    # Starts the game.
    game.game_loop()


class Game:
    class GameStates(Enum):
        """Enumerates game states."""
        GAME = auto()
        MAIN_MENU = auto()
        LAYOUT_MENU = auto()
        SETTINGS_MENU = auto()
        REALLY_QUIT = auto()
        REALLY_RESET = auto()

    def __init__(self, args):
        # Instantiates a clock.
        self.clock = pygame.time.Clock()
        # Loads settings from options.dat; If not successful, loads defaults.
        try:
            with open("./options.dat", "rb") as in_file:
                self.options = pickle.load(in_file)
        except (OSError, pickle.UnpicklingError):
            self.options = Options("en", True, True)
        # Loads graphics.
        self.gfx = Graphics(self.options.lang, args.scale)
        # Loads sounds.
        self.snd = Sounds()
        # Sets default state to MAIN_MENU.
        self.state = self.GameStates.MAIN_MENU
        # Instantiates a board object, which controls and displays all actual gameplay.
        self.board = Board(layouts.layouts[0],
                           self.gfx.board_surface,
                           self.gfx.display,
                           self.gfx.BOARD_POS,
                           self.gfx.scaling_factor,
                           self.gfx.tile_smooth,
                           self.gfx.tile_hole,
                           self.gfx.peg,
                           self.gfx.highlight,
                           self.gfx.highlight_full,
                           peg_move_snd=self.snd.peg_move,
                           snap_back_snd=self.snd.snap_back,
                           victory_snd=self.snd.victory,
                           defeat_snd=self.snd.defeat,
                           options=self.options)
        # Assigns methods to states; When game state changes, its corresponding method will be called.
        self.game_state_methods = {
            self.GameStates.GAME: self.gameplay,
            self.GameStates.MAIN_MENU: self.main_menu,
            self.GameStates.LAYOUT_MENU: self.layout_menu,
            self.GameStates.SETTINGS_MENU: self.settings_menu,
            self.GameStates.REALLY_QUIT: self.really_quit,
            self.GameStates.REALLY_RESET: self.really_reset
        }
        # Assigns methods and arguments to buttons. When a button gets clicked, the assigned method will be called.
        self.button_methods = {
            "play": {"method": self.switch_state, "args": (self.GameStates.LAYOUT_MENU,)},
            "settings": {"method": self.switch_state, "args": (self.GameStates.SETTINGS_MENU,)},
            "quit_game": {"method": exit, "args": (0,)},
            "layout_1": {"method": self.set_layout_and_start, "args": (0,)},
            "layout_2": {"method": self.set_layout_and_start, "args": (1,)},
            "layout_3": {"method": self.set_layout_and_start, "args": (2,)},
            "layout_4": {"method": self.set_layout_and_start, "args": (3,)},
            "layout_5": {"method": self.set_layout_and_start, "args": (4,)},
            "layout_back": {"method": self.switch_state, "args": (self.GameStates.MAIN_MENU,)},
            "undo": {"method": self.board.undo, "args": None,
                     "active_condition": self.board.undo_stack},
            "restart": {"method": self.switch_state, "args": (self.GameStates.REALLY_RESET,),
                        "active_condition": self.board.undo_stack},
            "exit_game": {"method": self.switch_state, "args": (self.GameStates.REALLY_QUIT,)},
            "dialog_quit_yes": {"method": self.switch_state, "args": (self.GameStates.MAIN_MENU,)},
            "dialog_quit_no": {"method": self.switch_state, "args": (self.GameStates.GAME,)},
            "dialog_restart_yes": {"method": self.reset_board, "args": None},
            "dialog_restart_no": {"method": self.switch_state, "args": (self.GameStates.GAME,)},
            "cancel": {"method": self.cancel_settings, "args": None},
            "apply": {"method": self.apply_settings, "args": None}
        }
        # Assigns methods and arguments to toggles. When a toggle gets switched, the assigned method will be called.
        self.toggle_methods = {
            "english_toggle_pressed": self.english_toggle_pressed,
            "polski_toggle_pressed": self.polski_toggle_pressed
        }
        # Initializes UI elements.
        self.buttons = InitializeButtons(self.gfx, self.snd, self.options, self.button_methods)
        self.dialog_windows = InitializeDialogWindows(self.gfx, self.options)
        self.toggles = InitializeToggles(self.gfx, self.snd, self.options, self.toggle_methods)

    def switch_state(self, state: GameStates) -> None:
        """Changes the game state."""
        self.state = state

    def set_layout_and_start(self, layout: int) -> None:
        """Loads a chosen layout into the board and changes game state to GAME."""
        self.board.load_layout(layouts.layouts[layout])
        self.switch_state(self.GameStates.GAME)

    def reset_board(self) -> None:
        """Moves all pegs to their starting positions, resets move count and clears the undo stack."""
        self.board.reset_pegs()
        self.state = self.GameStates.GAME

    def apply_settings(self) -> None:
        """
        Applies settings changes according to the state of their corresposing switches, saves the settings
        to options.dat, and changes the game state to MAIN_MENU.
        """
        # Reads the state of toggle switches.
        self.board.play_sounds = self.options.play_sounds = self.toggles.sound.is_on
        self.board.show_highlights = self.options.show_highlights = self.toggles.highlight.is_on
        self.options.lang = "en" if self.toggles.english.is_on else "pl"
        # Updates options.dat with the new settings.
        try:
            with open("./options.dat", "wb") as out_file:
                pickle.dump(self.options, out_file)
        except (OSError, pickle.PicklingError):
            pass
        self.switch_state(self.GameStates.MAIN_MENU)

    def cancel_settings(self) -> None:
        """Goes back to the main menu without saving the changes made to Settings; Resets the switches."""
        self.toggles.sound.is_on = self.options.play_sounds
        self.toggles.highlight.is_on = self.options.play_sounds
        self.switch_state(self.GameStates.MAIN_MENU)

    def english_toggle_pressed(self) -> None:
        """Radio button behavior: deactivates Polski if English has been activated."""
        self.toggles.polski.is_on = False

    def polski_toggle_pressed(self) -> None:
        """Radio button behavior: deactivates English if Polski has been activated."""
        self.toggles.english.is_on = False

    def main_menu(self, events) -> None:
        """Runs when self.state is MAIN_MENU."""
        self.gfx.display.blit(self.gfx.main_menu_bg, (0, 0))
        for button in self.buttons.main_menu_btns:
            button.update(events)

    def layout_menu(self, events) -> None:
        """Runs when self.state is LAYOUT_MENU."""
        self.gfx.display.blit(self.gfx.layout_menu_bg, (0, 0))
        for button in self.buttons.layout_menu_btns:
            button.update(events)

    def settings_menu(self, events) -> None:
        """Runs when self.state is LAYOUT_MENU."""
        self.gfx.display.blit(self.gfx.settings_menu_bg, (0, 0))
        self.toggles.sound.update(events)
        self.toggles.highlight.update(events)
        self.toggles.english.update(events)
        self.toggles.polski.update(events)
        for button in self.buttons.settings_btns:
            button.update(events)

    def really_quit(self, events) -> None:
        """Runs when self.state is REALLY_QUIT. Pops up the "Really quit?" dialog window."""
        self.dialog_windows.really_quit.update()
        for button in self.buttons.really_quit_btns:
            button.update(events)

    def really_reset(self, events) -> None:
        """Runs when self.state is REALLY_RESET. Pops up the "Really reset?" dialog window."""
        self.dialog_windows.really_reset.update()
        for button in self.buttons.really_restart_btns:
            button.update(events)

    def gameplay(self, events) -> None:
        """Runs when self.state is GAME. Actual gameplay."""
        self.gfx.display.blit(self.gfx.background, (0, 0))
        # Updates the move counter on the screen.
        gfx_move_count = self.gfx.small_font.render(
            f"{langs.move[self.options.lang]} {self.board.move_count}", False, "#DDDDDD")
        self.gfx.display.blit(gfx_move_count, (16, 50))
        # Updates the board - actual gameplay happens here.
        self.board.process_input(events)
        self.board.draw_board()
        for button in self.buttons.in_game_btns:
            button.update(events)
        # Draws labels on the screen if the game is lost or won.
        if self.board.is_victorious:
            self.gfx.display.blit(self.gfx.victory_label, ({"en": 19, "pl": 20}[self.options.lang], 150))
        elif self.board.is_defeated:
            self.gfx.display.blit(self.gfx.defeat_label, ({"en": 15, "pl": 21}[self.options.lang], 150))

    def game_loop(self) -> None:
        """Main gameplay loop. Calls the relevant method depending on the game state."""
        # Collects events.
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # Calls the method assigned to the current game state and passes events to it.
            if self.state in self.GameStates:
                game_state_method = self.game_state_methods[self.state]
                game_state_method(events)
            # Scales "display" up and blits it onto "screen".
            self.gfx.screen.blit(pygame.transform.scale(self.gfx.display, self.gfx.screen_res), (0, 0))
            # Redraws the screen.
            pygame.display.update()
            # Updates the clock.
            self.clock.tick(self.gfx.FPS)


if __name__ == "__main__":
    main()
