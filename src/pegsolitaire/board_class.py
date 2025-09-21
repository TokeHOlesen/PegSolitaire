import pygame.surface
from .board_tiles_class import *


class Board:
    """Represents the Peg Solitaire board and runs the actual game logic."""
    def __init__(self,
                 layout: dict,
                 board_surface: pygame.surface.Surface,
                 target_surface: pygame.surface.Surface,
                 board_pos: tuple[int, int],
                 res_multi: int,
                 smooth_tile_gfx: pygame.surface.Surface,
                 hole_tile_gfx: pygame.surface.Surface,
                 peg_gfx: pygame.surface.Surface,
                 highlight_gfx: pygame.surface.Surface,
                 highlight_full_gfx: pygame.surface.Surface,
                 board_size: int = 9,
                 peg_move_snd: pygame.mixer.Sound = None,
                 snap_back_snd: pygame.mixer.Sound = None,
                 victory_snd: pygame.mixer.Sound = None,
                 defeat_snd: pygame.mixer.Sound = None,
                 options=None):
        """
        :param layout: Board layout to use (a dictionary).
        :param board_surface: The surface the board elements will be drawn on.
        :param target_surface: The surface board_surface will be drawn on.
        :param board_size: The length of the side of the board, in tiles.
        :param board_pos: Where to draw the board_surface on target_surface.
        :param res_multi: Resolution multiplier, needed for correcting mouse cursor position values.
        :param smooth_tile_gfx: Smooth board tile graphics.
        :param hole_tile_gfx: Holed board tile graphics.
        :param peg_gfx: Peg graphics.
        :param highlight_gfx: Highlight graphics (overlaid on tiles that thr lifted peg can be moved to).
        :param highlight_full_gfx: Full highlight (shown when a peg is lifted over a valid sestination).
        :param peg_move_snd: Sound to play when a peg moves to a new valid position.
        :param victory_snd: Sound to play when the player is victorious.
        :param defeat_snd: Sound to play when there are no more valid moves.
        :param options: Options object holding game settings; optional.
        """
        self._surface = board_surface
        self.target_surface = target_surface
        self._tile_grid = layout["layout"]
        self._start_hole = layout["start"]
        self._board_size = board_size
        self.board_pos = board_pos
        self._res_multiplier = res_multi
        self._smooth_gfx = smooth_tile_gfx
        self._hole_gfx = hole_tile_gfx
        self._peg_gfx = peg_gfx
        self._highlight_gfx = highlight_gfx
        self._highlight_full_gfx = highlight_full_gfx
        self._peg_move_snd = peg_move_snd
        self._snap_back_snd = snap_back_snd
        self._victory_snd = victory_snd
        self._defeat_snd = defeat_snd
        self._grid_tiles = pygame.sprite.Group()
        self._static_pegs = pygame.sprite.Group()
        self._highlights = pygame.sprite.Group()
        self._fading_out_pegs = pygame.sprite.Group()
        self._dragged_peg = pygame.sprite.GroupSingle()
        self.undo_stack = []
        self.move_count = 0
        self._game_is_lost = False
        self._game_is_won = False
        self._options = options
        # Assigns graphics to the board tiles according to their type and adds them to self.grid_tiles sprite group.
        self._reset_tiles()
        self.reset_pegs()

    def _add_peg(self, coords: tuple[int, int], group: pygame.sprite.Group) -> None:
        """Adds an Peg object with the given grid coords to the given sprite group."""
        group.add(Peg(self._surface, coords, self._board_size, self.board_pos, self._res_multiplier, self._peg_gfx))

    def _reset_tiles(self) -> None:
        """Creates the game board according to the loaded layout."""
        self._grid_tiles.empty()
        for x in range(self._board_size):
            for y in range(self._board_size):
                if self._tile_grid[x][y] == 0:
                    self._grid_tiles.add(Tile(self._surface, (x, y), self._smooth_gfx))
                else:
                    self._grid_tiles.add(Tile(self._surface, (x, y), self._hole_gfx))

    def reset_pegs(self) -> None:
        """Resets all pegs to their starting positions and repopulates the self.static_pegs sprite group"""
        self._static_pegs.empty()
        self._dragged_peg.empty()
        for x in range(self._board_size):
            for y in range(self._board_size):
                if self._tile_grid[x][y] and (x, y) != self._start_hole:
                    self._add_peg((x, y), self._static_pegs)
        self.undo_stack.clear()
        self.move_count = 0
        self._game_is_won = self._game_is_lost = False

    def load_layout(self, layout: dict) -> None:
        """Loads a new layout and resets the board and all pegs."""
        self._tile_grid = layout["layout"]
        self._start_hole = layout["start"]
        self._reset_tiles()
        self.reset_pegs()

    def _tile_is_hole(self, grid_coords: tuple[int, int]) -> bool:
        """Returns true if the tile at the given coordinates is a hole"""
        pos_x, pos_y = grid_coords
        if self._tile_grid[pos_x][pos_y] == 1:
            return True
        return False

    def _tile_is_occupied(self, grid_coords: tuple[int, int]) -> bool:
        """Returns True if there is a peg at the given coordinates"""
        for peg in self._static_pegs:
            if peg.grid_coords == grid_coords:
                return True
        return False

    @staticmethod
    def _get_potential_destinations(this_peg: Peg) -> tuple:
        """Returns a tuple containing the coords of the tiles 2 tiles away from the Peg (horizontaly and vertically)"""
        start_pos_x, start_pos_y = this_peg.old_grid_coords
        return ((start_pos_x - 2, start_pos_y), (start_pos_x + 2, start_pos_y),
                (start_pos_x, start_pos_y - 2), (start_pos_x, start_pos_y + 2))

    def _highlight_valid_destinations(self, this_peg: Peg) -> None:
        """Highlights the tiles that the peg can be moved to."""
        if self._options is not None and self._options.show_highlights:
            potential_destinations = self._get_potential_destinations(this_peg)
            for destination in potential_destinations:
                if self._potential_move_is_legal(this_peg, destination):
                    self._highlights.add(Tile(self._surface, destination, self._highlight_gfx))

    def check_highlight_hover(self) -> None:
        """Checks if a peg is hovering above a highlighted tile. If yes, highlights it fully."""
        if self._dragged_peg:
            for highlight in self._highlights:
                if highlight.coords == self._dragged_peg.sprite.grid_coords:
                    highlight.graphic = self._highlight_full_gfx
                else:
                    highlight.graphic = self._highlight_gfx

    @staticmethod
    def _destination_is_valid(this_peg: Peg) -> bool:
        """Returns True if the destination is two tiles horizontally or vertically from the starting position"""
        new_peg_x, new_peg_y = this_peg.grid_coords
        old_peg_x, old_peg_y = this_peg.old_grid_coords
        if (new_peg_x == old_peg_x + 2
                or new_peg_x == old_peg_x - 2
                or new_peg_y == old_peg_y + 2
                or new_peg_y == old_peg_y - 2):
            return True
        return False

    def _is_jumping_over(self, this_peg: Peg, new_coords=None) -> bool:
        """Returns True if the peg is jumping over another peg to reach its new position"""
        new_peg_x, new_peg_y = new_coords if new_coords is not None else this_peg.grid_coords
        old_peg_x, old_peg_y = this_peg.old_grid_coords
        if new_peg_x == old_peg_x:
            if new_peg_y > old_peg_y and self._tile_is_occupied((new_peg_x, old_peg_y + 1)):
                return True
            elif new_peg_y < old_peg_y and self._tile_is_occupied((new_peg_x, old_peg_y - 1)):
                return True
        elif new_peg_y == old_peg_y:
            if new_peg_x > old_peg_x and self._tile_is_occupied((old_peg_x + 1, new_peg_y)):
                return True
            elif new_peg_x < old_peg_x and self._tile_is_occupied((old_peg_x - 1, new_peg_y)):
                return True
        return False

    def _move_is_legal(self, this_peg: Peg) -> bool:
        """
        Returns True if moving the peg to a new position satisfies all game rule requirements.
        The target tile must be a hole, be empty, be two tiles away horizontally or vertically from the starting
        position and the tile between the starting position and the target position must be occupied.
        """
        if (self._tile_is_hole(this_peg.grid_coords)
                and not self._tile_is_occupied(this_peg.grid_coords)
                and self._destination_is_valid(this_peg)
                and self._is_jumping_over(this_peg)):
            return True
        return False

    def _potential_move_is_legal(self, this_peg: Peg, destination: tuple[int, int]) -> bool:
        """Returns True if Peg can potentially be moved to the given destination."""
        pot_x, pot_y = destination
        if self._board_size > pot_x >= 0 and self._board_size > pot_y >= 0:
            if (self._tile_is_hole(destination)
                    and not self._tile_is_occupied(destination)
                    and self._is_jumping_over(this_peg, destination)):
                return True
        return False

    def _remove_peg(self, remove_xy: tuple[int, int]) -> None:
        """Moves a peg from _static_pegs to _fading_out_pegs. It will kill() itself when its alpha reaches 0."""
        for checked_peg in self._static_pegs:
            if checked_peg.grid_coords == remove_xy:
                # The removed peg is set to start fading out, and is moved to a group containing only fading out pegs.
                # Once it fades out completely, it will be removed.
                checked_peg.fade_out()
                self._static_pegs.remove(checked_peg)
                self._fading_out_pegs.add(checked_peg)

    @staticmethod
    def _get_jumped_peg_coords(this_peg: Peg) -> tuple[int, int]:
        """After jumping over a peg, identifies the peg to be removed and removes it"""
        new_peg_x, new_peg_y = this_peg.grid_coords
        old_peg_x, old_peg_y = this_peg.old_grid_coords
        remove_x = (new_peg_x + old_peg_x) // 2
        remove_y = (new_peg_y + old_peg_y) // 2
        return remove_x, remove_y

    def undo(self) -> None:
        """Resets the board to the state before the last move. Resets defeat/victory state."""
        if self.undo_stack:
            last_move = self.undo_stack.pop()
            self._remove_peg(last_move["new_pos"])
            self._add_peg(last_move["old_pos"], self._static_pegs)
            self._add_peg(last_move["jumped_peg_pos"], self._static_pegs)
            self._check_for_victory_and_defeat()
            self.move_count -= 1
            self._game_is_lost = False
            self._game_is_won = False

    def _check_for_victory(self) -> bool:
        """Returns True if the game is won."""
        if len(self._static_pegs.sprites()) + int(bool(self._dragged_peg)) == 1:
            if not self.is_victorious:
                self._play_sound(self._victory_snd)
            return True
        return False

    def _check_for_defeat(self) -> bool:
        """Returns True if there are no more valid moves, and the game is lost."""
        all_pegs = [peg for peg in self._static_pegs]
        if self._dragged_peg:
            all_pegs.append(self._dragged_peg.sprite)
        if len(all_pegs) == 1:
            return False
        for peg in all_pegs:
            potential_destinations = self._get_potential_destinations(peg)
            for destination in potential_destinations:
                if self._potential_move_is_legal(peg, destination):
                    return False
        if not self.is_defeated:
            self._play_sound(self._defeat_snd)
        return True

    def _check_for_victory_and_defeat(self) -> None:
        """Unless the result is already known, checks if the game has been won or lost."""
        if not self.is_victorious:
            self._game_is_won = self._check_for_victory()
        if not self.is_defeated:
            self._game_is_lost = self._check_for_defeat()

    @property
    def is_victorious(self) -> bool:
        """Returns True if the game is won."""
        return self._game_is_won

    @property
    def is_defeated(self) -> bool:
        """Returns True if the game is lost."""
        return self._game_is_lost

    def _play_sound(self, sound: pygame.mixer.Sound) -> None:
        """Plays a sound, unless an options object is present and sound is turned off."""
        if (self._options is not None and self._options.play_sounds) or self._options is None:
            sound.play()

    def process_input(self, events: pygame.event) -> None:
        """Runs the actual game logic."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Divides the mouse coords by the resolution multiplier to get actual mouse position in terms of display
                mouse_coords = tuple((coord // self._res_multiplier for coord in pygame.mouse.get_pos()))
                for peg in self._static_pegs:
                    if peg.is_mouseover(mouse_coords):
                        # When a peg gets lifted, sets its status to dragged and updates its mouse offset.
                        peg.is_being_dragged = True
                        peg.mouse_offset = mouse_coords
                        # Changes the peg's group
                        self._dragged_peg.add(peg)
                        self._static_pegs.remove(peg)
                        # If set in settings, highlights possible destinations for this peg.
                        self._highlight_valid_destinations(peg)

            if event.type == pygame.MOUSEBUTTONUP:
                for peg in self._dragged_peg:
                    if peg.is_being_dragged:
                        # When the user lets go of the mouse button, updates the peg's status
                        peg.is_being_dragged = False
                        if self._move_is_legal(peg):
                            # Gets the coordinates of the peg between the dragged peg's old and new location.
                            jumped_peg_coords = self._get_jumped_peg_coords(peg)
                            # Adds the move info to the undo stack
                            self.undo_stack.append(
                                {"new_pos": peg.grid_coords,
                                 "old_pos": peg.old_grid_coords,
                                 "jumped_peg_pos": jumped_peg_coords}
                            )
                            # Moves the peg and removes the peg that was jumped over.
                            self._remove_peg(jumped_peg_coords)
                            peg.move_to_new_pos()
                            self._play_sound(self._peg_move_snd)
                            self.move_count += 1
                        else:
                            # If the peg's position when dropped is not a valid destination, puts it back.
                            if peg.grid_coords != peg.old_grid_coords:
                                self._play_sound(self._snap_back_snd)
                            peg.snap_back()
                        # Updates sprite groups and checks victory conditions.
                        self._dragged_peg.remove(peg)
                        self._static_pegs.add(peg)
                        self._highlights.empty()
                        self._check_for_victory_and_defeat()

    def draw_board(self) -> None:
        """Updates all the sprite groups and blits them onto the board surface"""
        # Draws board tiles.
        self._grid_tiles.update()
        # If a peg is hovering above a highlighted tile, highlights it fully.
        self.check_highlight_hover()
        # Draws highlights.
        self._highlights.update()
        # Draws pegs on the board.
        self._static_pegs.update()
        # Draws pegs that are fading out.
        self._fading_out_pegs.update()
        # Draws the peg that is being dragged by the player (if any).
        self._dragged_peg.update()
        # Draws everything on the target surface.
        self.target_surface.blit(self._surface, self.board_pos)
