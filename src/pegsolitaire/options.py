class Options:
    """Stored the game settings."""
    def __init__(self,
                 language: str = "en",
                 show_highlights: bool = True,
                 play_sounds: bool = True):
        """
        :param language: The currently selected language.
        :param show_highlights: Whether or not to highlight valid moves.
        :param play_sounds: Whether or not to play sounds.
        """
        self._language = language
        self._show_highlights = show_highlights
        self._play_sounds = play_sounds

    @property
    def lang(self) -> str:
        return self._language

    @lang.setter
    def lang(self, language: str) -> None:
        self._language = language

    @property
    def show_highlights(self) -> bool:
        return self._show_highlights

    @show_highlights.setter
    def show_highlights(self, show_highlights: bool) -> None:
        self._show_highlights = show_highlights

    @property
    def play_sounds(self) -> bool:
        return self._play_sounds

    @play_sounds.setter
    def play_sounds(self, play_sounds: bool) -> None:
        self._play_sounds = play_sounds
