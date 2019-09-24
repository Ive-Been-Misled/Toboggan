"""Describe discrete actions that can be carried out by the player"""
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
        pass

    @staticmethod
    def get_intents():
        fil = path.join(path.abspath(path.dirname(__file__)), 'actions.json')
        return json.loads(open(fil).read())['intents']

    def cleanup(self):
        self._assistant.delete_workspace(workspace_id=self._workspace_id)


@dataclass
class Move:
    direction: Any
    distance: int

    def execute(self, game, character):
        pass


@dataclass
class Interact:
    interaction: Any
    thing: Any

    def execute(self, game, character):
        pass


@dataclass
class Percieve:
    location: Any
    sense: Any

    def execute(self, game, character):
        pass


@dataclass
class Attack:
    target: Any

    def execute(self, game, character):
        pass


@dataclass
class Speak:
    target: Any
    dialouge: str

    def execute(self, game, character):
        pass


@dataclass
class CheckSelf:

    def execute(self, game, character):
        pass
