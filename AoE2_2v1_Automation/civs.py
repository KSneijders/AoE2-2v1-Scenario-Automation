from AoE2ScenarioParser.datasets.object_support import Civilization


def get_civ(profile) -> Civilization:
    civs = profile['civs']
    return Civilization[civs['options'][civs['choiceIndex']].upper()]
