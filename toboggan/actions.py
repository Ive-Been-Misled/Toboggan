"""Describe discrete actions that can be carried out by the player"""
import sys
from dataclasses import dataclass
from typing import Any
import json
from os import environ, path
from datetime import datetime
from ibm_watson import AssistantV1
import spacy
from difflib import get_close_matches


class ActionMapper:
    def __init__(self):
        if ActionMapper.has_previous_workspace():
            info = ActionMapper.get_api_and_workspace_info()
            api_key = info['api_key']
            self._assistant = ActionMapper.create_assistant(api_key)
            self._workspace_id = info['workspace_id']
        else:
            api_key = environ['API_KEY']
            self._assistant = ActionMapper.create_assistant(api_key)
            self._workspace_id = ActionMapper.create_workspace(self._assistant)
            ActionMapper.save_api_and_workspace_info(api_key, self._workspace_id)

        self._nlp = spacy.load('en_core_web_sm')

    def map(self, input_string):
        intents = self._assistant.message(
            workspace_id=self._workspace_id,
            input={'text': input_string}
        ).get_result()['intents']

        if not intents:
            return None

        doc = self._nlp(input_string)
        direct_object = None
        prep_object = None
        for token in doc:
            if token.dep_ == 'dobj':
                direct_object = token.text
                print(f'direct object: {token.text}')
            if token.dep_ == 'pobj':
                prep_object = token.text
                print(f'prepositional object: {token.text}')

        action_class = intents[0]['intent'].split('_')[0].capitalize()
        if action_class == 'Attack' and direct_object:
            return vars(sys.modules[__name__])[action_class](direct_object)

        if len(intents[0]['intent'].split('_')) > 1:
            param = intents[0]['intent'].split('_')[1]
            return vars(sys.modules[__name__])[action_class](param)

        return vars(sys.modules[__name__])[action_class]()

    @staticmethod
    def has_previous_workspace():
        file_path = path.join(ActionMapper.dir(), 'watson_api.json')
        return path.exists(file_path)

    @staticmethod
    def get_api_and_workspace_info():
        return json.loads(open(ActionMapper.info_file_path()).read())

    @staticmethod
    def create_assistant(api_key):
        return AssistantV1(
            version='2019-02-28',
            iam_apikey=api_key,
            url='https://gateway.watsonplatform.net/assistant/api'
        )

    @staticmethod
    def create_workspace(assistant):
        return assistant.create_workspace(
            name='Toboggan',
            description=f'Created at {datetime.strftime(datetime.now(),"%c")}',
            intents=ActionMapper.get_intents()
        ).get_result()['workspace_id']

    @staticmethod
    def save_api_and_workspace_info(api_key, workspace_id):
        info = {
            'api_key': api_key,
            'workspace_id': workspace_id
        }
        with open(ActionMapper.info_file_path(), mode='w') as info_file:
            print(json.dumps(info, indent=2), file=info_file)

    @staticmethod
    def get_intents():
        return json.loads(open(ActionMapper.intents_file_path()).read())['intents']

    @staticmethod
    def info_file_path():
        return path.join(ActionMapper.dir(), 'watson_api.json')

    @staticmethod
    def intents_file_path():
        return path.join(ActionMapper.dir(), 'actions.json')

    @staticmethod
    def dir():
        return path.abspath(path.dirname(__file__))


@dataclass
class Move:
    direction: Any
    distance: int=0

    def execute(self, game, character):
        if self.direction in character.current_room.connected_rooms:
            moved = character.move_to(character.current_room.connected_rooms[self.direction])
        else:
            moved = False
        if moved:
            return str(character.current_room)
        else:
            return f'You cannot move {self.direction}.'


@dataclass
class Interact:
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
class Percieve:
    location: Any=None
    sense: Any=None

    def execute(self, game, character):
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

@dataclass
class Speak:
    target: Any
    dialouge: str=''

    def execute(self, game, character):
        return 'Speak not yet implemented.'


@dataclass
class Introspect:

    def execute(self, game, character):
        return str(character)
