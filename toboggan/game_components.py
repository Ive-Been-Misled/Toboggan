from .room_generator import RoomGenerator

class Game:
    def __init__(self):
        
        # apple = Item('Apple', 'A tasty red fruit', 0.1, 'food item')
        # sword = Item('Sword', 'A sharp metal pointy thing.', 10, 'sword')
        # north_room = RoomGenerator.Room('North Room', 'You are in a small room. There is a sword on the ground and a goblin standing in front of you. There is an exit south of you.', (None, None, None, None), {}, {sword.title: sword})
        # south_room = RoomGenerator.Room('Fields', 'You are in a field. There is an apple tree. It looks like one of the apples has fallen on the ground. There is an open door north of you and a forest to the west.', (None, None, None, None), {}, {apple.title: apple})
        # south_west_room = RoomGenerator.Room('Forest', 'You are in a forest. There is a goblin guarding a cave entrance to the west. There is a clearing to the east.', (None, None, None, None), {}, {} )
        # cave_room = RoomGenerator.Room('Cave', 'Inside the cave, you find a chest filled with gold.\n\nYou Win!', (None, None, None, None), {}, {})
        # self.starting_room = RoomGenerator.Room('Starting Room', 'You are in an empty room. There are exits to the north and south.', (north_room, south_room, None, None), {}, {})
        # north_room.connected_rooms['south'] = self.starting_room
        # south_room.connected_rooms['north'] = self.starting_room
        # south_room.connected_rooms['west'] = south_west_room
        # south_west_room.connected_rooms['east'] = south_room
        # south_west_room.connected_rooms['west'] = cave_room
        # cave_room.connected_rooms['east'] = south_west_room

        # Character('Goblin', north_room, hit_points=60)
        # Character('Goblin', south_west_room, hit_points=60)

        self.starting_room = RoomGenerator("Starting Room").starting_room
        self.player = Player(self.starting_room)

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
        self.inventory = {}
   
    def __str__(self):
        inv = ', '.join(self.inventory.keys())
        return (
            f'Name: {self.title}\n'            
            f'HP: {self.hit_points}\n'
            f'Current Location: {self.current_room.title}\n'
            f'Inventory: {inv}\n'
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
    def __init__(self, title, description, weight, itemType):
        self.title = title
        self.description = description
        self.weight = weight
        self.itemType = itemType
    def __str__(self):
        return ('This item weighs ' + str(self.weight) +' lbs.' + '\nIt is a ' + self.itemType)
