"""Describe discrete actions that can be carried out by the player"""
from dataclasses import dataclass
from typing import Any
from difflib import get_close_matches
from .text_generators import describe_location


@dataclass
class Introspect:

    def execute(self, game, character):
        return str(character)


@dataclass
class Move:
    destination: Any=None

    def execute(self, game, character):
        rooms = character.current_room.connected_rooms
        if self.destination is not None:
            destinations = get_close_matches(self.destination, rooms.keys())
            if len(destinations) > 0:
                character.move_to(character.current_room.connected_rooms[destinations[0]])
                return f'You move to the {destinations[0]}.<br><br>{str(character.current_room)}'

        return f'You cannot move to the {self.destination}.<br><br>{str(character.current_room)}'


@dataclass
class Pickup:
    thing: Any=None

    def execute(self, game, character):
        items = character.current_room.item_list
        print(items.keys())
        if self.thing is not None:
            things = get_close_matches(self.thing, items.keys())
            if len(things) > 0:
                character.inventory[things[0]] = character.current_room.item_list[things[0]]
                del character.current_room.item_list[things[0]]
                return f'You picked up the {things[0]}<br><br>{str(character.current_room)}'

        return f'You cannot pick up the {self.thing}.<br><br>{str(character.current_room)}'


@dataclass
class Drop:
    item: Any=None

    def execute(self, game, character):
        return f'You drop the {self.item}'

@dataclass
class Perceive:
    target: Any=None
    sense: Any=None

    @staticmethod
    def check_lists(target, character):
        if target in set(character.current_room.connected_rooms.keys()):
            return 'room'
        elif target in set(character.current_room.item_list.keys()):
            return 'item'
        elif target in set(character.current_room.characters.keys()):
            return 'character'
        else:
            return None

    def execute(self, game, character):
        list_id = self.check_lists(self.target, character)

        if (self.target is not None and
            list_id is not None and
            self.target not in character.current_room.perceived_rooms):

            character.current_room.perceived_rooms.append(self.target)
            character.current_room.description = \
                character.current_room.description + \
                "<br><br>" + \
                describe_location(self.target)
                # TODO:  ^^change this function so that it differentiates between items, rooms, 
                # and characters (use list_id)
            character.current_room.entered = False
            character.current_room.enter(character)
        
        return str(character.current_room)


@dataclass
class Attack:
    target: Any=None

    def execute(self, game, character):
        room_characters = character.current_room.characters
        targets = get_close_matches(self.target, room_characters.keys())
        if self.target is not None and len(targets) > 0:
            target_key = targets[0]
            target_obj = room_characters[target_key]
            character.attack(target_obj, 20) # TODO damage is hardcoded for now. this will need to change
            if target_obj.hit_points > 0:
                return 'You attacked the ' + target_key + ' for 20 damage!'
            else:
                character.current_room.characters.pop(target_key)
                return 'You killed the ' + target_key + '!'
        else:
            return 'There is no ' + str(self.target) + ' to attack.'