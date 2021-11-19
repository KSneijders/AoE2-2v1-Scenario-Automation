import base64
import json
import random
from typing import Dict

from AoE2ScenarioParser.datasets.object_support import StartingAge, Civilization
from AoE2ScenarioParser.datasets.players import ColorId
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player.player import Player
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from bidict import bidict

from src.challenges.challenges import challenge_map, challenge_dependencies
from src.challenges.permanent_disables import handle_permanent_disables
from src.civs import get_civ
from src.data import colour_to_player_id
from src.disable_structure import Disables
from src.encoded_strings import base64_encoded
from src.local_config import folder_2v1, folder_de

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

defendants, challengers = [], []
decoded_profiles = list(map(lambda e: json.loads(base64.b64decode(e)), base64_encoded))
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
    player_object.starting_age = StartingAge.DARK_AGE
    player_colour_map[randomized_id] = colour_id

    # Civs don't work...
    player_object.civilization = civ
    # player_object.lock_civ = True

challengers = list(map(lambda colour: player_colour_map.inverse[colour_to_player_id[colour.lower()]], challengers))
defendants = list(map(lambda colour: player_colour_map.inverse[colour_to_player_id[colour.lower()]], defendants))

for player_id in challengers + defendants:
    player_object = pm.players[player_id]
    if player_object.civilization in [Civilization.AZTECS, Civilization.INCAS, Civilization.MAYANS]:
        um.filter_units_by_const(
            unit_consts=[UnitInfo.SCOUT_CAVALRY.ID],
            player_list=[player_object.player_id],
        )[0].unit_const = UnitInfo.EAGLE_SCOUT.ID

for challenger_id in challengers:
    player_object = pm.players[challenger_id]

    profile = decoded_profiles[randomized_player_ids.index(challenger_id)]
    ids: Dict[str, Dict] = {c['id']: c for c in profile['challenges']['collection']}

    handle_permanent_disables(player_object, ids)

    for id_ in ids.keys():
        if id_ in challenge_map:
            dependencies = {c_id: ids[c_id] for c_id in challenge_dependencies.get(id_, []) if c_id in ids}
            challenge_map[id_](
                scenario,
                player_object,
                challenge=ids[id_],
                players_sides={
                    'challenges': challengers,
                    'defendants': defendants
                },
                dependencies=dependencies
            )

disables_object = Disables.get_instance()
for disables in [disables_object.initial_disables, disables_object.other_disables]:
    for player, disable_dict in disables.items():
        for type_, disable_list_ in disable_dict.items():
            getattr(pm.players[player], f"disabled_{type_}").extend(disable_list_)
disables_object.combine_age_requirements(scenario)

tm.import_triggers(disables_object.triggers)
pm.set_diplomacy_teams(challengers, defendants)

scenario.write_to_file(f"{folder_de}!2v1-{filename}.aoe2scenario")
