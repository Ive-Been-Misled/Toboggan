"""
Room generation and room data storage.
"""
from .text_generators import describe_location
from .text_generators import room_noun_generator
from .game_components import Character, Item
#from .noun_key import NounKey


class RoomGenerator:
    """
    Generates rooms and room connections.
    """
    def __init__(self, starting_room_title):
        starting_room_desc = describe_location(starting_room_title)
        self.starting_room = RoomGenerator.Room(self, starting_room_title, starting_room_desc)

        self.room_list = []
        self.room_list.append(self.starting_room)

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
            self.description = description
            self.connected_rooms = {}
            self.characters = {}
            self.item_list = {}
            self.entered = False
        
        def __str__(self):
            #chars = ', '.join(self.characters.keys())
            #items = ', '.join(self.item_list.keys())
            return (
                f'[{self.title.capitalize()}] \n\n'
                f'{self.description} \n\n'
                #f'The following characters are in the room: '
                #f'{chars}\n\n'
            )

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
                Character(char_name, self)

        def generate_room_items(self, item_name_list: []) -> None:
            """
            Generates the items that are inside the room
            given a list of nouns.

            Args:
                item_name_list: List of item names

            Returns:
                None
            """
            for item_name in item_name_list:
                #TODO: generate item description, weight and type
                item = Item(item_name, '', 1, 1)
                self.item_list[item_name] = item

        def add_item(self, item: object) -> None:
            """
            Adds a given item to the room.

            Args:
                item: the item to add to the room

            Returns:
                None
            """
            self.item_list[item.title] = item

        def remove_item(self, item: object) -> None:
            """
            Removes a given item from the room.

            Args:
                item: the item to remove from the room

            Returns:
                None
            """
            del self.item_list[item.title]

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
                room_entities = room_noun_generator(self.description)
                self.room_generator.generate_connected_rooms(self, room_entities['place'])
                self.generate_room_characters(room_entities['character'])
                self.generate_room_items(room_entities['object'])

        def exit(self, character: object) -> None:
            """
            Removes a given character from the room.

            Args:
                character: The character exiting the room

            Returns:
                None
            """
            self.characters.pop(character.title, None)

