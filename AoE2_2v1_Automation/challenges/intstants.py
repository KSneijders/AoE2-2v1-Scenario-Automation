import random
from typing import Dict

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.disable_structure import Disables
from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.helper import get_player_tc
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.object_support import Civilization
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import TechnologyState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player import Player
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


def delete_starting_vills(scenario: AoE2DEScenario, player: Player, challenge: Dict, *args):
    tm, um = scenario.trigger_manager, scenario.unit_manager
    vills = um.filter_units_by_const(
        unit_consts=[UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID],
        player_list=[player.player_id]
    )
    random.shuffle(vills)
    vills = vills[:int(challenge['selectedOption'])]
    trigger = tm.add_trigger(f"[p{player.player_id}] Delete starting vills ({len(vills)})")
    trigger.new_effect.kill_object(selected_object_ids=[vill.reference_id for vill in vills])


def delete_starting_scout(scenario: AoE2DEScenario, player: Player, *args):
    tm, um = scenario.trigger_manager, scenario.unit_manager
    scout = um.filter_units_by_const(
        unit_consts=[UnitInfo.SCOUT_CAVALRY.ID, UnitInfo.EAGLE_SCOUT.ID],
        player_list=[player.player_id]
    )[0]
    trigger = tm.add_trigger(f"[p{player.player_id}] Delete starting scout")
    trigger.new_effect.kill_object(selected_object_ids=[scout.reference_id])


def instant_barracks(scenario: AoE2DEScenario, player: Player, *args):
    mm = scenario.map_manager

    dark_age_buildings = [
        BuildingInfo.DOCK.ID,
        BuildingInfo.OUTPOST.ID,
        BuildingInfo.PALISADE_WALL.ID,
        BuildingInfo.PALISADE_GATE.ID,
        BuildingInfo.HOUSE.ID if player.civilization != Civilization.HUNS else -1,
        BuildingInfo.MINING_CAMP.ID,
        BuildingInfo.LUMBER_CAMP.ID,
        BuildingInfo.MILL.ID,
        BuildingInfo.FARM.ID,
    ]

    trigger = Trigger(f"Enable buildings after instant_barracks (p{player.player_id}")
    trigger.new_condition.objects_in_area(
        quantity=1,
        object_list=BuildingInfo.BARRACKS.ID,
        source_player=player.player_id,
        area_x1=0, area_y1=0, area_x2=mm.map_size - 1, area_y2=mm.map_size - 1,
    )
    for building in dark_age_buildings:
        trigger.new_effect.enable_disable_object(
            object_list_unit_id=building,
            source_player=player.player_id,
            enabled=True
        )

    Disables.get_instance().add_other_disables(dark_age_buildings, player.player_id, 'buildings')
    Disables.get_instance().add_trigger(player.player_id, trigger)


def instant_loom(scenario: AoE2DEScenario, player: Player, *args):
    tm, um = scenario.trigger_manager, scenario.unit_manager
    tc = get_player_tc(um, player.player_id)

    player.disabled_units.extend([UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID])
    enable_vils_trigger = tm.add_trigger(f"[p{player.player_id}] Allow villager crafting", looping=True)
    enable_vils_trigger.new_condition.technology_state(
        quantity=TechnologyState.RESEARCHING,
        source_player=player.player_id,
        technology=TechInfo.LOOM.ID,
    )
    enable_vils_trigger.new_effect.enable_disable_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=player.player_id,
        enabled=True
    )
    enable_vils_trigger.new_effect.enable_disable_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=player.player_id,
        enabled=True
    )

    disable_vills_trigger = tm.add_trigger(f"[p{player.player_id}] Revert allow villager crafting", enabled=False, looping=True)
    disable_vills_trigger.new_condition.technology_state(
        quantity=TechnologyState.RESEARCHING,
        source_player=player.player_id,
        technology=TechInfo.LOOM.ID,
        inverted=True,
    )
    disable_vills_trigger.new_condition.technology_state(
        quantity=TechnologyState.READY,
        source_player=player.player_id,
        technology=TechInfo.LOOM.ID,
    )
    disable_vills_trigger.new_effect.enable_disable_object(
        object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
        source_player=player.player_id,
        enabled=False
    )
    disable_vills_trigger.new_effect.enable_disable_object(
        object_list_unit_id=UnitInfo.VILLAGER_FEMALE.ID,
        source_player=player.player_id,
        enabled=False
    )
    disable_vills_trigger.new_effect.change_ownership(
        selected_object_ids=tc.reference_id,
        target_player=PlayerId.GAIA,
    )
    disable_vills_trigger.new_effect.change_ownership(
        selected_object_ids=tc.reference_id,
        target_player=player.player_id,
    )
    disable_vills_trigger.new_effect.deactivate_trigger(trigger_id=disable_vills_trigger.trigger_id)
    enable_vils_trigger.new_effect.activate_trigger(trigger_id=disable_vills_trigger.trigger_id)
