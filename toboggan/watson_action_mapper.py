"""Use IBM Watson to map actions"""
import sys
import json
from os import environ, path
from datetime import datetime
from ibm_watson import AssistantV1
import spacy
from .actions import Move, Percieve


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

        self._nlp = spacy.load('en_core_web_lg')

    def map(self, input_string):
        if input_string == 'look around':
            return Percieve()

        doc = self._nlp(input_string)
        obj = "nothing"
        for token in doc:
            if (token.dep_ == 'dobj' or
                token.dep_ == 'advmod' or
                token.dep_ == 'pobj'):
                obj = token.text

        return Move(destination=obj)

    # use a simpler map for demo purposes until assistant can be retrained
    def _map(self, input_string):
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
            if token.dep_ == 'dobj' or token.dep_ == 'advmod':
                direct_object = token.text
                print(f'direct object: {direct_object}')
            if token.dep_ == 'pobj':
                prep_object = token.text
                print(f'prepositional object: {prep_object}')

        action_class = intents[0]['intent'].split('_')[0].capitalize()
        if action_class == 'Move' and direct_object:
            return vars(sys.modules[__name__])[action_class](direct_object)
        #TODO implement case for both attack and move where no direct object is given

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