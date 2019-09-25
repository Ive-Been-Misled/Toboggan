class Game:
    def __init__(self):
        north_room = Room('North Room', 'You are in a small room. There is a sword on the ground and a goblin standing in front of you. There is an exit south of you.', (None, None, None, None), {}, {})
        self.starting_room = Room('Starting Room', 'You are in an empty room. There is an exit to the north.', (north_room, None, None, None), {}, {})
        north_room.connected_rooms['south'] = self.starting_room
        self.player = Player(self.starting_room)

        enemy = Character('Goblin', north_room)

    def generate_storyboard(self):
        pass

    def update(self, action):
        pass

    def save(self):
        pass

    def get_state(self):
        pass

class Character:
    def __init__(self, title, starting_room, hit_points=100):
        self.title = title
        self.hit_points = hit_points
        self.current_room = starting_room
        self.current_room.enter(self)
   
    def __str__(self):
        return (
            f'Name: {self.title}\n'            
            f'HP: {self.hit_points}\n'
            f'Current Location: {self.current_room.title}\n'
        )

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
        super().__init__('You', starting_room, hit_points)

class Item:
    def __init__(self):
        self.description = ''

class Room:
    def __init__(self, title, description, connected_rooms, init_characters={}, init_items={}):
        self.title = title
        self.description = description
        self.connected_rooms = { 'north': connected_rooms[0], 'south': connected_rooms[1], 'east': connected_rooms[2], 'west': connected_rooms[3] }
        self.characters = init_characters
        self.items = init_items
    
    def __str__(self):
        chars = ', '.join(self.characters.keys())
        return (
            f'{self.title} \n\n'
            f'{self.description} \n\n'
            f'The following characters are in the room: \n'
            f'{chars}'
        )

    def add_item(self, item):
        self.items.add(item)

    def remove_item(self, item):
        self.items.remove(item)

    def enter(self, character):
        self.characters[character.title] = character

    def exit(self, character):
        self.characters.pop(character.title, None)

    