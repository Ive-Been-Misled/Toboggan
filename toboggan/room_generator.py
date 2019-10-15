# TODO: remove this test code, replace with actual functions
# # # # 
i = 0

def generate_description(title):
    global i
    i += 1
    return title + " " + str(i)

def generate_connected_titles(desc):
    return ["north", "east", "west"]
# # # #

class RoomGenerator:

    def __init__(self, starting_room_title):
        starting_room_desc = generate_description(starting_room_title)
        self.starting_room = RoomGenerator.Room(starting_room_title, starting_room_desc, {})

        connected_room_titles = generate_connected_titles(starting_room_desc)

        self.generate_connected_rooms(self.starting_room, connected_room_titles)

    @staticmethod
    def generate_connected_rooms(current_room, connected_room_titles):
        if not current_room.entered:
            for title in connected_room_titles:
                desc = generate_description(title)
                connected_room = RoomGenerator.Room(title, desc, {})
                current_room.connected_rooms[title] = connected_room

                # TODO: change this to "back" later
                connected_room.connected_rooms["back"] = current_room
    
    class Room:
        def __init__(self, title, description, connected_rooms, init_characters={}, init_items={}):
            self.title = title
            self.description = description
            self.connected_rooms = {}
            #self.connected_rooms = { 'north': connected_rooms[0], 'south': connected_rooms[1], 'east': connected_rooms[2], 'west': connected_rooms[3] }
            self.characters = init_characters
            self.item_list = init_items
            self.entered = False
        
        def __str__(self):
            chars = ', '.join(self.characters.keys())
            #items = ', '.join(self.item_list.keys())
            return (
                f'[{self.title}] \n\n'
                f'{self.description} \n\n'
                f'The following characters are in the room: '
                f'{chars}\n\n'
            )

        def add_item(self, item):
            self.item_list.add(item)

        def remove_item(self, item):
            self.item_list.remove(item)

        def enter(self, character):
            self.characters[character.title] = character
            connected_room_titles = generate_connected_titles(self.description)
            RoomGenerator.generate_connected_rooms(self, connected_room_titles)
            self.entered = True

        def exit(self, character):
            self.characters.pop(character.title, None)

