"""
Game module. Holds the Game class used for controlling game state.
"""

from .room_generator import RoomGenerator
from .game_components import Player, Combat

class Game:
    """
    Main Game controller class. Keeps track of game state.
    """
    def __init__(self, first_room):
        self.room_controller = RoomGenerator(first_room)
        self.starting_room = self.room_controller.starting_room
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

    # def generate_storyboard(self):
    #     pass

    # def update(self, action):
    #     pass

    # def save(self):
    #     pass

    # def get_state(self):
    #     pass

game_controller = Game("A Lovecraftian Horror Story")
