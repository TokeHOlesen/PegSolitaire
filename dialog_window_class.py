import pygame


class DialogWindow(pygame.sprite.Sprite):
    """Draws a dialog window, with the given text, and a shadow."""
    def __init__(self,
                 message: str,
                 surface: pygame.surface.Surface,
                 pos: tuple[int, int],
                 gfx_dialog_window: pygame.surface.Surface,
                 font="./Assets/Graphics/superstar_memesbruh03.ttf",
                 font_size=16):
        """
        :param message: The text to display.
        :param surface: The surface the game element will be drawn on.
        :param pos: Position of the surface on the screen.
        :param gfx_dialog_window: Graphics to use for this game element.
        :param font: Font used to render the text.
        :param font_size: What size to render the text at.
        """
        super().__init__()
        self._surface = surface
        self.graphic = gfx_dialog_window
        self.rect = self.graphic.get_rect()
        self.rect.x, self.rect.y = pos
        # Creates a "shadow" surface the same size as the dialog window, and makes it dark grey.
        self.shadow = pygame.Surface((self.rect.width, self.rect.height))
        self.shadow.fill("#333333")
        self.message_font = pygame.font.Font(font, font_size)
        self.message = self.message_font.render(message, False, "#EEEEEE")
        self.message_x_pos = self.rect.x + self.rect.width // 2 - self.message.get_width() // 2

    def display(self) -> None:
        """Blits the dialog window on the target surface: the shadow, the window, and the text, in that order."""
        self._surface.blit(self.shadow, (self.rect.x + 5, self.rect.y + 5))
        self._surface.blit(self.graphic, self.rect)
        self._surface.blit(self.message, (self.message_x_pos, self.rect.y + 25))

    def update(self) -> None:
        self.display()
