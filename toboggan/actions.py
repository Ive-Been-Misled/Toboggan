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
    destination: Any

    def execute(self, game, character):
        if self.destination in character.current_room.connected_rooms:
            moved = character.move_to(character.current_room.connected_rooms[self.destination])
        else:
            moved = False
        if moved:
            return str(character.current_room)
        else:
            return f'You cannot move to {self.destination}.'


@dataclass
class Pickup:
    interaction: Any
    thing: Any=None

    def execute(self, game, character):
        if len(character.current_room.item_list) >0:
            for x,y in character.current_room.item_list.items():
                character.inventory[x] = y
                character.current_room.item_list.pop(x)
                return f'You picked up a {x}'
        else:
            return 'There are nothing to pick up in this room.'


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
        if self.target is not None and targets:
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