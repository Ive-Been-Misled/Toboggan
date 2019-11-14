from enum import Enum
class NounKey(Enum):
    CHARACTERS = [
        'character',
        'goblin',
        'man',
        'dog',
        'giraffe',
        'boy',
        'monster',
        'brother',
        'mother',
        'people',
        'horror',
        'slayer',
        'elf',
        'spirit',
        'ghost'
        ]

    FOOD_ITEMS = [
        'apple',
        'banana',
        'burger',
        'potion',
        'drink',
        'heart',
        'carcasses'
        ]

    WEAPON_ITEMS = [
        'sword',
        'box',
        'axe',
        'key',
        'flame',
        'fire'
        ]

    ARMOR_ITEMS = [
        'chestplate',
        'hat',
        'pants',
        'helmet'
        ]

    LOCATIONS = [
        'forest',
        'city',
        'room',
        'building',
        'alley',
        'place',
        'door',
        'window',
        'mines',
        'vaults',
        'dungeon',
        'halls',
        'lairs',
        'structure',
        'road'
        ]

    MISC = [
        'time',
        'day',
        'emotion',
        'thought',
        'shapes',
        'sizes',
        'set',
        'alot',
        'lot',
        'eye',
        'industry'
        ]

    #MISC_TIME = ['day', 'time', 'hour', 'time']
    #MISC_BODY = ['hair', 'finger', 'leg', 'arm', 'grin', 'smile']
    #MISC_EMOTION = ['fright', 'emotion', 'pride']
    #MISC_COST = ['choice', 'cost', 'increment']

    @classmethod
    def find_name(cls, noun: str):
        for noun_class in NounKey:
            if noun in noun_class.value:
                return noun_class
        return NounKey.MISC
