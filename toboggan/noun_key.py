from enum import Enum
class NounKey(Enum):
    CHARACTERS = ['character', 'goblin', 'man', 'dog', 'giraffe', 'boy', 'monster', 'brother', 'mother']
    FOOD_ITEMS = ['apple', 'banana', 'burger', 'potion', 'drink']
    WEAPON_ITEMS = ['sword', 'box', 'axe', 'key']
    ARMOR_ITEMS = ['chestplate', 'hat', 'pants']
    LOCATIONS = ['forest','city','room','building','alley','place', 'door', 'window']

    #MISC_TIME = ['day', 'time', 'hour', 'time']
   #MISC_BODY = ['hair', 'finger', 'leg', 'arm', 'grin', 'smile']
    #MISC_EMOTION = ['fright', 'emotion', 'pride']
    #MISC_COST = ['choice', 'cost', 'increment']

    #LOCATIONS = ['place']
    #CHARACTERS = ['character']
    #FOOD_ITEMS = ['food', 'potion']
    #WEAPON_ITEMS = ['weapon']
    #ARMOR_ITEMS = ['armor']
    MISC = ['']

    @classmethod
    def find_name(cls, noun: str):
        for noun_class in NounKey:
            if noun in noun_class.value:
                return noun_class
        return NounKey.MISC
