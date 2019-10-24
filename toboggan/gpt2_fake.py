from faker import Faker
from spacy.lang.en import English

class _GPT2_Fake:
    def __init__(self):
        self.fake = Faker()
        nlp = English()
        self.tokenizer = nlp.Defaults.create_tokenizer(nlp)

    def sample_sequence(self, input_text: str):
        while 1:
            for token in self.tokenizer(self.fake.text()):
                if token.text is '.':
                    yield '.'
                else:
                    yield ' ' + token.text

GPT2 = _GPT2_Fake()
