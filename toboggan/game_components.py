"""
Components used to define the game object. Each component keeps
track of an entity in the game.
"""
import random
import copy
from .text_generators import describe_item
from .text_generators import describe_character

DEFAULT_WEAPON = 'Unarmed'
DEFAULT_ARMOR = 'Empty'

class Character:
    """
    Default class used for creating game characters
    (i.e. enemies, the player, npcs).
    """

    def __init__(self, title, starting_room, combat_skill=100, defense=100, speed=100, hit_points=100, level=1):
        self.title = title
        self.base_combat_skill = combat_skill
        self.combat_skill = combat_skill
        self.base_defense = defense
        self.defense = defense
        self.speed = speed
        self.hit_points = hit_points
        self.level = level
        self.current_room = starting_room
        self.current_room.enter(self)
        self.inventory = {}
        self.description = None
        self.equipped_weapon = WeaponItem(DEFAULT_WEAPON, 3, 0)
        self.equipped_armor = ArmorItem(DEFAULT_ARMOR, 0)
        self.xp = 0
        self.next_level = self.level*5

    def __str__(self):
        inv = ', '.join(self.inventory.keys())
        return (
            f'<center>[{self.title}]</center>\n'
            f'HP: {self.hit_points}\n\n'
            f'Level: {self.level}\n'
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
        if self.equipped_weapon.title != DEFAULT_WEAPON:
            self.inventory[self.equipped_weapon.title] = copy.deepcopy(self.equipped_weapon)

        self.equipped_weapon = weapon
        self.combat_skill = self.base_combat_skill + self.equipped_weapon.combat_skill

    def equip_armor(self, armor: object) -> None:
        if self.equipped_armor.title != DEFAULT_ARMOR:
            self.inventory[self.equipped_armor.title] = copy.deepcopy(self.equipped_armor)

        self.equipped_armor = armor
        self.defense = self.base_defense + self.equipped_armor.armor

    def attack(self, target: object) -> str:
        """
        Inflicts damage on another given character.

        Args:
            target: The character being attacked
            damage: The amount of damage to inflict upon the target

        Returns:
            None
        """
        attack_str = ''
        if random.randint(1, 20)+self.combat_skill < 10 + target.defense:
            return f'Drat the attack missed'
        if self.equipped_weapon.title == DEFAULT_WEAPON and isinstance(self, Player):
            target.lose_hp(3)
            attack_str = f'{self.title} struck {target.title} while unarmed and dealt 3 damage.'
        else:
            target.lose_hp(self.equipped_weapon.damage)
            attack_str = f'{self.title.capitalize()} struck {target.title} with {self.equipped_weapon.title} dealing {self.equipped_weapon.damage} damage.'
        if target.hit_points <= 0:
            self.xp+=1
        if self.xp >= self.next_level:
            self.level += 1
            self.next_level = self.level*5
            up = [random.randint(1, int(self.level * (1 + random.random()))) for x in range(3)]
            up_text = [f'Combat Skill: {self.combat_skill} + {up[0]} = {self.combat_skill + up[0]}',
                       f'Defense: {self.defense} + {up[1]} = {self.defense + up[1]}',
                       f'Speed: {self.speed} + {up[2]} = {self.speed + up[2]}']
            self.base_combat_skill += up[0]
            self.combat_skill += up[0]
            self.base_defense += up[1]
            self.defense += up[1]
            self.speed += up[2]
            attack_str += '<br><br> You levelled up your stats increased: <br> - ' + '<br> - '.join(up_text)
        return attack_str

class Player(Character):
    """
    Character class specific to the player. Inherits Character.
    """
    def __init__(self, starting_room, combat_skill=100, defense=100, speed=100, hit_points=100, level=1):
        super().__init__('You', starting_room, combat_skill, defense, speed, hit_points, level)

class Enemy(Character):
    """
    Enemy class specific to enemies. Inherits Character.
    """
    def __init__(self, title, starting_room, combat_skill, defense, speed, hit_points, level):
        super().__init__(title, starting_room, combat_skill, defense, speed, hit_points, level)
        self.equipped_weapon = WeaponItem(f'{self.title} strike', random.randint(1+level, 3*level), 0)

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
            f'Food Item\n'
            f'Effect: HP +{self.hp}'
        )

class WeaponItem(Item):
    def __init__(self, title, damage=0, combat_skill=0):
        self.damage = damage
        self.combat_skill = combat_skill
        super().__init__(title)

    def __str__(self):
        return (
            f'<center>[{self.title.capitalize()}]</center>\n'
            f'Weapon\n'
            f'Effect: Combat Skill +{self.combat_skill}\n'
            f'Effect: Damage {self.damage}\n\n'
        )

class ArmorItem(Item):
    def __init__(self, title, armor=10):
        self.armor = armor
        super().__init__(title)

    def __str__(self):
        return (
            f'<center>[{self.title.capitalize()}]</center>\n'
            f'Armor Item\n'
            f'Effect: Defense +{self.armor}\n\n'
        )

class Combat:
    def __init__(self, participants):
        self.participants = copy.copy(participants)
        self.participants.pop('You')
        self.player = participants['You']
        self.initiative = list(self.participants.values())
        self.turn = None
           
    def combat_start(self):
        
        init_print = [char.title for char in self.initiative]
        combat_str = ('COMBAT BEGINS:<br>'
                      'You find yourself staring down: <br> - '+ '<br> - '.join(init_print) +
                      '<br>They appear hostile and intent to attack you.'
                     )
        self.initiative.sort(key=lambda x: x.speed, reverse=True)
        self.turn = self.initiative[0]
        return combat_str

    def continue_init(self):
        [self.initiative.remove(char) for char in self.initiative if char.title not in self.player.current_room.characters.keys()]
        if self.initiative:
            current_turn = self.initiative.pop(0)
            self.initiative.append(current_turn)
            self.turn = self.initiative[0]
        
        return len(self.initiative) > 0

    def enemies_attack(self):
        combat_str = f'{self.turn.title} attacks you. <br><br>' + self.turn.attack(self.player)
        return combat_str
