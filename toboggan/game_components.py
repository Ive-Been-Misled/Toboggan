"""
Components used to define the game object. Each component keeps
track of an entity in the game.
"""

class Character:
    """
    Default class used for creating game characters
    (i.e. enemies, the player, npcs).
    """

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

    def move_to(self, room: object) -> bool:
        """
        Moves a character from their current room into a given room.

        Args:
            room: The room the character is moving to

        Returns:
            True if the character successfully moved, false otherwise
        """
        if room is not None:
            self.current_room.exit(self)
            self.current_room = room
            self.current_room.enter(self)
            return True
        return False

    def lose_hp(self, damage: int) -> None:
        """
        Lowers the character's hit points by a given amount.

        Args:
            damage: Amount of hit points the character loses

        Returns:
            None
        """
        self.hit_points = self.hit_points - damage

    def gain_hp(self, hit_points: int) -> None:
        """
        Raises the character's hit points by a given amount.

        Args:
            hit_points: Amount of hit points the character gains

        Returns:
            None
        """
        self.hit_points = self.hit_points + hit_points

    def attack(self, target: object, damage: int) -> None:
        """
        Inflicts damage on another given character.

        Args:
            target: The character being attacked
            damage: The amount of damage to inflict upon the target

        Returns:
            None
        """
        target.lose_hp(damage)

class Player(Character):
    """
    Character class specific to the player. Inherits Character.
    """
    def __init__(self, starting_room, hit_points=100):
        super().__init__('You', starting_room, hit_points)

class Item:
    """
    Item class. Used to keep track of data about a specific item.
    """
    def __init__(self, title, description, weight, item_type):
        self.title = title
        self.description = description
        self.weight = weight
        self.item_type = item_type

    def __str__(self):
        return 'This item weighs ' + str(self.weight) +' lbs.' + '\nIt is a ' + self.item_type
