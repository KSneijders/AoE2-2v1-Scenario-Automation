import base64
import json
import random
from typing import Dict

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.encoded_strings import base64_encoded
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.simple_disables import simple_disables
from AoE2ScenarioParser.datasets.players import PlayerColorId, PlayerId, ColorId
from AoE2ScenarioParser.local_config import folder_2v1, folder_de
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

filename = f"arabia3"  # 3{random.randint(1, 10)}
scenario = AoE2DEScenario.from_file(f"{folder_2v1}{filename}.aoe2scenario")
tm, um, mm, xm, pm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
                     scenario.player_manager

for p in pm.players:
    p.color = ColorId.GRAY

players_nums = list(range(1, len(base64_encoded) + 1))
random.shuffle(players_nums)
player_map: Dict = {k: -1 for k in players_nums}

color_map = {
    'blue': PlayerId.ONE,
    'red': PlayerId.TWO,
    'green': PlayerId.THREE,
    'yellow': PlayerId.FOUR,
    'cyan': PlayerId.FIVE,
    'purple': PlayerId.SIX,
    'grey': PlayerId.SEVEN,
    'orange': PlayerId.EIGHT,
}

for index, encoded_settings in enumerate(base64_encoded):
    profile_settings = json.loads(base64.b64decode(encoded_settings))
    players: Dict[str, Dict[str, str]] = profile_settings['players']
    this_player, solo_player, this_side = {}, {}, ""
    for profile in players.values():
        if profile['id'] == "default":
            this_player = profile
            this_side = profile['side']
            continue
        if profile['side'] == "Defendant":
            solo_player = profile
            continue

    player_map[players_nums[index]] = color_map[this_player['colour'].lower()]
    player_object = scenario.player_manager.players[players_nums[index]]
    player_object.color = ColorId.from_player_id(player_map[players_nums[index]])

    if this_side == "Challenger":
        ids = [c['id'] for c in profile_settings['challenges']['collection']]
        for id_ in ids:
            if id_ in simple_disables.keys():
                e = simple_disables[id_]
                for type_, list_or_item in e.items():
                    if isinstance(list_or_item, list):
                        getattr(player_object, f"disabled_{type_}").extend(list_or_item)
                    else:
                        getattr(player_object, f"disabled_{type_}").append(list_or_item)
    print(player_object)

scenario.write_to_file(f"{folder_de}!2v1-{filename}.aoe2scenario")
