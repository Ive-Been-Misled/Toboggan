"""Describe discrete actions that can be carried out by the player"""
from dataclasses import dataclass
from typing import Any
from difflib import get_close_matches
from .text_generators import describe_location, describe_item
from .game_components import FoodItem, WeaponItem, ArmorItem
from .text_generators import _NLP
from operator import attrgetter

def find_match(key_list, elem):
    elems = get_close_matches(elem, key_list)
    if len(elems) == 0:
        new_elem = ''
        for token in _NLP(elem):
            if token.text not in ['the', 'a', 'an']:
                new_elem += token.text_with_ws
        elems = get_close_matches(new_elem, key_list)
        
        [elems.append(key) for key in key_list if new_elem in key]

    if elems:
        return elems[0]
        
def center_string(string):
    return '<center>' + string + '</center>'

@dataclass
class Introspect:
    placeholder: Any=None

    def execute(self, game, character):
        return str(character) + '<br><br>' + str(character.current_room)


@dataclass
class Move:
    destination: Any=None

    @staticmethod
    def run_away_response(game, character):
        enemies_in_room = len(character.current_room.characters) > 1

        if enemies_in_room:
            if character.speed <= max(game.combat.initiative, key=attrgetter('speed')).speed:
                return center_string(
                    f'You attempt to escape to another room, but alas '
                    f'{game.combat.initiative[0].title} is too fast and prevents you from escaping.<br>'
                    f'It seems you must face your enemies or die trying.'
                )
            game.active_combat = False
            return center_string(f'You manage to escape your foes in the previous room through your superior speed.')
            
        game.active_combat = False
        return ''

    def execute(self, game, character):
        current_room = character.current_room

        if self.destination is None:
            return center_string('You must specify a location to move to.') + f'<br>{str(current_room)}'
        
        destination_match = find_match(current_room.connected_rooms.keys(), self.destination)
        if destination_match is None:
            return center_string(f'There is no {self.destination} to move to.') + f'<br>{str(current_room)}'
        
        return_string = self.run_away_response(game, character)
        
        if not game.active_combat:
            article = ''
            if _NLP(destination_match)[0].text not in ['the', 'an', 'a']: article = 'the'

            character.move_to(current_room.connected_rooms[destination_match])

            if destination_match != 'back':
                return_string += center_string(f'You move to {article} {destination_match}.')
            else:
                return_string += center_string('You move back.')

        return_string += f'<br>{str(character.current_room)}'
        return return_string


@dataclass
class Pickup:
    thing: Any=None

    @staticmethod
    def pickup(item_match, character):
        article = ''
        if _NLP(item_match)[0].text not in ['the', 'an', 'a']: article = 'the'

        item = character.current_room.item_list[item_match]
        character.inventory[item_match] = item
        character.current_room.remove_item(item)

        return center_string(f'You picked up {article} {item_match}') + f'<br>{str(character.current_room)}'

    def execute(self, game, character):
        if self.thing is None:
            return center_string(f'You must specifify an object to pick up.') + f'<br>{str(character.current_room)}'

        item_match = find_match(character.current_room.item_list.keys(), self.thing)

        if item_match is None:
            return center_string(f'You cannot pick up the {self.thing}.') + f'<br>{str(character.current_room)}'

        return self.pickup(item_match, character)


@dataclass
class Use:
    thing: Any=None

    @staticmethod
    def use_item(item_match, character):
        item = character.inventory[item_match]
        article = ''
        if _NLP(item_match)[0].text not in ['the', 'an', 'a']: article = 'the'

        item_functions = {
            FoodItem: character.use_food_item,
            WeaponItem: character.equip_weapon,
            ArmorItem: character.equip_armor
        }
        
        response = item_functions[type(item)](item)
        del character.inventory[item_match]
        return center_string(response).replace(item_match, f'{article} {item_match}') + f'<br>{str(character.current_room)}'

    def execute(self, game, character):
        if self.thing is None:
            return center_string(f'You must specifify an object to use.') + f'<br>{str(character.current_room)}'

        item_match = find_match(character.inventory.keys(), self.thing)

        if item_match is None:
            return center_string(f'You do not have a {self.thing}.') + f'<br>{str(character.current_room)}'

        return self.use_item(item_match, character)

@dataclass
class Drop:
    thing: Any=None

    @staticmethod
    def drop(item_match, character):
        article = ''
        if _NLP(item_match)[0].text not in ['the', 'an', 'a']: article = 'the'

        item = character.inventory[item_match]
        del character.inventory[item_match]
        character.current_room.add_item(item)

        return center_string(f'You dropped {article} {item_match}') + f'<br>{str(character.current_room)}'

    def execute(self, game, character):
        if self.thing is None:
            return center_string(f'You must specifify an object to drop.') + f'<br>{str(character.current_room)}'

        item_match = find_match(character.inventory.keys(), self.thing)

        if item_match is None:
            return center_string(f'You don\'t have a {self.thing} to drop.') + f'<br>{str(character.current_room)}'

        return self.drop(item_match, character)

@dataclass
class Perceive:
    target: Any=None

    @staticmethod
    def check_lists(target, character):
        if target is None:
            return None

        current_room = character.current_room

        entity_groups = [
            #current_room.connected_rooms,
            current_room.item_list,
            character.inventory,
            current_room.characters
        ]
        for group in entity_groups:
            match = find_match(group.keys(), target)
            if match is not None:
                return group[match]

        return None

    def execute(self, game, character):
        match = self.check_lists(self.target, character)
        if match is None:
            return center_string(f'You look around.') + f'<br>{str(character.current_room)}'
        match.generate_description()
        return str(match) + '<br><br>' + str(character.current_room)


@dataclass
class Attack:
    target: Any="nothing"

    def execute(self, game, character):
        room_characters = character.current_room.characters
        
        if self.target is None:
            return center_string(f'You must specify a target to attack.') + f'<br>{str(character.current_room)}'

        target_key = find_match(room_characters.keys(), self.target)

        if target_key is None:
            return center_string(f'There is no {str(self.target)} to attack.') + f'<br>{str(character.current_room)}'

        target_obj = room_characters[target_key]
        attack_str = character.attack(target_obj)
        if target_obj.hit_points > 0:
            return center_string(attack_str) + f'<br>{str(character.current_room)}'
        else:
            character.current_room.formatted_desc = character.current_room.formatted_desc.replace("<c>" + target_key + "</c>", "<s>" + target_key + "</s>")
            character.current_room.characters.pop(target_key)
            return center_string(f'{attack_str}<br>You killed {target_key}!') + f'<br>{str(character.current_room)}'
