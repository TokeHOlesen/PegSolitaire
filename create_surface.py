import pygame


def create_simple_surface(width: int,
                          height: int,
                          fill_color: str = "#B2B2B2",
                          corner_highlight_color: str = "#F5F5F5",
                          corner_shadow_color: str = "#535353",
                          highlight_color: str = "#D2D2D2",
                          shadow_color: str = "#898989") -> pygame.surface.Surface:
    """
    Helper function used to quickly create passable UI surfaces when more elaborate graphics are not available.
    Creates a pygame surface in the shape of a simple 3D button.
    Can be used for buttons, switches, windows etc.
    """
    btn_x = width
    btn_y = height
    gfx_button = pygame.Surface((btn_x, btn_y))
    gfx_button.fill(fill_color)
    gfx_button.set_at((0, 0), corner_highlight_color)
    gfx_button.set_at((btn_x - 1, btn_y - 1), corner_shadow_color)
    pygame.draw.line(gfx_button, highlight_color, (1, 0), (btn_x - 2, 0))
    pygame.draw.line(gfx_button, highlight_color, (0, 1), (0, btn_y - 2))
    pygame.draw.line(gfx_button, shadow_color, (1, btn_y - 1), (btn_x - 2, btn_y - 1))
    pygame.draw.line(gfx_button, shadow_color, (btn_x - 1, 1), (btn_x - 1, btn_y - 2))
    return gfx_button
