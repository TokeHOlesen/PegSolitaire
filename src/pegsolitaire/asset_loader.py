import pygame
from importlib import resources
from io import BytesIO

PACKAGE_NAME = "pegsolitaire"


def read_asset_bytes(path: str) -> bytes:
    """Returns the bytes of the given resource in assets/"""
    return resources.files(PACKAGE_NAME).joinpath("assets", path).read_bytes()


def load_image(path: str, convert=True, convert_alpha=False) -> pygame.Surface:
    """Returns a pygame surface created from the image at the given relative path (in assets/)."""
    data = read_asset_bytes(path)
    surface = pygame.image.load(BytesIO(data))
    if convert_alpha:
        return surface.convert_alpha()
    return surface.convert() if convert else surface


def load_sound(path:str) -> pygame.mixer.Sound:
    """Returns a pygame sound object created from the sound file at the given relative path (in assets/)."""
    data = read_asset_bytes(path)
    return pygame.mixer.Sound(file=BytesIO(data))


def load_font(path: str, size: int) -> pygame.font.Font:
    """Returns a pygame Font object created from the font file at the given relative path (in assets/)."""
    data = read_asset_bytes(path)
    return pygame.font.Font(BytesIO(data), size)
