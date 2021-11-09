from typing import List

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.extra_disables import ExtraInstantDisables
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.conditions import ConditionId
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import TechnologyState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.condition import Condition
from AoE2ScenarioParser.objects.data_objects.player import Player
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


def handle_instants(scenario: AoE2DEScenario, player: Player, ids: List[str]):
    for id_ in ids:
        if id_ in instants:
            instants[id_](scenario, player)


def delete_starting_scout(scenario: AoE2DEScenario, player: Player):
    tm, um = scenario.trigger_manager, scenario.unit_manager
    scout = um.filter_units_by_const(
        unit_consts=[UnitInfo.SCOUT_CAVALRY.ID, UnitInfo.EAGLE_SCOUT.ID],
        player_list=[player.player_id]
    )[0]
    trigger = tm.add_trigger(f"Delete starting scout p{player.player_id}")
    trigger.new_effect.kill_object(selected_object_ids=[scout.reference_id])


def instant_barracks(scenario: AoE2DEScenario, player: Player):
    dark_age_buildings = [
        BuildingInfo.DOCK.ID,
        BuildingInfo.OUTPOST.ID,
        BuildingInfo.PALISADE_WALL.ID,
        BuildingInfo.PALISADE_GATE.ID,
        BuildingInfo.HOUSE.ID,          # Civ based
        BuildingInfo.MINING_CAMP.ID,
        BuildingInfo.LUMBER_CAMP.ID,
        BuildingInfo.FOLWARK.ID,        # Civ based
        BuildingInfo.MILL.ID,           # Civ based
        BuildingInfo.FARM.ID,
    ]

    condition = Trigger("_").new_condition.objects_in_area(
        object_type=ConditionId.OBJECTS_IN_AREA,
        quantity=1,
        object_list=BuildingInfo.BARRACKS.ID,
        source_player=player.player_id,
        area_x1=-1, area_y1=-1, area_x2=-1, area_y2=-1,
    )

    ExtraInstantDisables('buildings', dark_age_buildings, [condition], player=player.player_id)


def instant_loom(scenario: AoE2DEScenario, player: Player):
    tm, um = scenario.trigger_manager, scenario.unit_manager

    tm.add_trigger('').new_condition.objects_in_area(
    )

    tc = um.filter_units_by_const(unit_consts=[BuildingInfo.TOWN_CENTER.ID], player_list=[player.player_id])[0]

    player.disabled_units.extend([UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID])
    enable_vils_trigger = tm.add_trigger("Allow villager crafting", looping=True)
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

    disable_vills_trigger = tm.add_trigger("Revert allow villager crafting", enabled=False, looping=True)
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


instants = {
    'instant_loom': instant_loom,
    'instant_barracks': instant_barracks,
    'delete_starting_scout': delete_starting_scout
}
