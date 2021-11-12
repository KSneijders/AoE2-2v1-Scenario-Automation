from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.intstants import instant_loom, \
    instant_barracks, delete_starting_scout, delete_starting_vills
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.other import max_vills_in_dark_age
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.challenges.resources import no_forage_bush, \
    no_stone, no_hunt, no_mills, send_sheep_to_solo, no_sheep

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
    'no_sheep': no_sheep,
    'max_vills_in_dark_age': max_vills_in_dark_age,
}
