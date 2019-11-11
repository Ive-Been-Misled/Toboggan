"""Declare some top-level classes for managing all other objects."""
from .game_class import game_controller
from .watson_action_mapper import ActionMapper
from .character_generation import char_gen
from .game_components import Combat


class Calvin:
    """A precocious, mischievous and adventurous six-year-old boy."""

    def __init__(self):
        """Initialize all other objects needed for the game."""
        self._game = game_controller
        self._ac = ActionMapper()
        self.combat = False

    def generate_char_gen_response(self, input_string):
        skill_scores = {}
        for skill in self._game.skills:
            idx = input_string.lower().find(skill)
            if idx != -1:
                skill_scores[skill] = idx

        if len(skill_scores) > 0:
            for i in range(len(skill_scores)):
                best_skill = min(skill_scores, key=skill_scores.get)
                del skill_scores[best_skill]
                self._game.skills.remove(best_skill)
                self._game.stat_list.append(best_skill)
                self._game.init += 1
        
        statement = (
                'This is character creation. Enter the following stats '
                'in order from best to worst:<br><br>'
        )

        for skill in self._game.skills:
            statement = statement + self._game.skill_definitions[skill]

        if self._game.init < 3:
            return statement
        else:
            self._game.player = char_gen(self._game.stat_list, self._game.starting_room)
            return (
                'Below are your character stats. Type \'look around\' to start the game! <br><br>' +
                str(self._game.player).replace('\n', '<br>')
            )

    def generate_response(self, input_string):
        """Return a string respresenting a response to a input string"""

        if self._game.init < 3:
            return self.generate_char_gen_response(input_string)
        
        paragraphs = []
        #paragraphs.append(f'You {input_string}.')

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
        if len(self._game.player.current_room.characters) > 1 and not self.combat:
            self._game.combat = Combat(self._game.player.current_room.characters)
            paragraphs.append(self._game.combat.combat_start())
            self.combat = True
        elif self.combat:
            paragraphs.append(self._game.combat.enemies_attack())

        

        return '<br><br>'.join(paragraphs)
