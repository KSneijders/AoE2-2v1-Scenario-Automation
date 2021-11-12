from typing import Dict

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.helper import get_player_tc
from AoE2ScenarioParser.datasets.trigger_lists import ObjectClass
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player import Player
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


def max_vills_in_dark_age(scenario: AoE2DEScenario, player: Player, challenge: Dict, *args):
    tm, um = scenario.trigger_manager, scenario.unit_manager

    genders = [UnitInfo.VILLAGER_MALE, UnitInfo.VILLAGER_FEMALE]
    tc = get_player_tc(um, player.player_id)
    max_vil_count = int(challenge['selectedOption'])

    disable_trigger = tm.add_trigger(f"[p{player.player_id}] Disable vills when max reached", looping=True)
    disable_trigger.new_condition.own_objects(
        quantity=max_vil_count,
        object_group=ObjectClass.CIVILIAN
    )
    for gender in genders:
        disable_trigger.new_effect.enable_disable_object(
            object_list_unit_id=gender.ID,
            source_player=player.player_id,
            enabled=False
        )
    disable_trigger.new_effect.task_object(
        selected_object_ids=[tc.reference_id]
    )

    enable_trigger = tm.add_trigger(f"[p{player.player_id}] Enable vills when below max", enabled=False, looping=True)
    enable_trigger.new_condition.own_fewer_objects(
        quantity=max_vil_count - 1,
        object_group=ObjectClass.CIVILIAN
    )
    for gender in genders:
        enable_trigger.new_effect.enable_disable_object(
            object_list_unit_id=gender.ID,
            source_player=player.player_id,
            enabled=True
        )

    disable_trigger.new_effect.deactivate_trigger(trigger_id=disable_trigger.trigger_id)
    disable_trigger.new_effect.activate_trigger(trigger_id=enable_trigger.trigger_id)
    enable_trigger.new_effect.deactivate_trigger(trigger_id=enable_trigger.trigger_id)
    enable_trigger.new_effect.activate_trigger(trigger_id=disable_trigger.trigger_id)
