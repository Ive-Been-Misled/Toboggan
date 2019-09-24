"""Describe discrete actions that can be carried out by the player"""
import atexit
import json
from os import environ, path
from datetime import datetime
from ibm_watson import AssistantV1


class ActionMapper():
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


class Move:
  def __init__(self, direction, distance):
    self.direction = direction
    self.distance = distance
class Interact:
  def __init__(self, interaction, thing):
    self.interaction = interaction
    self.thing = thing
class Percieve:
  def __init__(self, location, sense):
    self.location = location
    self.sense = sense
class Attack:
  def __init__(self, target, player):
    self.target = target
    self.player = player
class Speak:
  def __init__(self, target, dialogue):
    self.target = target
    self.dialogue = dialogue
class CheckSelf:
  def __init__(self, player):
    self.player = player
