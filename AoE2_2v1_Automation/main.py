import base64
import json
import random
from typing import Dict

from bidict import bidict

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.civs import get_civ
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.disable_other_resources import no_hunt, \
    no_forage_bush, no_stone, no_mills, send_sheep_to_solo
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.disable_structure import Disables
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.encoded_strings import base64_encoded
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.intstants import instant_barracks, \
    instant_loom, delete_starting_scout, delete_starting_vills
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.permanent_disables import \
    handle_permanent_disables
from AoE2ScenarioParser.datasets.players import PlayerId, ColorId
from AoE2ScenarioParser.local_config import folder_2v1, folder_de
from AoE2ScenarioParser.objects.data_objects.player import Player
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

filename = f"arabia"
num = random.randint(1, 10)
scenario = AoE2DEScenario.from_file(f"{folder_2v1}{filename}{num}.aoe2scenario")
tm, um, mm, xm, pm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
                     scenario.player_manager

for p in pm.players:
    p.color = ColorId.GRAY

randomized_player_ids = list(range(1, len(base64_encoded) + 1))
# random.shuffle(randomized_player_ids)
player_colour_map: bidict = bidict()
"""Maps Player ID to their colour"""

colour_to_player_id: Dict = {
    'blue': PlayerId.ONE,
    'red': PlayerId.TWO,
    'green': PlayerId.THREE,
    'yellow': PlayerId.FOUR,
    'cyan': PlayerId.FIVE,
    'purple': PlayerId.SIX,
    'grey': PlayerId.SEVEN,
    'orange': PlayerId.EIGHT,
}

challenges = {
    'instant_loom': instant_loom,
    'instant_barracks': instant_barracks,
    'delete_starting_scout': delete_starting_scout,
    'delete_starting_vills': delete_starting_vills,
    'no_forage_bush': no_forage_bush,
    'no_stone': no_stone,
    'no_hunt': no_hunt,
    'no_mills': no_mills,
    'send_sheep_to_solo': send_sheep_to_solo,
}

decoded_profiles = list(map(lambda e: json.loads(base64.b64decode(e)), base64_encoded))

defendants, challengers = [], []
for index, profile_settings in enumerate(decoded_profiles):
    civ = get_civ(profile_settings)

    players: Dict[str, Dict[str, str]] = profile_settings['players']
    current_player, current_side = {}, ""

    for profile in players.values():
        if profile['id'] != "default":
            continue

        current_player = profile
        current_side = profile['side']

        if current_side == "Defendant":
            defendants.append(profile['colour'])
        else:
            challengers.append(profile['colour'])

    randomized_id = randomized_player_ids[index]
    colour_id = colour_to_player_id[current_player['colour'].lower()]

    player_object: Player = scenario.player_manager.players[randomized_id]
    player_object.color = ColorId.from_player_id(colour_id)
    player_colour_map[randomized_id] = colour_id

    # Civs don't work...
    player_object.civilization = civ
    # player_object.lock_civ = True

# print(player_colour_map)

#
# print(challengers)
# print(defendants)
#
# for challenger in challengers:
#     print(challenger)
#     exit()
    if current_side == "Challenger":
        ids: Dict[str, Dict] = {c['id']: c for c in profile_settings['challenges']['collection']}
        handle_permanent_disables(player_object, ids)

        for id_ in ids.keys():
            if id_ in challenges:
                challenges[id_](scenario, player_object, ids[id_])
        challenges['send_sheep_to_solo'](scenario, player_object)
        ...
    else:
        pass

challengers = list(map(lambda colour: player_colour_map.inverse[colour_to_player_id[colour.lower()]], challengers))
defendants = list(map(lambda colour: player_colour_map.inverse[colour_to_player_id[colour.lower()]], defendants))


disables_object = Disables.get_instance()
for disables in [disables_object.initial_disables, disables_object.other_disables]:
    for player, disable_dict in disables.items():
        for type_, disable_list_ in disable_dict.items():
            getattr(pm.players[player], f"disabled_{type_}").extend(disable_list_)

tm.import_triggers(disables_object.triggers)
pm.create_diplomacy_teams(challengers, defendants)

scenario.write_to_file(f"{folder_de}!2v1-{filename}.aoe2scenario")
