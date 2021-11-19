from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.objects.managers.de.unit_manager_de import UnitManagerDE


def get_player_tc(um: UnitManagerDE, player_id: int):
    return um.filter_units_by_const([BuildingInfo.TOWN_CENTER.ID], player_list=[player_id])[0]


def entire_map(scenario):
    mm = scenario.map_manager
    return {
        'area_x1': 0,
        'area_y1': 0,
        'area_x2': mm.map_size - 1,
        'area_y2': mm.map_size - 1
    }


def deep_get(d, keys):
    if not keys or d is None:
        return d
    return deep_get(d.get(keys[0]), keys[1:])
