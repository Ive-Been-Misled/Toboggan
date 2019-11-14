"""Stateless NLP utility functions"""
from os import environ
from typing import Iterator
from toboggan.noun_key import NounKey
import spacy
from pattern.text.en import singularize
from .setting import setting_instance


if 'FAKE_GPT2' in environ:
    from .gpt2_fake import GPT2
else:
    from .gpt2 import GPT2

_NLP = spacy.load('en_core_web_lg')

def describe_location(location: str) -> str:
    """Given a location, returns a description of location"""
    prompt = f"""\
    You are in the world of {setting_instance.universe_setting}. You are in {location}. You look around. You see
    """
    description = 'You see'

    current_length = 0
    min_length = 42

    for token in GPT2.sample_sequence(prompt):
        description += token
        current_length += 1
        print(f"DEBUG: {token}")
        if current_length >= min_length and token in ('.', '?', '#', '"', '<|endoftext|>'):
            break
    description = description.replace('<|endoftext|>', ' ')
    return description

def describe_item(item: str) -> str:
    prompt = f"You have a {item}. Here is a description of the {item}:"

    description = f''
    
    current_length = 0
    min_length = 42

    for token in GPT2.sample_sequence(prompt):
        description += token
        current_length += 1
        print(f"DEBUG: {token}")
        if current_length >= min_length and token in ('.', '?', '#', '"', '<|endoftext|>'):
            break

    return description

def describe_character(character: str) -> str:
    prompt = f"You encounter a {character}. Here is a description of the {character}:"

    description = f'<center>[{character.capitalize()}]</center>'
    
    current_length = 0
    min_length = 42

    for token in GPT2.sample_sequence(prompt):
        description += token
        current_length += 1
        print(f"DEBUG: {token}")
        if current_length >= min_length and token in ('.', '?', '#', '"', '<|endoftext|>'):
            break

    return description

def noun_chunks(text: str) -> Iterator[str]:
    """Given some text, return the noun chunks"""
    doc = _NLP(text)
    return doc.noun_chunks


def room_noun_generator(text: str) -> dict:
    """Given a description, return a list of mentioned nouns and their type"""
    doc = _NLP(text)
    title_list = {noun:[] for noun in NounKey}
    seen_nouns = set()
    for token in doc.noun_chunks:
        for word in _NLP(token.text):
            singular_word = singularize(word.text).lower()
            if (word.pos_ in ('NOUN', 'PROPN') and
                    word.dep_ == 'ROOT' and
                    word.text != 'back' and
                    singular_word not in seen_nouns and
                    token.text.find('no ') != 0):
                noun = noun_classifier(word.text)
                title_list[noun].append(token.text)
                seen_nouns.add(singular_word)

    return title_list

def tokenize(text: str):
    doc = _NLP(text)
    return doc

def noun_classifier(word: str) -> NounKey:
    """Determines what type of noun a passed noun is."""
    tokens = _NLP(' '.join([' '.join(noun.value) for noun in NounKey]))
    word_token = _NLP(word)
    max_score = 0
    best_class = None
    for token in tokens:
        temp_score = token.similarity(word_token)
        if temp_score > max_score:
            max_score = temp_score
            best_class = token.text
    return NounKey.find_name(best_class)
