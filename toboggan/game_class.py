"""
Game module. Holds the Game class used for controlling game state.
"""

from .room_generator import RoomGenerator
from .game_components import Player, Combat

class Game:
    """
    Main Game controller class. Keeps track of game state.
    """
    def __init__(self):
        self.room_controller = None
        self.starting_room = None
        self.player = None
        self.init = 0
        self.skills = ['combat', 'speed', 'defense']
        self.skill_definitions = {
            'combat': 'Combat Skill: This will determine your attack accuracy<br><br>',
            'speed': 'Speed: This will determine how fast you can attack and how easily you can evade enemies<br><br>',
            'defense': 'Defense: This will determine how well you can block enemy attacks<br><br>'
        }
        self.stat_list = []
        self.combat = None
        self.active_combat = False

    def generate_starting_room(self, starting_room):
        self.room_controller = RoomGenerator(starting_room)
        self.starting_room = self.room_controller.starting_room