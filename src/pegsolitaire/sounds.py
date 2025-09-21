import pygame
from .asset_loader import load_sound


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.button_press = load_sound("Sounds/button_press.ogg")
        self.toggle_press = load_sound("Sounds/toggle.ogg")
        self.peg_move = load_sound("Sounds/move_peg.ogg")
        self.snap_back = load_sound("Sounds/snap_back.ogg")
        self.defeat = load_sound("Sounds/defeat.ogg")
        self.victory = load_sound("Sounds/victory.ogg")
        
