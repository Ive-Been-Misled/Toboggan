from .text_generators import describe_location
from .text_generators import room_noun_generator
from .game_components import Character, Item
from .noun_key import NounKey


class RoomGenerator:

    def __init__(self, starting_room_title):
        starting_room_desc = describe_location(starting_room_title)
        self.starting_room = RoomGenerator.Room(starting_room_title, starting_room_desc)
        connected_room_titles = room_noun_generator(starting_room_desc)['place']

        self.generate_connected_rooms(self.starting_room, connected_room_titles)

    @staticmethod
    def generate_connected_rooms(current_room, connected_room_titles):
        if not current_room.entered:
            for title in connected_room_titles:
                connected_room = RoomGenerator.Room(title, None)
                current_room.connected_rooms[title] = connected_room
                connected_room.connected_rooms["back"] = current_room
    
    class Room:
        def __init__(self, title, description, init_characters={}, init_items={}):
            self.title = title
            self.description = description
            self.connected_rooms = {}
            self.characters = init_characters
            self.item_list = init_items
            self.entered = False
        
        def __str__(self):
            chars = ', '.join(self.characters.keys())
            #items = ', '.join(self.item_list.keys())
            return (
                f'[{self.title.capitalize()}] \n\n'
                f'{self.description} \n\n'
                #f'The following characters are in the room: '
                #f'{chars}\n\n'
            )

        def generate_room_characters(self, char_name_list):
            for char_name in char_name_list:
                Character(char_name, self)

        def generate_room_items(self, item_name_list):
            for item_name in item_name_list:
                #TODO: generate item description, weight and type
                item = Item(item_name, '', 1, 1)
                self.item_list[item_name] = item

        def add_item(self, item):
            self.item_list.add(item)

        def remove_item(self, item):
            self.item_list.remove(item)

        def enter(self, character):
            self.characters[character.title] = character
            if not self.entered:
                self.entered = True
                if self.description is None:
                    self.description = describe_location(self.title)
                room_entities = room_noun_generator(self.description)
                RoomGenerator.generate_connected_rooms(self, room_entities['place'])
                self.generate_room_characters(room_entities['character'])
                self.generate_room_items(room_entities['object'])

        def exit(self, character):
            self.characters.pop(character.title, None)

