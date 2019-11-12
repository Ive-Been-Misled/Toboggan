"""
Room generation and room data storage.
"""
from .text_generators import describe_location
from .text_generators import room_noun_generator
from .text_generators import tokenize
from .game_components import Character, Enemy, FoodItem, WeaponItem, ArmorItem
from .noun_key import NounKey
from .character_generation import enemy_gen
import re
import random

def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(re.escape(sub), string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

class RoomGenerator:
    """
    Generates rooms and room connections.
    """
    def __init__(self, starting_room_title):
        starting_room_desc = describe_location(starting_room_title)
        self.starting_room = RoomGenerator.Room(self, starting_room_title, starting_room_desc)
        self.starting_room.description_tokens = tokenize(self.starting_room.description)
        self.room_list = []
        self.room_list.append(self.starting_room)
        self.level = 1

    def generate_connected_rooms(self, current_room: object, connected_room_titles: []) -> None:
        """
        Given a room and a list of titles, generate rooms that connect
        to that room.

        Args:
            current_room: The room to generate connections to.
            connected_room_titles: The titles of the rooms that will be 
                                   connected to current_room
        
        Returns:
            None

        """
        current_room.description_tokens = tokenize(current_room.description)
        for title in connected_room_titles:
            connected_room = RoomGenerator.Room(self, title, None)
            current_room.connected_rooms[title] = connected_room
            connected_room.connected_rooms["back"] = current_room
            self.room_list.append(connected_room)
    
    class Room:
        """
            Room data object. Stores information about a given room
            and has useful classes for object manipulation
        """
        def __init__(self, room_generator, title, description):
            self.room_generator = room_generator
            self.title = title
            self.formatted_desc = description
            self.description = description
            self.description_tokens = None
            self.connected_rooms = {}
            self.perceived_rooms = []
            self.characters = {}
            self.item_list = {}
            self.original_items = set()
            self.additional_items = set()
            self.entered = False
        
        def __str__(self):
            #chars = ', '.join(self.characters.keys())
            #items = ', '.join(self.item_list.keys())
            addnl = ''
            if len(self.additional_items) > 0:
                addnl = f'The following additional items are in the room: {", ".join(self.additional_items)}'

            return (
                f'<center>[{self.title.capitalize()}]</center>\n'
                f'{self.formatted_desc} \n\n {addnl}'
            )

        def format_description(self, room_entities):
            self.formatted_desc = self.description
            word_occurances = {}
            noun_occurance = {}
            seen_words = set()
            place_set = set(room_entities[NounKey.LOCATIONS])
            character_set = set(room_entities[NounKey.CHARACTERS])
            item_set = set(
                room_entities[NounKey.FOOD_ITEMS] +
                room_entities[NounKey.ARMOR_ITEMS] +
                room_entities[NounKey.WEAPON_ITEMS] 
            )

            for token in self.description_tokens:
                if token.text in word_occurances.keys():
                    word_occurances[token.text] += 1
                else:
                    word_occurances[token.text] = 1

                if token.pos_ == 'NOUN' and token.text not in seen_words:
                    noun_occurance[token.text] = word_occurances[token.text]
                    seen_words.add(token.text)
            for chunk in self.description_tokens.noun_chunks:
                found_root = False
                for token in chunk:
                    if token.text in set(noun_occurance.keys()):
                        root = token.text
                        found_root = True

                if found_root:
                    if chunk.text in place_set:
                        self.formatted_desc = replacenth(self.formatted_desc, chunk.text, '<r>' + chunk.text + '</r>', noun_occurance[root])
                    elif chunk.text in character_set:
                        self.formatted_desc = replacenth(self.formatted_desc, chunk.text, '<c>' + chunk.text + '</c>', noun_occurance[root])
                    elif chunk.text in item_set:
                        self.formatted_desc = replacenth(self.formatted_desc, chunk.text, '<t>' + chunk.text + '</t>', noun_occurance[root])

        def generate_room_characters(self, char_name_list: []) -> None:
            """
            Generates the characters that are inside the room
            given a list of nouns.

            Args:
                char_name_list: List of character names

            Returns:
                None
            """
            for char_name in char_name_list:
                enemy_gen(char_name, self.characters['You'].level, self)

        def generate_food_items(self, item_name_list: []) -> None:
            """
            Generates the items that are inside the room
            given a list of nouns.

            Args:
                item_name_list: List of item names

            Returns:
                None
            """
            for item_name in item_name_list:
                hp = random.randint(1, 10) * self.characters['You'].level
                item = FoodItem(item_name, hp)
                self.item_list[item_name] = item
                self.original_items.add(item_name)

        def generate_weapon_items(self, item_name_list: []) -> None:
            """
            Generates the items that are inside the room
            given a list of nouns.

            Args:
                item_name_list: List of item names

            Returns:
                None
            """
            for item_name in item_name_list:
                damage = random.randint(1, 10) * self.characters['You'].level
                combat_skill = random.randint(1, 5) * self.characters['You'].level
                item = WeaponItem(item_name, damage, combat_skill)
                self.item_list[item_name] = item
                self.original_items.add(item_name)
                
        def generate_armor_items(self, item_name_list: []) -> None:
            """
            Generates the items that are inside the room
            given a list of nouns.

            Args:
                item_name_list: List of item names

            Returns:
                None
            """
            for item_name in item_name_list:
                armor = random.randint(1, 5) * self.characters['You'].level
                item = ArmorItem(item_name, armor)
                self.item_list[item_name] = item
                self.original_items.add(item_name)       

        def add_item(self, item: object) -> None:
            """
            Adds a given item to the room.

            Args:
                item: the item to add to the room

            Returns:
                None
            """
            self.item_list[item.title] = item
            self.formatted_desc = self.formatted_desc.replace("<s>" + item.title + "</s>", "<t>" + item.title + "</t>")
            if item.title not in self.original_items:
                self.additional_items.add(item.title)

        def remove_item(self, item: str) -> None:
            """
            Removes a given item from the room.

            Args:
                item: the item to remove from the room

            Returns:
                None
            """
            del self.item_list[item.title]
            self.formatted_desc = re.sub(f'<t>( *)({item.title})( *)</t>', r'\1<s>\2</s>\3', self.formatted_desc)
            if item.title in self.additional_items:
                self.additional_items.remove(item.title)



        def enter(self, character: object) -> None:
            """
            Adds a given character to the room. When the room is first
            entered, connected rooms are generated.

            Args:
                character: The character entering the room

            Returns:
                None
            """
            self.characters[character.title] = character
            if not self.entered:
                self.entered = True
                if self.description is None:
                    self.description = describe_location(self.title)
                self.description_tokens = tokenize(self.description)
                room_entities = room_noun_generator(self.description)
                self.room_generator.generate_connected_rooms(self, room_entities[NounKey.LOCATIONS])
                self.generate_room_characters(room_entities[NounKey.CHARACTERS])
                self.generate_food_items(room_entities[NounKey.FOOD_ITEMS])
                self.generate_weapon_items(room_entities[NounKey.WEAPON_ITEMS])
                self.generate_armor_items(room_entities[NounKey.ARMOR_ITEMS])

                self.format_description(room_entities)

        def exit(self, character: object) -> None:
            """
            Removes a given character from the room.

            Args:
                character: The character exiting the room

            Returns:
                None
            """
            self.characters.pop(character.title, None)

