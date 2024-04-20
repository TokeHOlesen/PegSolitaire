import pygame
from options import Options


class Toggle(pygame.sprite.Sprite):
    """A button-like toggle that can be switched On or Off."""
    def __init__(self,
                 target_surface: pygame.surface.Surface,
                 pos: tuple[int, int],
                 res_multi: int,
                 gfx_off: pygame.surface.Surface,
                 gfx_on: pygame.surface.Surface = None,
                 click_sound: pygame.mixer.Sound = None,
                 options: Options = None,
                 is_on: bool = False,
                 is_radio: bool = False,
                 command=None):
        """
        :param target_surface: The surface the game element will be drawn on.
        :param pos: Position of the tile on the board grid.
        :param res_multi: Resolution multiplier. By how much the display will be scaled on screen.
        :param gfx_off: Graphics shown when OFF.
        :param gfx_on: Graphics shown when ON.
        :param click_sound: The sounds to play when the switch gets flipped.
        :param options: An object containing the game settings; optional.
        :param is_on: Current state.
        :param is_radio: True if the switch should behave as a radio button.
        :param command: Function to call when the toggle is clicked.
        """
        super().__init__()
        self._target_surface = target_surface
        self._gfx_off = gfx_off
        self._gfx_on = gfx_on if gfx_on is not None else pygame.transform.rotate(gfx_off, 180)
        self._gfx_toggle = {
            False: self._gfx_off,
            True: self._gfx_on
        }
        self._rect = self._gfx_off.get_rect()
        self._rect.x, self._rect.y = pos
        self._click_sound = click_sound
        self._options = options
        self._res_multi = res_multi
        self.is_on = is_on
        self._is_radio = is_radio
        self._command = command

    def is_mouseover(self) -> bool:
        """Returns True if the mouse cursor is above the object."""
        mouse_x, mouse_y = tuple((coord // self._res_multi for coord in pygame.mouse.get_pos()))
        if self._rect.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def play_sound(self) -> None:
        """If an options object has been passed and allows playing sound and a sound has been passed, plays a sound."""
        if self._options is not None and self._options.play_sounds and self._click_sound is not None:
            self._click_sound.play()

    def execute_command(self) -> None:
        """If a method has been passed as an argument, calls it."""
        if self._command is not None:
            self._command()

    def display(self) -> None:
        """Blits the toggle on the target surface."""
        self._target_surface.blit(self._gfx_toggle[self.is_on], self._rect)

    def update(self, events) -> None:
        """Flips state when clicked, and draws on display."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouseover():
                    # Flips the switch, unless it's a radio button and already on.
                    if (self._is_radio and not self.is_on) or not self._is_radio:
                        self.is_on = not self.is_on
                        self.execute_command()
                        self.play_sound()

        self.display()
