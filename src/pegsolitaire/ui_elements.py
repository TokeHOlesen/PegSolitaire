from . import languages as langs
from .button_class import Button
from .dialog_window_class import DialogWindow
from .toggle_class import Toggle


class InitializeButtons:
    """Initializes all buttons."""
    def __init__(self, gfx_object, snd_object, options_object, button_methods):
        self.gfx = gfx_object
        self.snd = snd_object
        self.options = options_object
        self.btn_methods = button_methods

        # Data to use when instantiating main menu buttons. If not specified, defaults will be used.
        self.main_menu_btn_data = {
            "play": {
                "command": self.btn_methods["play"]["method"],
                "args": self.btn_methods["play"]["args"],
                "btn_gfx": self.gfx.main_menu_btn,
                "btn_x_pos": 60,
                "btn_y_pos": 88,
                "text": langs.play,
                "font_type": "Graphics/Retron2000.ttf",
                "font_size": 27,
                "text_y_offset": -5
            },
            "settings": {
                "command": self.btn_methods["settings"]["method"],
                "args": self.btn_methods["settings"]["args"],
                "btn_gfx": self.gfx.main_menu_btn,
                "btn_x_pos": 60,
                "btn_y_pos": 128,
                "text": langs.settings,
                "font_type": "Graphics/Retron2000.ttf",
                "font_size": 27,
                "text_y_offset": -5
            },
            "quit_game": {
                "command": self.btn_methods["quit_game"]["method"],
                "args": self.btn_methods["quit_game"]["args"],
                "btn_gfx": self.gfx.main_menu_btn,
                "btn_x_pos": 60,
                "btn_y_pos": 168,
                "text": langs.quit_game,
                "font_type": "Graphics/Retron2000.ttf",
                "font_size": 27,
                "text_y_offset": -5
            }
        }

        # Data to use when instantiating layout menu buttons. If not specified, defaults will be used.
        self.layout_menu_btn_data = {
            "layout_1": {
                "command": self.btn_methods["layout_1"]["method"],
                "args": self.btn_methods["layout_1"]["args"],
                "btn_gfx": self.gfx.layout_menu_btn,
                "btn_x_pos": 80,
                "btn_y_pos": 65,
                "text": langs.layout_english
            },
            "layout_2": {
                "command": self.btn_methods["layout_2"]["method"],
                "args": self.btn_methods["layout_2"]["args"],
                "btn_gfx": self.gfx.layout_menu_btn,
                "btn_x_pos": 80,
                "btn_y_pos": 90,
                "text": langs.layout_german
            },
            "layout_3": {
                "command": self.btn_methods["layout_3"]["method"],
                "args": self.btn_methods["layout_3"]["args"],
                "btn_gfx": self.gfx.layout_menu_btn,
                "btn_x_pos": 80,
                "btn_y_pos": 115,
                "text": langs.layout_french
            },
            "layout_4": {
                "command": self.btn_methods["layout_4"]["method"],
                "args": self.btn_methods["layout_4"]["args"],
                "btn_gfx": self.gfx.layout_menu_btn,
                "btn_x_pos": 80,
                "btn_y_pos": 140,
                "text": langs.layout_diamond
            },
            "layout_5": {
                "command": self.btn_methods["layout_5"]["method"],
                "args": self.btn_methods["layout_5"]["args"],
                "btn_gfx": self.gfx.layout_menu_btn,
                "btn_x_pos": 80,
                "btn_y_pos": 165,
                "text": langs.layout_asymmetrical
            },
            "layout_back": {
                "command": self.btn_methods["layout_back"]["method"],
                "args": self.btn_methods["layout_back"]["args"],
                "btn_gfx": self.gfx.back_btn,
                "btn_x_pos": 95,
                "btn_y_pos": 203,
                "text": langs.back_button
            }
        }

        # Data to use when instantiating in game buttons. If not specified, defaults will be used.
        self.in_game_btn_data = {
            "undo": {
                "command": self.btn_methods["undo"]["method"],
                "args": self.btn_methods["undo"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 12,
                "btn_y_pos": 12,
                "text": langs.undo,
                "active_condition": self.btn_methods["undo"]["active_condition"]
            },
            "restart": {
                "command": self.btn_methods["restart"]["method"],
                "args": self.btn_methods["restart"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 12,
                "btn_y_pos": 178,
                "text": langs.restart,
                "active_condition": self.btn_methods["restart"]["active_condition"]
            },
            "exit_game": {
                "command": self.btn_methods["exit_game"]["method"],
                "args": self.btn_methods["exit_game"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 12,
                "btn_y_pos": 208,
                "text": langs.exit_game
            }
        }

        # Data to use when instantiating "really quit" dialog window buttons. If not specified, defaults will be used.
        self.really_quit_btn_data = {
            "dialog_quit_yes": {
                "command": self.btn_methods["dialog_quit_yes"]["method"],
                "args": self.btn_methods["dialog_quit_yes"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 86,
                "btn_y_pos": 124,
                "text": langs.yes
            },
            "dialog_quit_no": {
                "command": self.btn_methods["dialog_quit_no"]["method"],
                "args": self.btn_methods["dialog_quit_no"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 166,
                "btn_y_pos": 124,
                "text": langs.no
            }
        }

        # Data to use when instantiating "really restart" dialog window buttons. If not specified, defaults will be used
        self.really_restart_btn_data = {
            "dialog_restart_yes": {
                "command": self.btn_methods["dialog_restart_yes"]["method"],
                "args": self.btn_methods["dialog_restart_yes"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 86,
                "btn_y_pos": 124,
                "text": langs.yes
            },
            "dialog_restart_no": {
                "command": self.btn_methods["dialog_restart_no"]["method"],
                "args": self.btn_methods["dialog_restart_no"]["args"],
                "btn_gfx": self.gfx.in_game_btn,
                "btn_x_pos": 166,
                "btn_y_pos": 124,
                "text": langs.no
            }
        }

        # Data to use when instantiating the settings menu buttons. If not specified, defaults will be used.
        self.settings_btn_data = {
            "cancel": {
                "command": self.btn_methods["cancel"]["method"],
                "args": self.btn_methods["cancel"]["args"],
                "btn_gfx": self.gfx.settings_menu_btn,
                "btn_x_pos": 64,
                "btn_y_pos": 194,
                "text": langs.cancel
            },
            "apply": {
                "command": self.btn_methods["apply"]["method"],
                "args": self.btn_methods["apply"]["args"],
                "btn_gfx": self.gfx.settings_menu_btn,
                "btn_x_pos": 176,
                "btn_y_pos": 194,
                "text": langs.apply
            }
        }

        # Defaults to use when no values are specified.
        self.defaults = {
            "click_sound": self.snd.button_press,
            "is_active": True,
            "font_type": "Graphics/superstar_memesbruh03.ttf",
            "font_size": 16,
            "text_color": "#EEEEEE",
            "inactive_text_color": "#999999",
            "text_x_offset": 0,
            "text_y_offset": 2,
            "active_condition": None
        }

        # Instantiates the buttons using the data provided. Each list contains button for a particular game state.
        self.main_menu_btns = [Button(**self.generate_button_kwargs(
            self.main_menu_btn_data, key)) for key in self.main_menu_btn_data.keys()]
        self.layout_menu_btns = [Button(**self.generate_button_kwargs(
            self.layout_menu_btn_data, key)) for key in self.layout_menu_btn_data.keys()]
        self.in_game_btns = [Button(**self.generate_button_kwargs(
            self.in_game_btn_data, key)) for key in self.in_game_btn_data.keys()]
        self.really_quit_btns = [Button(**self.generate_button_kwargs(
            self.really_quit_btn_data, key)) for key in self.really_quit_btn_data.keys()]
        self.really_restart_btns = [Button(**self.generate_button_kwargs(
            self.really_restart_btn_data, key)) for key in self.really_restart_btn_data.keys()]
        self.settings_btns = [Button(**self.generate_button_kwargs(
            self.settings_btn_data, key)) for key in self.settings_btn_data.keys()]

    def generate_button_kwargs(self, menu: dict, btn_name: str) -> dict:
        """Returns a set of keyword arguments to pass to the Button class constructor."""
        this_btn = menu[btn_name]
        button_kwargs = {
            "target_surface": self.gfx.display,
            "res_multi": self.gfx.scaling_factor,
            "command": this_btn["command"],
            "coords": (this_btn["btn_x_pos"], this_btn["btn_y_pos"]),
            "text": this_btn["text"][self.options.lang],
            "font_type": this_btn["font_type"] if "font_type" in this_btn.keys() else self.defaults["font_type"],
            "font_size": this_btn["font_size"] if "font_size" in this_btn.keys() else self.defaults["font_size"],
            "btn_gfx": this_btn["btn_gfx"],
            "cmd_args": this_btn["args"],
            "btn_gfx_pressed": this_btn["btn_gfx_pressed"] if "btn_gfx_pressed" in this_btn.keys() else None,
            "click_sound": this_btn["click_sound"] if "click_sound" in this_btn.keys() else self.defaults[
                "click_sound"],
            "options": self.options,
            "is_active": this_btn["is_active"] if "is_active" in this_btn.keys() else self.defaults["is_active"],
            "text_color": this_btn["text_color"] if "text_color" in this_btn.keys() else self.defaults["text_color"],
            "inactive_text_color": this_btn["inactive_text_color"] if "inactive_text_color" in this_btn.keys() else
            self.defaults["inactive_text_color"],
            "text_x_offset": this_btn["text_x_offset"] if "text_x_offset" in this_btn.keys() else self.defaults[
                "text_x_offset"],
            "text_y_offset": this_btn["text_y_offset"] if "text_y_offset" in this_btn.keys() else self.defaults[
                "text_y_offset"],
            "active_condition": this_btn["active_condition"] if "active_condition" in this_btn.keys() else
            self.defaults["active_condition"],
        }
        return button_kwargs


class InitializeDialogWindows:
    """Initializes the dialog windows."""
    def __init__(self, gfx_object, options_object):
        self.gfx = gfx_object
        self.options = options_object
        self.really_quit = DialogWindow(langs.really_quit[self.options.lang],
                                        self.gfx.display, (68, 56), self.gfx.dialog_window)
        self.really_reset = DialogWindow(langs.really_reset[self.options.lang],
                                         self.gfx.display, (68, 56), self.gfx.dialog_window)


class InitializeToggles:
    """Initializes a set of toggle switches."""
    def __init__(self, gfx_object, snd_object, options_object, toggle_methods):
        self.gfx = gfx_object
        self.snd = snd_object
        self.options = options_object
        self.methods = toggle_methods
        self.sound = Toggle(self.gfx.display, (240, 68), self.gfx.scaling_factor, self.gfx.toggle_off,
                            self.gfx.toggle_on, is_on=self.options.play_sounds,
                            click_sound=self.snd.toggle_press,
                            options=self.options)
        self.highlight = Toggle(self.gfx.display, (240, 98), self.gfx.scaling_factor, self.gfx.toggle_off,
                                self.gfx.toggle_on, is_on=self.options.show_highlights,
                                click_sound=self.snd.toggle_press, options=self.options)
        self.english = Toggle(self.gfx.display, (136, 128), self.gfx.scaling_factor, self.gfx.en_toggle_off,
                              self.gfx.en_toggle_on, is_on=(self.options.lang == "en"),
                              command=self.methods["english_toggle_pressed"], click_sound=self.snd.toggle_press,
                              options=self.options, is_radio=True)
        self.polski = Toggle(self.gfx.display, (208, 128), self.gfx.scaling_factor, self.gfx.pl_toggle_off,
                             self.gfx.pl_toggle_on, is_on=(self.options.lang == "pl"),
                             command=self.methods["polski_toggle_pressed"], click_sound=self.snd.toggle_press,
                             options=self.options, is_radio=True)
