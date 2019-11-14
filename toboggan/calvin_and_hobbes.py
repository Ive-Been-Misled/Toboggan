"""Declare some top-level classes for managing all other objects."""
from .game_class import Game
from .watson_action_mapper import ActionMapper
from .character_generation import char_gen
from .game_components import Combat
from .setting import setting_instance
from .actions import Move

class Calvin:
    """A precocious, mischievous and adventurous six-year-old boy."""

    def __init__(self):
        """Initialize all other objects needed for the game."""
        self._game = Game()
        self._ac = ActionMapper()
        self.can_move = True

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
                '<center>[Character Creation]</center> <br>'
                'This is character creation. Enter the following stats '
                'in order of how good you want each to be. For example '
                'if you entered \'combat defense speed\' you would be '
                'great at attacking, good at defending, and okay at running:'
                '<br><br>'
        )

        for skill in self._game.skills:
            statement = statement + self._game.skill_definitions[skill]

        if self._game.init < 6:
            return statement
        else:
            self._game.player = char_gen(self._game.stat_list, self._game.starting_room)
            return (
                'Below are your character stats. Type \'look around\' to start the game! <br><br>' +
                str(self._game.player).replace('\n', '<br>')
            )

    def generate_tutorial_response(self, input_string):
        if input_string == 'continue':
            return self.generate_user_variables_response(input_string)
        
        if self._game.init == 0:
            return (
                '<center>[Welcome to Toboggan]</center> <br>'
                'Toboggan is a text-based game generator. '
                'It builds a network of visitable rooms filled '
                'with enemies, items, and other rooms. You can pick up '
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
                'different things. Use an action by typing it or something '
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

    def generate_user_variables_response(self, input_string):
        self._game.init += 1
        if self._game.init == 1:
            return (
                '<center>[Adventure Setting]</center><br>'
                'To start playing Toboggan, you first need to enter a setting. '
                'The setting you enter will generally control what your random '
                'adventure will be about.<br><br>Can\'t think of anything? Try:<br>'
                ' - Middle-Earth<br> - A Lovecraftian horror story<br> - Cyberpunk'
            )
        
        if self._game.init == 2:
            return (
                '<center>[First Room]</center><br>'
                'Now that you\'ve entered a setting, enter the room you would like '
                'to start in. This doesn\'t have to be a traditional room per se. Here '
                'are some examples of interesting starting room ideas:<br>'
                '- A large cavern<br>'
                '- An old, haunted house<br>'
                '- A space ship<br>'
                '- The top floor of a skyscrapper'
            )

    def generate_response(self, input_string):
        """Return a string respresenting a response to a input string"""
        if self._game.player is not None and input_string == 'kill self':
            self._game.player.hit_points = 0

        if self._game.player is not None and self._game.player.hit_points <= 0:
            if input_string == 'start over':
                self._game = Game()
                return self.generate_tutorial_response(input_string)

            return (
                '<center>[Game Over]</center><br>'
                'Thanks for playing! Here\'s your game stats:<br><br>'
                f'Number of enemies killed: {self._game.player.xp}<br>'
                f'Number of rooms explored: {len(self._game.room_controller.room_list)}<br>'
                f'Your final stats: {self._game.player}<br>'
                f'Type \'start over\' to play again!'
            ).replace('\n', '<br>')

        if self._game.init == 0:
            return self.generate_tutorial_response(input_string)

        if self._game.init == 1:
            setting_instance.universe_setting = input_string
            return self.generate_user_variables_response(input_string)

        if self._game.init == 2:
            self._game.init += 1
            self._game.generate_starting_room(input_string)
            return self.generate_char_gen_response(input_string)

        if self._game.init < 6:
            return self.generate_char_gen_response(input_string)

        if self._game.init == 6:
            if input_string != 'look around':
                return self.generate_char_gen_response(input_string)
            else:
                self._game.init += 1

        paragraphs = []

        action = self._ac.map(input_string)
        if action:
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
