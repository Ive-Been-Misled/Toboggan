"""
Components used to define the game object. Each component keeps
track of an entity in the game.
"""
from .text_generators import describe_item
from .text_generators import describe_character
import copy
class Character:
    """
    Default class used for creating game characters
    (i.e. enemies, the player, npcs).
    """

    def __init__(self, title, starting_room, combat_skill=100, defense=100, speed=100, hit_points=100):
        self.title = title
        self.base_combat_skill = combat_skill
        self.combat_skill = combat_skill
        self.base_defense = defense
        self.defense = defense
        self.speed = speed
        self.hit_points = hit_points
        self.current_room = starting_room
        self.current_room.enter(self)
        self.inventory = {}
        self.description = None
        self.equipped_weapon = WeaponItem('Empty', 0, 0)
        self.equipped_armor = ArmorItem('Empty', 0, 0)

    def __str__(self):
        inv = ', '.join(self.inventory.keys())
        return (
            f'<center>[{self.title}]</center>\n'
            f'HP: {self.hit_points}\n\n'
            f'Combat Skill: {self.combat_skill}\n'
            f'Defense: {self.defense}\n'
            f'Speed: {self.speed}\n\n'
            f'Equipped Weapon: {self.equipped_weapon.title}\n'
            f'Equipped Armor: {self.equipped_armor.title}\n\n'
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

    def equip_weapon(self, weapon: object) -> None:
        if self.equipped_weapon.title != 'Empty':
            self.inventory[self.equipped_weapon.title] = copy.deepcopy(self.equipped_weapon)

        self.equipped_weapon = weapon
        self.combat_skill = self.base_combat_skill + self.equipped_weapon.combat_skill

    def equip_armor(self, armor: object) -> None:
        if self.equipped_armor.title != 'Empty':
            self.inventory[self.equipped_armor.title] = copy.deepcopy(self.equipped_armor)

        self.equipped_armor = armor
        self.defense = self.base_defense + self.equipped_armor.armor

    def attack(self, target: object, weapon: object) -> str:
        """
        Inflicts damage on another given character.

        Args:
            target: The character being attacked
            damage: The amount of damage to inflict upon the target

        Returns:
            None
        """
        target.lose_hp(weapon.damage)
        return ''

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

class FoodItem(Item):

    def __init__(self, title, hp=10):
        self.hp = hp
        super().__init__(title)

    def __str__(self):
        return (
            f'<center>[{self.title.capitalize()}]</center>\n'
            f'Effect: HP +{self.hp}\n'
        )

class WeaponItem(Item):
    def __init__(self, title, damage=0, combat_skill=0):
        self.damage = damage
        super().__init__(title)

    def __str__(self):
        return (
            f'<center>[{self.title.capitalize()}]</center>\n'
            f'Effect: Combat Skill +{self.combat_skill}\n'
            f'Effect: Damage {self.damage}\n'
        )

class ArmorItem(Item):
    def __init__(self, title, armor=10):
        self.armor = armor
        super().__init__(title)

    def __str__(self):
        return (
            f'<center>[{self.title.capitalize()}]</center>\n'
            f'Effect: Defense +{self.armor}\n'
        )

class Combat:
    def __init__(self, participants: list):
        self.participants = participants
        self.initiative = list(self.participants.values())
        self.turn = 0
    
    def combat_start(self):
        init_print = [char.title for char in self.initiative]
        init_print.remove('You')
        combat_str = ('COMBAT BEGINS:<br>'
                      'You find yourself staring down '+ ', '.join(init_print) +
                      '<br>They appear hostile and intent to attack you.'
                     )
        self.initiative.sort(key=lambda x: x.speed, reverse=True)
        return combat_str
    
    def enemies_attack(self):
        combat_str = ''
        if self.initiative[self.turn].title is 'You':
            combat_str = 'You have a chance to act against the enemies.  What will you do?'
        else:
            combat_str = f'{self.initiative[self.turn].title} attacks you dealing alotta damage.'
        self.turn += 1
        self.turn %= len(self.initiative)
        return combat_str
        
