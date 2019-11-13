"""Describe discrete actions that can be carried out by the player"""
from dataclasses import dataclass
from typing import Any
from difflib import get_close_matches
from .text_generators import describe_location, describe_item
from .game_components import FoodItem, WeaponItem, ArmorItem

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
class Use:
    thing: Any=None

    def execute(self, game, character):
        items = character.inventory
        return_string = f'<center>You do not have a {self.thing}.</center><br>{str(character.current_room)}'
        if self.thing is not None:
            things = get_close_matches(self.thing, items.keys())
            if len(things) > 0:
                item = character.inventory[things[0]]
                if type(item) is FoodItem:
                    character.gain_hp(item.hp)
                    return_string = f'<center>You used the {things[0]} and gained {item.hp} hit points.</center><br>{str(character.current_room)}'
                elif type(item) is WeaponItem:
                    character.equip_weapon(item)
                    return_string = f'<center>You equipped the {things[0]}.</center><br>{str(character.current_room)}'
                elif type(item) is ArmorItem:
                    character.equip_armor(item)
                    return_string = f'<center>You equipped the {things[0]}.</center><br>{str(character.current_room)}'
                del character.inventory[things[0]]                
        else:
            return_string = f'<center>You must specifify an object to use.</center><br>{str(character.current_room)}'
        
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
        print(target)
        rooms = character.current_room.connected_rooms.keys()
        items = list(character.current_room.item_list.keys()) + list(character.inventory.keys())
        characters = character.current_room.characters.keys()
        if target is not None:
            room_matches = get_close_matches(target, rooms)
            item_matches = get_close_matches(target, items)
            character_matches = get_close_matches(target, characters)
        else:
            return None, None
        if len(room_matches) > 0:
            return room_matches[0], 'room'
        elif len(item_matches) > 0:
            return item_matches[0], 'item'
        elif len(character_matches) > 0:
            return character_matches[0],  'character'
        else:
            return None, None

    def execute(self, game, character):
        match, list_id = self.check_lists(self.target, character)
        return_string = f'<center>You look around.</center><br>{str(character.current_room)}'
        if (match is not None and
            list_id is not None and
            match not in character.current_room.perceived_rooms):
            if list_id == 'room':
                character.current_room.perceived_rooms.append(match)
                character.current_room.description = \
                    character.current_room.description + \
                    f"<br><br>You look at the {match}.<br><br>" + \
                    describe_location(match)
                character.current_room.entered = False
                character.current_room.enter(character)
                return_string = str(character.current_room)
            elif list_id == 'item':
                if match in set(character.inventory.keys()):
                    item = character.inventory[match]
                else:
                    item = character.current_room.item_list[match]
                return_string = str(item) + item.generate_description()
            elif list_id == 'character':
                return_string = character.current_room.characters[match].generate_description()
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
            attack_str = character.attack(target_obj)
            if target_obj.hit_points > 0:
                return f'<center>{attack_str}</center><br>{str(character.current_room)}'
            else:
                character.current_room.formatted_desc = character.current_room.formatted_desc.replace("<c>" + target_key + "</c>", "<s>" + target_key + "</s>")
                character.current_room.characters.pop(target_key)
                return f'<center>{attack_str}</center><center>You killed the {target_key}!</center><br>{str(character.current_room)}'
        else:
            return f'There is no {str(self.target)} to attack.<br>{str(character.current_room)}'
