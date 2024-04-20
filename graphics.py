import pygame
import languages as langs
from create_surface import create_simple_surface


class Graphics:
    # Intializes pygame
    pygame.init()
    # Game running speed.
    FPS = 60
    # Dimensions of board_surface.
    BOARD_DIMENSIONS = (216, 216)
    # The position of the upper left corner of the board, relative to the target surface.
    # In practical terms, the position of board_surface on the "display" surface.
    BOARD_POS = (92, 12)
    # Effective resolution of the display.
    # Before blitting on screen, display will be scaled up by RES_MULTI.
    DISPLAY_WIDTH = 320
    DISPLAY_HEIGHT = 240
    # Resolution multiplier.
    RES_MULTI = 3
    # Colors for rendering text
    TEXT_WHITE = "#EEEEEE"
    TEXT_RED = "#11FF11"
    TEXT_GREEN = "#FF1916"

    def __init__(self, lang):
        """Loads the graphics and initializes the graphics variables."""
        # Display variables
        self.screen_res = (self.DISPLAY_WIDTH * self.RES_MULTI, self.DISPLAY_HEIGHT * self.RES_MULTI)
        self.screen = pygame.display.set_mode(self.screen_res)
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.board_surface = pygame.Surface(self.BOARD_DIMENSIONS)
        pygame.display.set_caption("Peg Solitaire")
        pygame.display.set_icon(pygame.image.load("./Assets/Graphics/icon.ico").convert_alpha())
        # Fonts
        self.large_font = pygame.font.Font("./Assets/Graphics/Retron2000.ttf", 27)
        self.small_font = pygame.font.Font("./Assets/Graphics/superstar_memesbruh03.ttf", 16)

        # Game tiles
        self.tile_smooth = pygame.image.load("Assets/Graphics/tile_smooth.png").convert()
        self.tile_hole = pygame.image.load("Assets/Graphics/tile_hole.png").convert()
        self.peg = pygame.image.load("Assets/Graphics/peg.png").convert_alpha()
        self.highlight = pygame.image.load("Assets/Graphics/highlight.png").convert_alpha()
        self.highlight_full = pygame.image.load("Assets/Graphics/highlight_full.png").convert_alpha()

        # Game background
        self.background = pygame.image.load("Assets/Graphics/background.png").convert()

        # Main screen logo
        self.logo = {
            "en": pygame.image.load("Assets/Graphics/logo_en.png").convert_alpha(),
            "pl": pygame.image.load("Assets/Graphics/logo_pl.png").convert_alpha()
        }

        # Buttons
        self.main_menu_btn = create_simple_surface(200, 30)
        self.back_btn = create_simple_surface(130, 20)
        self.layout_menu_btn = create_simple_surface(160, 20)
        self.settings_menu_btn = create_simple_surface(80, 20)
        self.in_game_btn = create_simple_surface(68, 20)

        # On / off toggle switches
        self.dialog_window = create_simple_surface(184, 98)
        self.toggle_off = create_simple_surface(40, 20)
        self.toggle_on = pygame.transform.rotate(self.toggle_off, 180)
        text_toggle_off = self.small_font.render("OFF", False, self.TEXT_GREEN)
        text_toggle_on = self.small_font.render("ON", False, self.TEXT_RED)
        self.toggle_off.blit(text_toggle_off, (8, 2))
        self.toggle_on.blit(text_toggle_on, (12, 3))

        # English toggle switch
        self.en_toggle_off = create_simple_surface(72, 20)
        self.en_toggle_on = pygame.transform.rotate(self.en_toggle_off, 180)
        text_en_toggle_off = self.small_font.render("English", False, self.TEXT_GREEN)
        text_en_toggle_on = self.small_font.render("English", False, self.TEXT_RED)
        self.en_toggle_off.blit(text_en_toggle_off, (8, 2))
        self.en_toggle_on.blit(text_en_toggle_on, (9, 3))

        # Polish toggle switch
        self.pl_toggle_off = create_simple_surface(72, 20)
        self.pl_toggle_on = pygame.transform.rotate(self.pl_toggle_off, 180)
        text_pl_toggle_off = self.small_font.render("Polski", False, self.TEXT_GREEN)
        text_pl_toggle_on = self.small_font.render("Polski", False, self.TEXT_RED)
        self.pl_toggle_off.blit(text_pl_toggle_off, (12, 2))
        self.pl_toggle_on.blit(text_pl_toggle_on, (13, 3))

        # Renders all text labels
        self.choose_lt_label = self.large_font.render(langs.choose_layout[lang], False, self.TEXT_WHITE)
        self.victory_label = self.small_font.render(langs.victory[lang], False, self.TEXT_RED)
        self.defeat_label = self.small_font.render(langs.defeat[lang], False, self.TEXT_GREEN)
        self.settings_label = self.large_font.render(langs.settings[lang], False, self.TEXT_WHITE)
        self.sound_toggle_label = self.small_font.render(langs.sound_toggle[lang], False, self.TEXT_WHITE)
        self.highlight_toggle_label = self.small_font.render(langs.highlight_toggle[lang], False, self.TEXT_WHITE)
        self.language_toggle_label = self.small_font.render(langs.language_toggle[lang], False, self.TEXT_WHITE)
        self.rest_req_label = self.small_font.render(langs.restart_required[lang], False, self.TEXT_WHITE)
        self.copyright_label = self.small_font.render("(c) 2024 Toke Henrik Olesen", False, "#E5E5E5")

        # Renders the main menu background
        self.main_menu_bg = pygame.surface.Surface((self.background.get_width(), self.background.get_height()))
        self.main_menu_bg.blit(self.background, (0, 0))
        self.main_menu_bg.blit(self.logo[lang], (24, 6))
        self.main_menu_bg.blit(self.copyright_label,
                               ((self.DISPLAY_WIDTH - self.copyright_label.get_width()) // 2, 214))

        # Renders the layout menu background
        self.layout_menu_bg = pygame.surface.Surface((self.background.get_width(), self.background.get_height()))
        self.layout_menu_bg.blit(self.background, (0, 0))
        self.layout_menu_bg.blit(self.choose_lt_label,
                                 ((self.DISPLAY_WIDTH - self.choose_lt_label.get_width()) // 2, 10))

        # Renders the settings menu background
        self.settings_menu_bg = pygame.surface.Surface((self.background.get_width(), self.background.get_height()))
        self.settings_menu_bg.blit(self.background, (0, 0))
        self.settings_menu_bg.blit(self.settings_label,
                                   ((self.DISPLAY_WIDTH - self.settings_label.get_width()) // 2, 10))
        self.settings_menu_bg.blit(self.sound_toggle_label, (38, 70))
        self.settings_menu_bg.blit(self.highlight_toggle_label, (38, 100))
        self.settings_menu_bg.blit(self.language_toggle_label, (38, 130))
        self.settings_menu_bg.blit(self.rest_req_label,
                                   ((self.DISPLAY_WIDTH - self.rest_req_label.get_width()) // 2, 154))
