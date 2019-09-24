"""Declare some top-level classes for managing all other objects."""
from .game_components import Game
from .actions import ActionMapper


class Calvin:
    """A precocious, mischievous and adventurous six-year-old boy."""

    def __init__(self):
        """Initialize all other objects needed for the game."""
        self._game = Game()
        self._ac = ActionMapper()

    def generate_response(self, input_string):
        """Return a string respresenting a response to a input string"""
        print(self._game.player.current_room.title)
        return f'You typed the magical word(s):<br><br> {input_string}'
