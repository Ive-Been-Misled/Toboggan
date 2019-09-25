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
        paragraphs = []
        paragraphs.append('You typed the magical word(s):')
        paragraphs.append(input_string)

        action = self._ac.map(input_string)
        if action:
            paragraphs.append(f'The mapped action was {action}.')
        else:
            paragraphs.append('The input was not understood.')

        return '<br><br>'.join(paragraphs)
