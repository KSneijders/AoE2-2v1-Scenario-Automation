from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.objects.managers.de.unit_manager_de import UnitManagerDE
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


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


def set_allied_starting_tc_explored(scenario: AoE2DEScenario, teams):
    tm, um = scenario.trigger_manager, scenario.unit_manager
    remove_map_revealers = tm.add_trigger("Remove map revealers")
    for team in teams:
        for player in team:
            remove_map_revealers.new_effect.remove_object(
                object_list_unit_id=OtherInfo.MAP_REVEALER.ID, source_player=player, **entire_map(scenario),
            )
            for player2 in team:
                if player == player2:
                    continue
                tc = get_player_tc(um, player2)
                um.add_unit(player=player, unit_const=OtherInfo.MAP_REVEALER.ID, x=tc.x - 1, y=tc.y)
                um.add_unit(player=player, unit_const=OtherInfo.MAP_REVEALER.ID, x=tc.x, y=tc.y)
                um.add_unit(player=player, unit_const=OtherInfo.MAP_REVEALER.ID, x=tc.x, y=tc.y - 1)
                um.add_unit(player=player, unit_const=OtherInfo.MAP_REVEALER.ID, x=tc.x, y=tc.y)
