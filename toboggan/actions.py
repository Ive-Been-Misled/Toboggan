"""Describe discrete actions that can be carried out by the player"""
from dataclasses import dataclass
from typing import Any
from difflib import get_close_matches
from .text_generators import describe_location, describe_item


@dataclass
class Introspect:
    placeholder: Any=None

    def execute(self, game, character):
        return str(character)


@dataclass
class Move:
    destination: Any=None

    def execute(self, game, character):
        rooms = character.current_room.connected_rooms
        return_string = f'<center>There is no {self.destination} to move to.</center><br>{str(character.current_room)}'
        if self.destination is not None:
            destinations = get_close_matches(self.destination, rooms.keys())
            if len(destinations) > 0:
                character.move_to(character.current_room.connected_rooms[destinations[0]])
                if destinations[0] != 'back':
                    return_string = f'<center>You move to the {destinations[0]}.</center><br>{str(character.current_room)}'
                else:
                    return_string = f'<center>You move back.</center><br>{str(character.current_room)}'
        else:
            return_string = f'<center>You must specify a location to move to.</center><br>{str(character.current_room)}'
        return return_string


@dataclass
class Pickup:
    thing: Any=None

    def execute(self, game, character):
        items = character.current_room.item_list
        return_string = f'<center>You cannot pick up the {self.thing}.</center><br>{str(character.current_room)}'
        if self.thing is not None:
            things = get_close_matches(self.thing, items.keys())
            if len(things) > 0:
                item = character.current_room.item_list[things[0]]
                character.inventory[things[0]] = item
                character.current_room.remove_item(item)
                return_string = f'<center>You picked up the {things[0]}</center><br>{str(character.current_room)}'
        else:
            return_string = f'<center>You must specifify an object to pick up.</center><br>{str(character.current_room)}'
        
        return return_string


@dataclass
class Drop:
    thing: Any=None

    def execute(self, game, character):
        items = character.inventory
        return_string = f'<center>You don\'t have a {self.thing} to drop.</center><br>{str(character.current_room)}'
        if self.thing is not None:
            things = get_close_matches(self.thing, items.keys())
            if len(things) > 0:
                item = character.inventory[things[0]]
                del character.inventory[things[0]]
                character.current_room.add_item(item)
                return_string = f'<center>You dropped the {things[0]}.</center><br>{str(character.current_room)}'
        else:
            return_string = f'<center>You must specifiy an object to drop.</center><br>{str(character.current_room)}'

        return return_string

@dataclass
class Perceive:
    target: Any=None

    @staticmethod
    def check_lists(target, character):
        if target in set(character.current_room.connected_rooms.keys()):
            return 'room'
        elif (target in set(character.current_room.item_list.keys()) or 
              target in set(character.inventory.keys())):
            return 'item'
        elif target in set(character.current_room.characters.keys()):
            return 'character'
        else:
            return None

    def execute(self, game, character):
        list_id = self.check_lists(self.target, character)
        return_string = f'<center>You look around.</center><br>{str(character.current_room)}'
        if (self.target is not None and
            list_id is not None and
            self.target not in character.current_room.perceived_rooms):
            if list_id == 'room':
                character.current_room.perceived_rooms.append(self.target)
                character.current_room.description = \
                    character.current_room.description + \
                    f"<br><br>You look at the {self.target}.<br><br>" + \
                    describe_location(self.target)
                character.current_room.entered = False
                character.current_room.enter(character)
                return_string = str(character.current_room)
            elif list_id == 'item':
                if self.target in set(character.inventory.keys()):
                    return_string = character.inventory[self.target].generate_description()
                else:
                    return_string = character.current_room.item_list[self.target].generate_description()
            elif list_id == 'character':
                return_string = character.current_room.characters[self.target].generate_description()
        return return_string


@dataclass
class Attack:
    target: Any="nothing"

    def execute(self, game, character):
        room_characters = character.current_room.characters
        targets = get_close_matches(self.target, room_characters.keys())
        if self.target is not None and len(targets) > 0:
            target_key = targets[0]
            target_obj = room_characters[target_key]
            weapon = lambda: None  # Default weapon for now
            weapon.damage = 20
            character.attack(target_obj, weapon)
            if target_obj.hit_points > 0:
                return 'You attacked the ' + target_key + ' for 20 damage!'
            else:
                character.current_room.characters.pop(target_key)
                return 'You killed the ' + target_key + '!'
        else:
            return 'There is no ' + str(self.target) + ' to attack.'
