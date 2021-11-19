import random

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, ObjectClass
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player.player import Player
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from AoE2_2v1_Automation.helper import get_player_tc, entire_map


def no_mills(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm, um, mm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager
    tc = get_player_tc(um, player.player_id)

    disable_mill = tm.add_trigger(f"[p{player.player_id}] Disable mill after 1 at tc", looping=True)
    disable_mill.new_condition.objects_in_area(
        quantity=1,
        object_list=BuildingInfo.MILL.ID,
        source_player=player.player_id,
        area_x1=int(tc.x - 3), area_y1=int(tc.y - 3), area_x2=int(tc.x + 3), area_y2=int(tc.y + 3),
    )
    disable_mill.new_effect.enable_disable_object(
        object_list_unit_id=BuildingInfo.MILL.ID,
        source_player=player.player_id,
        enabled=False
    )

    enable_mill = tm.add_trigger(f"[p{player.player_id}] Re-enable mill", looping=True)
    enable_mill.new_condition.own_fewer_objects(
        quantity=0,
        object_list=BuildingInfo.MILL.ID,
        source_player=player.player_id,
        **entire_map(scenario)
    )
    enable_mill.new_effect.enable_disable_object(
        object_list_unit_id=BuildingInfo.MILL.ID,
        source_player=player.player_id,
        enabled=True
    )

    remove_mills = tm.add_trigger(f"[p{player.player_id}] Kill all mills", looping=True)
    remove_mills.new_condition.own_objects(
        quantity=1,
        object_list=BuildingInfo.MILL.ID,
        source_player=player.player_id
    )
    remove_mills.new_condition.objects_in_area(
        quantity=1,
        object_list=BuildingInfo.MILL.ID,
        source_player=player.player_id,
        area_x1=int(tc.x - 3), area_y1=int(tc.y - 3), area_x2=int(tc.x + 3), area_y2=int(tc.y + 3),
        inverted=True,
    )
    remove_mills.new_effect.kill_object(
        object_list_unit_id=BuildingInfo.MILL.ID,
        source_player=player.player_id,
        **entire_map(scenario)
    )


def send_sheep_to_solo(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm, um, mm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager
    players_sides = kwargs['players_sides']
    disable_resource_collection(scenario, player, "shepherd", "herd herdables")

    defendant_id = random.choice(players_sides['defendants'])
    tc = get_player_tc(um, player.player_id)
    defendants_tc = get_player_tc(um, defendant_id)

    herdables = um.filter_units_by_const(unit_consts=[
        UnitInfo.SHEEP.ID, UnitInfo.GOAT.ID, UnitInfo.TURKEY.ID, UnitInfo.GOOSE.ID, UnitInfo.PIG.ID,
        UnitInfo.COW_A.ID, UnitInfo.COW_B.ID, UnitInfo.COW_C.ID, UnitInfo.COW_D.ID,
    ], player_list=[PlayerId.GAIA])
    herdables = um.get_units_in_area(
        x1=int(tc.x - 32), y1=int(tc.y - 32),
        x2=int(tc.x + 32), y2=int(tc.y + 32),
        unit_list=herdables
    )

    trigger = tm.add_trigger("Disable herdable selection")
    trigger.new_effect.disable_object_selection(selected_object_ids=[herdable.reference_id for herdable in herdables])

    trigger = tm.add_trigger("Disable herdable selection", looping=True)
    trigger.new_condition.timer(timer=3)
    trigger.new_effect.task_object(
        object_group=ObjectClass.LIVESTOCK,
        source_player=player.player_id,
        location_x=int(defendants_tc.x), location_y=int(defendants_tc.y),
        **entire_map(scenario)
    )


def no_sheep(scenario: AoE2DEScenario, player: Player, **kwargs):
    disable_resource_collection(scenario, player, "shepherd", "herd herdables")


def no_forage_bush(scenario: AoE2DEScenario, player: Player, **kwargs):
    disable_resource_collection(scenario, player, "forager", "forage berries")


def no_stone(scenario: AoE2DEScenario, player: Player, **kwargs):
    disable_resource_collection(scenario, player, "stone_miner", "mine stone")


def no_hunt(scenario: AoE2DEScenario, player: Player, **kwargs):
    disable_resource_collection(scenario, player, "hunter", "hunt")


def disable_resource_collection(scenario: AoE2DEScenario, player: Player, name: str, action: str = ""):
    tm, um, mm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager
    trigger = tm.add_trigger(f"[p{player.player_id}] Warn when {name.replace('_', ' ')} villager", looping=True)
    genders = ['FEMALE', 'MALE']
    trigger.new_condition.own_objects(
        quantity=1,
        object_list=UnitInfo[f"VILLAGER_MALE_{name.upper()}"].ID,
        source_player=player.player_id
    )
    trigger.new_effect.send_chat(
        source_player=player.player_id,
        message=f"<RED>"
                f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "
                f"You are not allowed to {action or f'have {name} vills'} "
                f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "
    )
    trigger.new_effect.stop_object(
        object_list_unit_id=UnitInfo[f"VILLAGER_MALE_{name.upper()}"].ID,
        source_player=player.player_id,
        **entire_map(scenario)
    )

    trigger = tm.add_trigger(f"[p{player.player_id}] Remove {name.replace('_', ' ')} work rate")
    for gender in genders:
        trigger.new_effect.modify_attribute(
            quantity=0,
            object_list_unit_id=UnitInfo[f"VILLAGER_{gender}_{name.upper()}"].ID,
            source_player=player.player_id,
            operation=Operation.SET,
            object_attributes=ObjectAttribute.WORK_RATE
        )
