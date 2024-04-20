import pygame


class Tile(pygame.sprite.Sprite):
    """Represents a tile on the Board."""
    def __init__(self,
                 target_surface: pygame.surface.Surface,
                 pos: tuple[int, int],
                 tile_type: pygame.surface.Surface):
        """
        :param target_surface: The surface the game element will be drawn on.
        :param pos: Position of the tile on the board grid.
        :param tile_type: Graphics to use for this game element.
        """
        super().__init__()
        self._target_surface = target_surface
        self.graphic = tile_type
        self.rect = self.graphic.get_rect()
        self.coords = pos
        x_pos, y_pos = pos
        self.rect.x, self.rect.y = x_pos * self.rect.width, y_pos * self.rect.height

    def display(self) -> None:
        """Blits the tile on the target surface."""
        self._target_surface.blit(self.graphic, self.rect)

    def update(self) -> None:
        self.display()


class Peg(Tile):
    """Represents a Peg on the Board."""
    def __init__(self,
                 target_surface: pygame.surface.Surface,
                 pos: tuple[int, int],
                 board_size: int,
                 board_pos: tuple[int, int],
                 res_multi: int,
                 tile_type: pygame.surface.Surface):
        """
        :param board_size: The length of the side of the board that this element will be placed on, in tiles.
        :param board_pos: The position of the board's surface on the target surface, in pixels.
        :param res_multi: Resolution multiplier, needed for correcting mouse cursor position values.
        """
        super().__init__(target_surface, pos, tile_type)
        self.is_being_dragged = False
        self._board_size = board_size
        self._board_pos = board_pos
        self._res_multiplier = res_multi
        self._mouse_offset = (0, 0)
        self._old_rect = self.rect.copy()
        # Set to True when the peg is being deleted and is fading out. It's alpha value will decrease each cycle.
        self._fading_out = False
        self._alpha = 255
        # Set to True when the peg has been released outside of a valid destination and is being moved back to where it
        # was taken from.
        self.is_snapping_back = False
        # How fast the peg moves back to its previous position.
        self._speed = 12
        # Vectors: position when released, destination (original position), direction and velocity
        self._position = None
        self._destination = None
        self._direction = None
        self._velocity = None

    @property
    def grid_coords(self) -> tuple[int, int]:
        """
        Returns the x position of the peg within the grid (in terms of tiles).
        Return value is limited to board size, in case user drags peg outside.
        """
        return (int(min(self.rect.centerx // self.rect.width, self._board_size - 1)),
                int(min(self.rect.centery // self.rect.height, self._board_size - 1)))

    @property
    def old_grid_coords(self) -> tuple[int, int]:
        """Returns the coords within the grid from which the peg was moved."""
        return (int(self._old_rect.centerx // self._old_rect.width),
                int(self._old_rect.centery // self._old_rect.height))

    @property
    def mouse_offset(self) -> tuple[int, int]:
        """
        Returns the mouse cursor offset for the peg object.
        It ensures that the position of the peg relative to the mouse cursor remains constant while dragging.
        """
        return self._mouse_offset

    @mouse_offset.setter
    def mouse_offset(self, mouse_pos: tuple[int, int]) -> None:
        """Sets the mouse offset to the current different between the position of the cursor and the dragged peg."""
        mouse_x, mouse_y = mouse_pos
        self._mouse_offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

    def fade_out(self) -> None:
        """Begins to fade the button out. When done, it will be removed."""
        self._fading_out = True

    def snap_back(self) -> None:
        """Returns the peg to the position it was dragged from."""
        if self.rect != self._old_rect:
            self.is_snapping_back = True
            # Initializes the vectors.
            self._position = pygame.math.Vector2(self.rect.x, self.rect.y)
            self._destination = pygame.math.Vector2(self._old_rect.x, self._old_rect.y)
            self._direction = self._destination - self._position
            self._velocity = self._direction.normalize() * self._speed

    def is_mouseover(self, mouse_pos: tuple[int, int]) -> bool:
        """Returns True if the mouse cursor is above this peg."""
        mouse_x, mouse_y = mouse_pos[0] - self._board_pos[0], mouse_pos[1] - self._board_pos[1]
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        return False

    def move_to_new_pos(self) -> None:
        """Updates the position of the peg, both in terms of board grid and in terms of pixels (on board surface)."""
        new_x, new_y = self.grid_coords
        self.rect.x, self.rect.y = new_x * self.rect.width, new_y * self.rect.height
        self._old_rect = self.rect.copy()

    def update(self) -> None:
        """Draws the peg on the board surface."""
        # If the peg is being dragged, updates its coords every frame to keep a constant position relative to the cursor
        if self.is_being_dragged:
            mouse_x, mouse_y = tuple((coord // self._res_multiplier for coord in pygame.mouse.get_pos()))
            x_offset, y_offset = self.mouse_offset
            self.rect.x = min(max(0, mouse_x + x_offset), self._target_surface.get_width() - int(self.rect.width))
            self.rect.y = min(max(0, mouse_y + y_offset), self._target_surface.get_height() - int(self.rect.height))
        # If self._fading_out is set to true (which happens when the peg gets jumped over), reduces it's alpha
        # value by 8 every frame. Once it reaches 0, kill()s it.
        if self._fading_out:
            self._alpha = max(0, self._alpha - 8)
            alpha_image = self.graphic.copy()
            alpha_image.fill((255, 255, 255, self._alpha), special_flags=pygame.BLEND_RGBA_MULT)
            self._target_surface.blit(alpha_image, self.rect)
            if self._alpha <= 0:
                self.kill()
        # If self._is_snapping_back is set to True, changes self._position by the value of self._velocity every frame.
        # self._velocity is the normalized direction vector multiplied by the value of self._speed.
        # If the peg is within the number is pixels defined in self._speed, stops moving and sets the peg's position
        # to self._destination.
        if self.is_snapping_back:
            if self._position.distance_to(self._destination) < self._speed:
                self.is_snapping_back = False
                self.rect.topleft = self._destination
            else:
                self._position += self._velocity
                self.rect.topleft = self._position
        # Draws the peg.
        if not self._fading_out:
            self.display()
