from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.intstants import instant_loom, \
    instant_barracks, delete_starting_scout, delete_starting_vills
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.other import max_vills_in_dark_age, \
    no_extra_tcs, kill_vills_when_housed, max_pop, no_relics, delay_age_until_solo_aged, kill_vills_per_age
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.resources import no_forage_bush, \
    no_stone, no_hunt, no_mills, send_sheep_to_solo, no_sheep
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.techs import \
    no_current_age_blacksmith_techs, get_all_blacksmith_techs, get_murder_holes, get_heresy

challenge_map = {
    'instant_loom': instant_loom,
    'instant_barracks': instant_barracks,
    'delete_starting_scout': delete_starting_scout,
    'delete_starting_vills': delete_starting_vills,
    'no_forage_bush': no_forage_bush,
    'no_stone': no_stone,
    'no_hunt': no_hunt,
    'no_mills': no_mills,
    'send_sheep_to_solo': send_sheep_to_solo,
    'no_sheep': no_sheep,
    'max_vills_in_dark_age': max_vills_in_dark_age,
    'no_extra_tcs': no_extra_tcs,
    'kill_vills_when_housed': kill_vills_when_housed,
    'max_pop': max_pop,
    'no_current_age_blacksmith_techs': no_current_age_blacksmith_techs,
    'no_relics': no_relics,
    'get_all_blacksmith_techs': get_all_blacksmith_techs,
    'get_murder_holes': get_murder_holes,
    'get_heresy': get_heresy,
    'delay_age_until_solo_aged': delay_age_until_solo_aged,
    # 'kill_vills_per_age': kill_vills_per_age,
}

challenge_dependencies = {
    'kill_vills_when_housed': [
        'max_pop'
    ],
    'kill_vills_per_age': [
        'max_pop'
    ],
}
