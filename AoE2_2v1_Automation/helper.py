from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.objects.managers.de.unit_manager_de import UnitManagerDE


def get_player_tc(um: UnitManagerDE, player):
    return um.filter_units_by_const([BuildingInfo.TOWN_CENTER.ID], player_list=[player.player_id])[0]
