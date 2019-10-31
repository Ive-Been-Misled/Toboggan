"""Declare some top-level classes for managing all other objects."""
from .game_class import game_controller
from .watson_action_mapper import ActionMapper


class Calvin:
    """A precocious, mischievous and adventurous six-year-old boy."""

    def __init__(self):
        """Initialize all other objects needed for the game."""
        self._game = game_controller
        self._ac = ActionMapper()

    def generate_response(self, input_string):
        """Return a string respresenting a response to a input string"""
        paragraphs = []
        paragraphs.append(f'You {input_string}.')

        action = self._ac.map(input_string)
        if action:
            output = action.execute(self._game, self._game.player) \
                           .replace('\n', '<br>')
            paragraphs.append(output)
        else:
            paragraphs.append(
                'The universe does not understand your action. '
                'Nothing happens.'
            )

        return '<br><br>'.join(paragraphs)
