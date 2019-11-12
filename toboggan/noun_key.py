from enum import Enum
class NounKey(Enum):
    LOCATIONS = ['place']
    CHARACTERS = ['character']
    FOOD_ITEMS = ['food', 'potion']
    WEAPON_ITEMS = ['weapon']
    ARMOR_ITEMS = ['armor']
    MISC = ['']

    @classmethod
    def find_name(cls, noun: str):
        for noun_class in NounKey:
            if noun in noun_class.value:
                return noun_class
        return NounKey.MISC
