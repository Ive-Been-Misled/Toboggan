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
