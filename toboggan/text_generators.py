"""Stateless NLP utility functions"""
from os import environ
from typing import Iterator
import spacy



if 'FAKE_GPT2' in environ:
    from .gpt2_fake import GPT2
else:
    from .gpt2 import GPT2

_NLP = spacy.load('en_core_web_lg')
COMPARE_WORDS = ['place', 'object', 'character']

def describe_location(location: str) -> str:
    """Given a location, returns a description of location"""
    prompt = f"""\
    You are in {location}. You look around. You see
    """
    description = 'You see'

    current_length = 0
    min_length = 42

    for token in GPT2.sample_sequence(prompt):
        description += token
        current_length += 1
        print(f"DEBUG: {token}")
        if current_length >= min_length and token in ('.', '?', '#', '"'):
            break

    return description

def noun_chunks(text: str) -> Iterator[str]:
    """Given some text, return the noun chunks"""
    doc = _NLP(text)
    return doc.noun_chunks


def room_noun_generator(text: str) -> dict:
    """Given a description, return a list of mentioned nouns and their type"""
    doc = _NLP(text)
    title_list = {'place':[], 'object':[], 'character':[]}
    for token in doc:
        if token.pos_ == 'NOUN' and token.text != 'back':
            title_list[noun_classifier(token.text)].append(token.text)
    return title_list

def tokenize(text: str):
    doc = _NLP(text)
    return doc

def noun_classifier(word: str) -> str:
    """Determines what type of noun a passed noun is."""
    tokens = _NLP(' '.join(COMPARE_WORDS))
    word_token = _NLP(word)
    max_score = 0
    best_class = ''
    for token in tokens:
        temp_score = token.similarity(word_token)
        if temp_score > max_score:
            max_score = temp_score
            best_class = token.text
    return best_class
