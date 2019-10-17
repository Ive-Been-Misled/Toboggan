from .gpt2 import GPT2
import spacy

def describe_location(location: str) -> str:
    prompt = f"""\
    You are in {location}. You look around. You see
    """
    description = 'You see'

    current_length = 0
    min_length =  20

    for token in GPT2.sample_sequence(prompt):
        description += token
        current_length += 1
        if current_length >= min_length and token == '.':
            break

    return description

def room_title_generator(text: str) -> list:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    title_list = []
    for token in doc:
        if token.pos_ == 'NOUN' and token.text != 'back':
            title_list.append(token.text)
    return title_list
