"""Describe discrete actions that can be carried out by the player"""
import sys
from dataclasses import dataclass
from typing import Any
import atexit
import json
from os import environ, path
from datetime import datetime
from ibm_watson import AssistantV1


class ActionMapper:
    def __init__(self):
        self._assistant = AssistantV1(
            version='2019-02-28',
            iam_apikey=environ['API_KEY'],
            url='https://gateway.watsonplatform.net/assistant/api'
        )
        self._workspace_id = self._assistant.create_workspace(
            name='Toboggan',
            description=f'Created at {datetime.strftime(datetime.now(),"%c")}',
            intents=self.__class__.get_intents()
        ).get_result()['workspace_id']
        atexit.register(self.cleanup)

    def map(self, input_string):
        result = self._assistant.message(
            workspace_id=self._workspace_id,
            input={'text': input_string}
        ).get_result()

        intents = result['intents']

        if not intents:
            return None

        action_class = intents[0]['intent'].split('_')[0].capitalize()

        if len(intents[0]['intent'].split('_')) > 1:
            param = intents[0]['intent'].split('_')[1]
            return vars(sys.modules[__name__])[action_class](param)

        return vars(sys.modules[__name__])[action_class]()

    @staticmethod
    def get_intents():
        fil = path.join(path.abspath(path.dirname(__file__)), 'actions.json')
        return json.loads(open(fil).read())['intents']

    def cleanup(self):
        self._assistant.delete_workspace(workspace_id=self._workspace_id)


@dataclass
class Move:
    direction: Any
    distance: int=0

    def execute(self, game, character):
        pass


@dataclass
class Interact:
    interaction: Any
    thing: Any=None

    def execute(self, game, character):
        pass


@dataclass
class Percieve:
    location: Any=None
    sense: Any=None

    def execute(self, game, character):
        pass


@dataclass
class Attack:
    target: Any=None

    def execute(self, game, character):
        pass


@dataclass
class Speak:
    target: Any
    dialouge: str=''

    def execute(self, game, character):
        pass


@dataclass
class Introspect:

    def execute(self, game, character):
        pass
