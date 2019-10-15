from .gpt2 import GPT2
import spacy

def describe_location(location: str) -> str:
    prompt = f"""\
    You are in {location}. You look around. You see
    """
    description = 'You see'


    for token in GPT2.sample_sequence(prompt):
        description += token
        if token == '.':
            break

    return description

def room_title_generator(text: str) -> list:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    title_list = []
    for token in doc:
        if token.pos_ == 'NOUN':
            title_list.append(token.text)
    return title_list