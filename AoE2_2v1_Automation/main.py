import base64
import json
import random
from typing import Dict, List, Set

from bidict import bidict

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation import extra_disables
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.civs import get_civ
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.encoded_strings import base64_encoded
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.extra_disables import ExtraInstantDisables
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.intstants import handle_instants
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.simple_disables import handle_simple_disables
from AoE2ScenarioParser.datasets.players import PlayerId, ColorId
from AoE2ScenarioParser.helper.pretty_format import pretty_format_list
from AoE2ScenarioParser.local_config import folder_2v1, folder_de
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

filename = f"arabia"
num = random.randint(1, 10)
scenario = AoE2DEScenario.from_file(f"{folder_2v1}{filename}{num}.aoe2scenario")
tm, um, mm, xm, pm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
                     scenario.player_manager

for p in pm.players:
    p.color = ColorId.GRAY

players_nums = list(range(1, len(base64_encoded) + 1))
# random.shuffle(players_nums)
player_map: bidict = bidict()
"""Maps Player ID to their colour"""
extra_disables.extra_instant_disables = {k: [] for k in players_nums}
"""Used for challenges. Keeps track of what should get disabled at the start but can also be re-enabled afterwards"""

colour_map: Dict = {
    'blue': PlayerId.ONE,
    'red': PlayerId.TWO,
    'green': PlayerId.THREE,
    'yellow': PlayerId.FOUR,
    'cyan': PlayerId.FIVE,
    'purple': PlayerId.SIX,
    'grey': PlayerId.SEVEN,
    'orange': PlayerId.EIGHT,
}

defendants, challengers = [], []


for index, encoded_settings in enumerate(base64_encoded):
    profile_settings = json.loads(base64.b64decode(encoded_settings))
    civ = get_civ(profile_settings)

    players: Dict[str, Dict[str, str]] = profile_settings['players']
    this_player, solo_player, this_side = {}, {}, ""
    for profile in players.values():
        if profile['id'] == "default":
            this_player = profile
            this_side = profile['side']
            if this_side == "Defendant":
                defendants.append(profile['colour'])
            else:
                challengers.append(profile['colour'])
            continue
        if profile['side'] == "Defendant":
            solo_player = profile
            continue

    player_map[players_nums[index]] = colour_map[this_player['colour'].lower()]
    player_object = scenario.player_manager.players[players_nums[index]]
    player_object.color = ColorId.from_player_id(player_map[players_nums[index]])

    # Civs don't work...
    # player_object.civilization = civ
    # player_object.lock_civ = True

    if this_side == "Challenger":
        ids: List[str] = [c['id'] for c in profile_settings['challenges']['collection']]

        # SIMPLE DISABLES HAS TO BE EXECUTED FIRST!
        # For keeping track of what was already disabled. So triggers don't re-enable stuff after a challenge
        handle_simple_disables(scenario, player_object, ids)

        handle_instants(scenario, player_object, ids)
    else:
        ...


# Todo: Move to extra_disables file (or just rework entirely ???)
disables: List[ExtraInstantDisables]
for player_id, disables in extra_disables.extra_instant_disables.items():
    for disable in disables:
        trigger = tm.add_trigger('Handle :)')
        trigger.conditions.extend(disable.conditions)
        disabled = getattr(pm.players[player_id], f"disabled_{disable.type_}")
        for e in disable.disable_ids:
            if e not in disabled:
                disabled.append(e)
                trigger.new_effect.enable_disable_object(object_list_unit_id=e, source_player=player_id, enabled=True)


challengers = list(map(lambda colour: player_map.inverse[colour_map[colour.lower()]], challengers))
defendants = list(map(lambda colour: player_map.inverse[colour_map[colour.lower()]], defendants))

pm.create_diplomacy_teams(challengers, defendants)
pm.set_default_starting_resources()

scenario.write_to_file(f"{folder_de}!2v1-{filename}.aoe2scenario")

print(pretty_format_list([p for p in pm.players[1:4]]))