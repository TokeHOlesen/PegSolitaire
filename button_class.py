import pygame


class Button(pygame.sprite.Sprite):
    """Instantiates a button with the given properties."""
    def __init__(self,
                 *,
                 target_surface: pygame.surface.Surface,
                 command,
                 coords: tuple[int, int],
                 text: str,
                 font_type: str,
                 font_size: int,
                 btn_gfx: pygame.surface.Surface,
                 cmd_args: tuple = None,
                 cmd_kwargs: dict = None,
                 btn_gfx_pressed=None,
                 click_sound: pygame.mixer.Sound = None,
                 options=None,
                 res_multi: int = 1,
                 is_active: bool = True,
                 text_color: str = "#000000",
                 inactive_text_color: str = "#999999",
                 text_x_offset: int = 0,
                 text_y_offset: int = 0,
                 active_condition=None):
        """
        :param target_surface: The surface to draw the button on.
        :param command: The function to run when the button is clicked.
        :param coords: Position of the button on the target surface.
        :param text: Text on the button.
        :param font_type: Path to the font to use for the button text.
        :param font_size: The size of the font used for button text.
        :param btn_gfx: Graphic to show when not pressed.
        :param cmd_args: Arguments for the function that runs when button gets clicked.
        :param cmd_kwargs: Keyword arguments for the function that runs when the button gets clicked.
        :param btn_gfx_pressed: Graphic to show when not pressed. If None, btn_gfx rotated 180 degrees will be used.
        :param click_sound: Sound to play when the button is clicked.
        :param options: Options object to change button behavior; optional.
        :param res_multi: If the target surface gets scaled, resolution multiplier.
        :param is_active: Wheter the button is active and can be clicked.
        :param text_color: Color of the button text when the button is active.
        :param inactive_text_color: Color of the button text when the button is inactive.
        :param text_x_offset: How much to shift the button text in the x axis.
        :param text_y_offset: How much to shift the button text in the y axis.
        :param active_condition: If not None, the button will be active if the condition is True, and inactive if False.

        """
        super().__init__()
        self._surface = target_surface
        self._command = command
        self._command_args = cmd_args if cmd_args is not None else ()
        self._command_kwargs = cmd_kwargs if cmd_kwargs is not None else {}
        self._gfx_up = btn_gfx
        self._gfx_down = btn_gfx_pressed if btn_gfx_pressed is not None else pygame.transform.rotate(btn_gfx, 180)
        self._gfx_button = {
            False: self._gfx_up,
            True: self._gfx_down
        }
        self.rect = self._gfx_up.get_rect()
        self.rect.x, self.rect.y = coords
        self._click_sound = click_sound
        self._options = options
        self._res_multi = res_multi
        self._is_active = is_active
        self._text = text
        # Sets text color according to whether self._is_active is True or False
        self._text_color = {
            True: text_color,
            False: inactive_text_color
        }
        self._x_offset = text_x_offset
        self._y_offset = text_y_offset
        self._font = pygame.font.Font(font_type, size=font_size)
        self._is_pressed = False
        self.active_condition = active_condition

    @property
    def is_active(self) -> bool:
        """Checks whether the button is currently set to active or inactive."""
        return self._is_active

    @is_active.setter
    def is_active(self, state: bool) -> None:
        """Sets the button's active state."""
        if type(state) is bool:
            self._is_active = state
        else:
            raise TypeError("is_active must be a boolean value")

    def update_active_state(self) -> None:
        """Evaluates the condition and sets the button's active status accordingly."""
        if self.active_condition is not None:
            self.is_active = bool(self.active_condition)

    def is_mouseover(self) -> bool:
        """Returns true on mouseover"""
        mouse_x, mouse_y = tuple((coord // self._res_multi for coord in pygame.mouse.get_pos()))
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def run_command(self) -> None:
        """Calls the function associated with the button"""
        if self.is_mouseover() and self._is_active:
            self._command(*self._command_args, **self._command_kwargs)

    def display(self) -> None:
        """Draws the button on self._surface."""
        # Renders the text, with color depending on whether it is active
        button_text = self._font.render(self._text, False, self._text_color[self._is_active])
        # Draws the button graphic, with the button shown as either pressed or not pressed
        # Only draws the pressed version is both ._is_pressed and ._is_active are True
        self._surface.blit(self._gfx_button[self._is_pressed and self._is_active], self.rect)
        # Draws the text in the middle of the button
        # If ._is_pressed and ._is_active are both True, shifts the text down and to the right by one pixel
        shift_pos = int(self._is_pressed and self._is_active)
        text_pos_x = self.rect.x + self.rect.width // 2 - button_text.get_width() // 2 + self._x_offset + shift_pos
        text_pos_y = self.rect.y + self._y_offset + shift_pos
        self._surface.blit(button_text, (text_pos_x, text_pos_y))

    def play_sound(self) -> None:
        """Plays a sound if a sound has been passed as an argument and an options object exists and is set to play."""
        if self._options is not None and self._options.play_sounds and self._click_sound is not None:
            self._click_sound.play()

    def update(self, events) -> None:
        """
        Checks for mouse button presses and draws the button accordingly.
        If the left mouse button is released when the cursor is hovering above the button, executes command.
        """
        self.update_active_state()
        if self.is_active:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    # Only runs command if the button is released and left mouse button is not still pressed
                    # This is to make sure that the action doesn't trigger when user releases a different button instead
                    if self._is_pressed and not pygame.mouse.get_pressed()[0]:
                        self._is_pressed = False
                        self.play_sound()
                        self.run_command()
            # Sets the button to pressed if the user presses the left mouse button when the cursor is hovering over it,
            # or if they drag the cursor over the button with the left mouse button being held down.
            if self.is_mouseover() and pygame.mouse.get_pressed()[0]:
                self._is_pressed = True
            # Sets the button to not pressed if the user moves the mouse cursor away
            if self._is_pressed and not self.is_mouseover():
                self._is_pressed = False
        self.display()
