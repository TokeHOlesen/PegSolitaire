import pygame


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.button_press = pygame.mixer.Sound("./Assets/Sounds/button_press.ogg")
        self.toggle_press = pygame.mixer.Sound("./Assets/Sounds/toggle.ogg")
        self.peg_move = pygame.mixer.Sound("./Assets/Sounds/move_peg.ogg")
        self.snap_back = pygame.mixer.Sound("Assets/Sounds/snap_back.ogg")
        self.defeat = pygame.mixer.Sound("./Assets/Sounds/defeat.ogg")
        self.victory = pygame.mixer.Sound("./Assets/Sounds/victory.ogg")
