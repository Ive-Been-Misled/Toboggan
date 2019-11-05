"""
Game module. Holds the Game class used for controlling game state.
"""

from .room_generator import RoomGenerator
from .game_components import Player

class Game:
    """
    Main Game controller class. Keeps track of game state.
    """
    def __init__(self, first_room):
        self.room_controller = RoomGenerator(first_room)
        self.starting_room = self.room_controller.starting_room
        self.player = Player(self.starting_room)

    # def generate_storyboard(self):
    #     pass

    # def update(self, action):
    #     pass

    # def save(self):
    #     pass

    # def get_state(self):
    #     pass

game_controller = Game("A Lovecraftian Horror Story")
