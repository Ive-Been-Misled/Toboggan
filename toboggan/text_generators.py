"""Stateless NLP utility functions"""
from os import environ
from typing import Iterator
import spacy

if 'FAKE_GPT2' in environ:
    from .gpt2_fake import GPT2
else:
    from .gpt2 import GPT2

_nlp = spacy.load('en_core_web_lg')


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
    doc = _nlp(text)
    return doc.noun_chunks


def room_title_generator(text: str) -> list:
    """Given a description, return a list of mentioned locations"""
    doc = _nlp(text)
    title_list = []
    for token in doc:
        if token.pos_ == 'NOUN' and token.text != 'back':
            title_list.append(token.text)
    return title_list
