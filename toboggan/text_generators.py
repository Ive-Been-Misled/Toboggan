from .gpt2 import GPT2


def describe_location(location: str) -> str:
    prompt = f"""\
    You are in {location}. You look around. You see
    """
    description = 'You see'

    for token in GPT2.sample_sequence(prompt):
        if token == '\n':
            break
        description += token

    return description

def room_title_generator(text: str) -> list:
    pass