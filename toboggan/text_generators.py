from .gpt2 import GPT2
import spacy

def describe_location(location: str) -> str:
    prompt = f"""\
    You are in {location}. You look around. You see
    """
    description = 'You see'

    current_length = 0
    min_length =  42

    for token in GPT2.sample_sequence(prompt):
        description += token
        current_length += 1
        print(f"DEBUG: {token}")
        if current_length >= min_length and (token == '.' or token == '?' or
                token == '#' or token == '"'):
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
