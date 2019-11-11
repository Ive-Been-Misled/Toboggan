"""
Components used to define the game object. Each component keeps
track of an entity in the game.
"""
from .text_generators import describe_item
from .text_generators import describe_character

class Character:
    """
    Default class used for creating game characters
    (i.e. enemies, the player, npcs).
    """

    def __init__(self, title, starting_room, combat_skill=100, defense=100, speed=100, hit_points=100):
        self.title = title
        self.combat_skill = combat_skill
        self.defense = defense
        self.speed = speed
        self.hit_points = hit_points
        self.current_room = starting_room
        self.current_room.enter(self)
        self.inventory = {}
        self.description = None

    def __str__(self):
        inv = ', '.join(self.inventory.keys())
        return (
            f'HP: {self.hit_points}\n\n'
            f'Combat Skill: {self.combat_skill}\n'
            f'Defense: {self.defense}\n'
            f'Speed: {self.speed}\n'
            f'Inventory: {inv}\n'
        )

    def generate_description(self):
        if self.description is None:
            self.description = describe_character(self.title)
        
        return self.description

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
    def __init__(self, starting_room, combat_skill=100, defense=100, speed=100, hit_points=100):
        super().__init__('You', starting_room, combat_skill, defense, speed, hit_points)

class Item:
    """
    Item class. Used to keep track of data about a specific item.
    """
    def __init__(self, title):
        self.title = title
        self.description = None

    def generate_description(self):
        if self.description is None:
            self.description = describe_item(self.title)
        
        return self.description

    def __str__(self):
        return 'This item weighs ' + str(self.weight) +' lbs.' + '\nIt is a ' + self.item_type
