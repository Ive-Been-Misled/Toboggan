"""Declare some top-level classes for managing all other objects."""
from .game_class import game_controller
from .watson_action_mapper import ActionMapper
from .character_generation import char_gen
from .game_components import Combat
from .actions import Move


class Calvin:
    """A precocious, mischievous and adventurous six-year-old boy."""

    def __init__(self):
        """Initialize all other objects needed for the game."""
        self._game = game_controller
        self._ac = ActionMapper()
        self.can_move = True

    def generate_char_gen_response(self, input_string):
        if self._game.player is not None and self._game.player <= 0:
            return (
                'You died dummy!'
            )

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
                '<center>[Character Creation]</center> <br>'
                'This is character creation. Enter the following stats '
                'in order of how good you want each to be. For example '
                'if you entered \'combat defense speed\' you would be '
                'great at attacking, good at defending, and okay at running:'
                '<br><br>'
        )

        for skill in self._game.skills:
            statement = statement + self._game.skill_definitions[skill]

        if self._game.init < 4:
            return statement
        else:
            self._game.player = char_gen(self._game.stat_list, self._game.starting_room)
            return (
                'Below are your character stats. Type \'look around\' to start the game! <br><br>' +
                str(self._game.player).replace('\n', '<br>')
            )

    def generate_tutorial_response(self, input_string):
        if input_string == 'continue':
            self._game.init += 1
            return self.generate_char_gen_response(input_string)
        
        if self._game.init == 0:
            return (
                '<center>[Welcome to Toboggan]</center> <br>'
                'Toboggan is a text-based game generator. '
                'It builds a network of visitable rooms filled '
                'with friends, enemies, and items. You can pick up '
                'items to become stronger and fight enemies to '
                'level up. The game ends when you reach 0 hit points.'
                '<br><br><center>[How to play]</center><br>'
                '<r>Rooms</r>: Toboggan generates a random network of rooms, '
                'connected by keywords found in random descriptions. '
                'These keywords represent places you can move to, and '
                'are highlighted in blue<br><br>'
                '<t>Items</t>: Using different keywords found in room '
                'descriptions, Toboggan generates a list of items. '
                'Items can help make you stronger when fighting '
                'enemies or help you regain HP. They are highlighted '
                'in green<br><br>'
                '<c>Enemies</c>: Just like items and rooms, enemies are '
                'generated using a list of keywords. Be careful! When '
                'you enter a room with enemies, they may try to attack you. '
                'Enemies are highlighted in red'
                '<br><br><center>[Actions]</center><br>'
                'In Toboggan you can use the following actions to do '
                'different things. Use an action by typing it (or something) '
                'similar in the text entry below.<br><br>'
                'Perceive: Look at a room, item, or character.<br>'
                'Move: Move to a new room.<br>'
                'Introspect: Check your current stats (HP, Defense, etc.).<br>'
                'Attack: Strike at an enemy.<br>'
                'Pick Up: Put an item in a room into your inventory.<br>'
                'Drop: Remove an item from your inventory.<br>'
                'Use: Equip/Use items in your inventory.<br><br>'
                'Enter \'continue\' below to move on to character creation!'
            )

    def generate_response(self, input_string):
        """Return a string respresenting a response to a input string"""

        if self._game.init == 0:
            return self.generate_tutorial_response(input_string)

        if self._game.init < 4:
            return self.generate_char_gen_response(input_string)
        
        paragraphs = []

        action = self._ac.map(input_string)
        if action:
            # if len(self._game.player.current_room.characters) > 1 and isinstance(action, Move) and self._game.player.speed <= self._game.combat.initiative[0].speed:
            #     output = (f'You attempt to escape to another room, but alas {self._game.combat.initiative[0].title} is too fast and prevents you from escaping.'
            #               '<br><br>It seems you must face your enemies or die trying.'
            #              )
            # elif len(self._game.player.current_room.characters) > 1  and isinstance(action, Move) and self._game.player.speed > self._game.combat.initiative[0].speed:
            #     output = action.execute(self._game, self._game.player) \
            #                .replace('\n', '<br>')
            #     output += 'You manage to escape your foes in the previous room through your superior speed. <br><br>'
            #     self.combat = False
            # else:
            print(f'ACTION: {type(action).__name__}')
            output = action.execute(self._game, self._game.player) \
                           .replace('\n', '<br>')
            paragraphs.append(output)
        else:
            paragraphs.append(
                'The universe does not understand your action. '
                'Nothing happens.'
            )
        
        
        if len(self._game.player.current_room.characters) > 1 and not self._game.active_combat:
            self._game.combat = Combat(self._game.player.current_room.characters)
            paragraphs.append(self._game.combat.combat_start())
            self._game.active_combat = True
        elif self._game.active_combat:
            self._game.active_combat = self._game.combat.continue_init()
            if not self._game.active_combat:
                paragraphs.append('Combat is over and you stand victorious among your fallen foes.')
            else:
                paragraphs.append(self._game.combat.enemies_attack())
        
        return '<br><br>'.join(paragraphs)
