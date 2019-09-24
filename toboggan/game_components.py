class Game:
    def __init__(self):
        north_room = Room('North Room', 'North Room Desc', (None, None, None, None), {}, {})
        self.starting_room = Room('Starting Room', 'Starting Room Desc', (north_room, None, None, None), {}, {})
        north_room.south_room = self.starting_room
        self.player = Player(self.starting_room)

        enemy = Character('Goblin', north_room)

    def generate_storyboard(self):
        pass

    def update(self, action):
        pass

    def save():
        pass

    def get_state():
        pass

class Character:
    def __init__(self, title, starting_room, hit_points=100):
        self.title = title
        self.hit_points = hit_points
        self.current_room = starting_room
        self.current_room.enter(self)

    def move_to(self, room):
        if room != None:
            self.current_room.exit(self)
            self.current_room = room
            self.current_room.enter(self)
            return True
        else:
            return False

    def lose_hp(self, damage):
        self.hit_points = self.hit_points - damage

    def gain_hp(self, hp):
        self.hit_points = self.hit_points + hp

    def attack(self, target, damage):
        target.lose_hp(damage)

class Player(Character):
    def __init__(self, starting_room, hit_points=100):
        super().__init__('Player', starting_room, hit_points)

class Item:
    def __init__(self):
        self.description = ''

class Room:
    def __init__(self, title, description, connected_rooms, init_characters={}, init_items={}):
        self.title = title
        self.description = description
        self.north_room = connected_rooms[0]
        self.south_room = connected_rooms[1]
        self.east_room = connected_rooms[2]
        self.west_room = connected_rooms[3]
        self.characters = init_characters
        self.items = init_items
        self.description = ''

    def add_item(self, item):
        self.items.add(item)

    def remove_item(self, item):
        self.items.remove(item)

    def enter(self, character):
        self.characters[character.title] = character

    def exit(self, character):
        self.characters.pop(character.title, None)

    