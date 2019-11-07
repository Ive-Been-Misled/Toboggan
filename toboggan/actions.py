"""Describe discrete actions that can be carried out by the player"""
from dataclasses import dataclass
from typing import Any
from difflib import get_close_matches


@dataclass
class Percieve:
    location: Any=None
    sense: Any=None

    def execute(self, game, character):
        return str(character.current_room)


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
