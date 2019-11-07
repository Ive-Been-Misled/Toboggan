"""Use IBM Watson to map actions"""
import sys
import json
from os import environ, path
from datetime import datetime
from ibm_watson import AssistantV1
from .actions import Move, Percieve
from .text_generators import _NLP


class ActionMapper:
    """Utility to map natural language into a set of pre-defined action
    classes.
    """
    def __init__(self):
        if ActionMapper._has_previous_workspace():
            info = ActionMapper._get_api_and_workspace_info()
            api_key = info['api_key']
            self._assistant = ActionMapper._create_assistant(api_key)
            self._workspace_id = info['workspace_id']
        else:
            api_key = environ['API_KEY']
            self._assistant = ActionMapper._create_assistant(api_key)
            self._workspace_id = ActionMapper._create_workspace(self._assistant)
            ActionMapper._save_api_and_workspace_info(api_key, self._workspace_id)

        self._nlp = _NLP

    def simple_map(self, input_string):
        """Return only a Percieve or Move action."""
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

    def map(self, input_string):
        """Return an action corresponding the input_string, or None if no
        suitable match is found by Assistant.
        """
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
    def _has_previous_workspace():
        file_path = path.join(ActionMapper._dir(), 'watson_api.json')
        return path.exists(file_path)

    @staticmethod
    def _get_api_and_workspace_info():
        return json.loads(open(ActionMapper._info_file_path()).read())

    @staticmethod
    def _create_assistant(api_key):
        return AssistantV1(
            version='2019-02-28',
            iam_apikey=api_key,
            url='https://gateway.watsonplatform.net/assistant/api'
        )

    @staticmethod
    def _create_workspace(assistant):
        return assistant.create_workspace(
            name='Toboggan',
            description=f'Created at {datetime.strftime(datetime.now(),"%c")}',
            intents=ActionMapper._get_intents()
        ).get_result()['workspace_id']

    @staticmethod
    def _save_api_and_workspace_info(api_key, workspace_id):
        info = {
            'api_key': api_key,
            'workspace_id': workspace_id
        }
        with open(ActionMapper._info_file_path(), mode='w') as info_file:
            print(json.dumps(info, indent=2), file=info_file)

    @staticmethod
    def _get_intents():
        return json.loads(open(ActionMapper._intents_file_path()).read())['intents']

    @staticmethod
    def _info_file_path():
        return path.join(ActionMapper._dir(), 'watson_api.json')

    @staticmethod
    def _intents_file_path():
        return path.join(ActionMapper._dir(), 'actions.json')

    @staticmethod
    def _dir():
        return path.abspath(path.dirname(__file__))
