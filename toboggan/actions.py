"""Describe discrete actions that can be carried out by the player"""
from dataclasses import dataclass
from typing import Any
from difflib import get_close_matches
from .text_generators import describe_location, describe_item
from .game_components import FoodItem, WeaponItem, ArmorItem
from .text_generators import _NLP

@dataclass
class Introspect:
    placeholder: Any=None

    def execute(self, game, character):
        return str(character) + '<br><br>' + str(character.current_room)


@dataclass
class Move:
    destination: Any=None

    def execute(self, game, character):
        rooms = character.current_room.connected_rooms
        return_string = f'<center>There is no {self.destination} to move to.</center>'
        if self.destination is not None:
            destinations = get_close_matches(self.destination, rooms.keys())

            if len(destinations) == 0:
                new_destination = ''
                for token in _NLP(self.destination):
                    if token.text != 'the' and token.text != 'a' and token.text != 'an':
                        new_destination += token.text_with_ws
                destinations = get_close_matches(new_destination, rooms.keys())

            if len(destinations) == 0:
                tokens = _NLP(self.destination)
                word = ''
                for token in tokens:
                    if token.text != 'the' and token.text != 'an' and token.text != 'a':
                        word += token.text_with_ws
                for room in rooms.keys():
                    if word in room:
                        destinations.append(room)
            
            if len(destinations) > 0:
                if len(character.current_room.characters) > 1 and character.speed <= game.combat.initiative[0].speed:
                    return_string = (
                        f'<center>You attempt to escape to another room, but alas {game.combat.initiative[0].title} is too fast and prevents you from escaping.</center>'
                          '<center>It seems you must face your enemies or die trying.</center>'
                    )
                elif len(character.current_room.characters) > 1 and character.speed > game.combat.initiative[0].speed:
                    
                    return_string = (
                        f'<center>You manage to escape your foes in the previous room through your superior speed.</center>'
                          
                    )
                    game.active_combat = False
                    character.move_to(character.current_room.connected_rooms[destinations[0]])
                    if destinations[0] != 'back':
                        return_string += f'<center>You move to the {destinations[0]}.</center>'
                    else:
                        return_string += f'<center>You move back.</center>'
                else:
                    game.active_combat = False
                    character.move_to(character.current_room.connected_rooms[destinations[0]])
                    if destinations[0] != 'back':
                        return_string = f'<center>You move to the {destinations[0]}.</center>'
                    else:
                        return_string = f'<center>You move back.</center>'
        else:
            return_string = f'<center>You must specify a location to move to.</center>'
        return_string += f'<br>{str(character.current_room)}'
        return return_string


@dataclass
class Pickup:
    thing: Any=None

    def execute(self, game, character):
        items = character.current_room.item_list
        return_string = f'<center>You cannot pick up the {self.thing}.</center><br>{str(character.current_room)}'
        if self.thing is not None:
            things = get_close_matches(self.thing, items.keys())

            if len(things) == 0:
                new_thing = ''
                for token in _NLP(self.thing):
                    if token.text != 'the' and token.text != 'a' and token.text != 'an':
                        new_thing += token.text_with_ws
                things = get_close_matches(new_thing, items.keys())

            if len(things) == 0:
                tokens = _NLP(self.thing)
                word = ''
                for token in tokens:
                    if token.text != 'the' and token.text != 'an' and token.text != 'a':
                        word += token.text_with_ws
                
                for item in items.keys():
                    if word in item:
                        things.append(item)
            
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

            if len(things) == 0:
                new_thing = ''
                for token in _NLP(self.thing):
                    if token.text != 'the' and token.text != 'a' and token.text != 'an':
                        new_thing += token.text_with_ws
                things = get_close_matches(new_thing, items.keys())

            if len(things) == 0:
                tokens = _NLP(self.thing)
                word = ''
                for token in tokens:
                    if token.text != 'the' and token.text != 'an' and token.text != 'a':
                        word += token.text_with_ws

                for item in items.keys():
                    if word in item:
                        things.append(item)

            if len(things) > 0:
                item = character.inventory[things[0]]
                if type(item) is FoodItem:
                    character.gain_hp(item.hp)
                    return_string = f'<center>You used the {things[0]} and gained {item.hp} hit points.</center><br>{str(character.current_room)}'
                elif type(item) is WeaponItem:
                    character.equip_weapon(item)
                    return_string = f'<center>You equipped the {things[0]} in your weapon slot.</center><br>{str(character.current_room)}'
                elif type(item) is ArmorItem:
                    character.equip_armor(item)
                    return_string = f'<center>You equipped the {things[0]} in your armor slot.</center><br>{str(character.current_room)}'
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

            if len(things) == 0:
                new_thing = ''
                for token in _NLP(self.thing):
                    if token.text != 'the' and token.text != 'a' and token.text != 'an':
                        new_thing += token.text_with_ws
                things = get_close_matches(new_thing, items.keys())

            if len(things) == 0:
                tokens = _NLP(self.thing)
                word = ''
                for token in tokens:
                    if token.text != 'the' and token.text != 'an' and token.text != 'a':
                        word += token.text_with_ws
                
                for item in items.keys():
                    if word in item:
                        things.append(item)

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
        rooms = character.current_room.connected_rooms.keys()
        items = list(character.current_room.item_list.keys()) + list(character.inventory.keys())
        characters = character.current_room.characters.keys()
        if target is not None:
            room_matches = get_close_matches(target, rooms)
            item_matches = get_close_matches(target, items)
            character_matches = get_close_matches(target, characters)

            if len(room_matches + item_matches + character_matches) == 0:
                new_target = ''
                for token in _NLP(target):
                    if token.text != 'the' and token.text != 'a' and token.text != 'an':
                        new_target += token.text_with_ws
                room_matches = get_close_matches(new_target, rooms)
                item_matches = get_close_matches(new_target, items)
                character_matches = get_close_matches(new_target, characters)
        
            if len(room_matches + item_matches + character_matches) == 0:
                tokens = _NLP(target)
                word = ''
                for token in tokens:
                    if token.text != 'the' and token.text != 'an' and token.text != 'a':
                        word += token.text_with_ws
                
                for elem in rooms:
                    if word in elem:
                        room_matches.append(elem)
                for elem in items:
                    if word in elem:
                        item_matches.append(elem)
                for elem in characters:
                    if word in elem:
                        character_matches.append(elem)
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
                # character.current_room.perceived_rooms.append(match)
                # character.current_room.description = \
                #     character.current_room.description + \
                #     f"<br><br>You look at the {match}.<br><br>" + \
                #     describe_location(match)
                # character.current_room.entered = False
                # character.current_room.enter(character)
                # return_string = str(character.current_room)
                pass
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
        
        if self.target is not None:
            targets = get_close_matches(self.target, room_characters.keys())
            
            if len(targets) == 0:
                new_target = ''
                for token in _NLP(self.target):
                    if token.text != 'the' and token.text != 'a' and token.text != 'an':
                        new_target += token.text_with_ws
                targets = get_close_matches(new_target, room_characters.keys())
            
            if len(targets) == 0:
                tokens = _NLP(self.target)
                word = ''
                for token in tokens:
                    if token.text != 'the' and token.text != 'an' and token.text != 'a':
                        word += token.text_with_ws
                
                for elem in room_characters:
                    if word in elem:
                        targets.append(elem)

            if len(targets) > 0:
                target_key = targets[0]
                target_obj = room_characters[target_key]
                attack_str = character.attack(target_obj)
                if target_obj.hit_points > 0:
                    return f'<center>{attack_str}</center><br>{str(character.current_room)}'
                else:
                    character.current_room.formatted_desc = character.current_room.formatted_desc.replace("<c>" + target_key + "</c>", "<s>" + target_key + "</s>")
                    character.current_room.characters.pop(target_key)
                    return f'<center>{attack_str}</center><center>You killed {target_key}!</center><br>{str(character.current_room)}'
            else:
                return f'<center>There is no {str(self.target)} to attack.</center><br>{str(character.current_room)}'
        else:
            return f'<center>You must specify a target to attack.</center><br>{str(character.current_room)}'
