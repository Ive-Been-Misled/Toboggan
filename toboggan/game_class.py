from .room_generator import RoomGenerator
from .game_components import Character, Player, Item

class Game:
    def __init__(self):
        first_room = "A Lovecraftian Horror Story"

        self.starting_room = RoomGenerator(first_room).starting_room
        self.player = Player(self.starting_room)

    def generate_storyboard(self):
        pass

    def update(self, action):
        pass

    def save(self):
        pass

    def get_state(self):
        pass