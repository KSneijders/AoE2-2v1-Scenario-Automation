from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.object_support import Civilization
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import ObjectClass, ActionType, Attribute, Operation, ObjectAttribute
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player.player import Player
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from src.disable_structure import Disables
from src.helper import get_player_tc, entire_map, deep_get


def kill_vills_per_age(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm, um, xm, mm = scenario.trigger_manager, scenario.unit_manager, scenario.xs_manager, scenario.map_manager
    percentage = int(kwargs['challenge']['selectedOption'])  # 20 or 40

    pop_cap = int(kwargs['challenge']['selectedOption'])
    if pop_cap is not None:
        pop_cap = int(pop_cap)
    else:
        pop_cap = 200 if player.civilization != Civilization.GOTHS else 210

    xm.add_script(xs_string='\n'.join([
        f"void killP{player.player_id}Vills() {{",
        f"",
        f"",
        f"",
        f"}}",
    ]))

    for age in ["feudal", "castle", "imperial"]:
        trigger = tm.add_trigger(f"[p{player.player_id}] Kill vills when reaching {age} age")
        trigger.new_condition.research_technology(
            source_player=player.player_id,
            technology=TechInfo[f"{age.upper()}_AGE"].ID
        )
        trigger.new_effect.script_call(
            message="\n".join([
                f"void p{player.player_id}Kill{percentage}Percent{age.capitalize()}AgeVills {{",
                f"    killP{player.player_id}Vills();",
                f"}}"
            ])
        )

    for i in range(pop_cap):
        trigger = tm.add_trigger(f"Kill vill when var > 0 {i}", enabled=False, looping=True)
        trigger.new_condition.script_call(xs_function="ifKillCountAboveZero")
        trigger.new_effect.teleport_object(
            object_group=ObjectClass.CIVILIAN,
            source_player=player.player_id,
            location_x=1, location_y=1,
            area_x1=0,
            area_y1=0,
            area_x2=mm.map_size - 1,
            area_y2=mm.map_size - 1
        )
        trigger.new_effect.remove_object(
            source_player=player.player_id,
            area_x1=0, area_y1=0, area_x2=1, area_y2=1
        )
        trigger.new_effect.send_chat(
            source_player=player.player_id,
            message=f"R.I.P. Villager {i + 1}... You're housed btw!",
        )


def delay_age_until_solo_aged(scenario: AoE2DEScenario, player: Player, **kwargs):
    players_sides = kwargs['players_sides']
    defendant_id = players_sides['defendants'][0]

    for age in ["feudal", "castle", "imperial"]:
        trigger = Trigger(f"[p{player.player_id}] Wait for defendant {age.capitalize()} age")
        trigger.new_condition.research_technology(
            source_player=defendant_id,
            technology=TechInfo[f"{age.upper()}_AGE"].ID
        )
        Disables.get_instance().add_trigger(player.player_id, trigger, age_requirement=age)


def max_pop(_, player: Player, **kwargs):
    player.population_cap = int(kwargs['challenge']['selectedOption'])


def max_vills_in_dark_age(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm, um = scenario.trigger_manager, scenario.unit_manager
    challenge = kwargs['challenge']

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
        selected_object_ids=[tc.reference_id],
        action_type=ActionType.STOP
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

    reached_feudal_trigger = tm.add_trigger(f"[p{player.player_id}] Disable max dark age vills triggers")
    reached_feudal_trigger.new_condition.research_technology(
        source_player=player.player_id,
        technology=TechInfo.FEUDAL_AGE.ID
    )
    reached_feudal_trigger.new_effect.deactivate_trigger(disable_trigger.trigger_id)
    reached_feudal_trigger.new_effect.deactivate_trigger(enable_trigger.trigger_id)
    for gender in genders:
        reached_feudal_trigger.new_effect.enable_disable_object(
            object_list_unit_id=gender.ID,
            source_player=player.player_id,
            enabled=True
        )


def no_extra_tcs(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm = scenario.trigger_manager

    disable_trigger = tm.add_trigger(f"[p{player.player_id}] Disable TC", looping=True)
    disable_trigger.new_condition.own_objects(
        quantity=1,
        source_player=player.player_id,
        object_list=BuildingInfo.TOWN_CENTER.ID,
    )
    disable_trigger.new_effect.enable_disable_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=player.player_id,
        enabled=False
    )

    enable_trigger = tm.add_trigger(f"[p{player.player_id}] Enable TC", enabled=False, looping=True)
    enable_trigger.new_condition.own_fewer_objects(
        quantity=0,
        source_player=player.player_id,
        object_list=BuildingInfo.TOWN_CENTER.ID,
    )
    enable_trigger.new_effect.enable_disable_object(
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        source_player=player.player_id,
        enabled=True
    )

    disable_trigger.new_effect.deactivate_trigger(trigger_id=disable_trigger.trigger_id)
    disable_trigger.new_effect.activate_trigger(trigger_id=enable_trigger.trigger_id)
    enable_trigger.new_effect.deactivate_trigger(trigger_id=enable_trigger.trigger_id)
    enable_trigger.new_effect.activate_trigger(trigger_id=disable_trigger.trigger_id)

    kill_all_tcs = tm.add_trigger(f"[p{player.player_id}] Kill TC when > 1", looping=True)
    kill_all_tcs.new_condition.own_objects(
        quantity=2,
        source_player=player.player_id,
        object_list=BuildingInfo.TOWN_CENTER.ID,
    )
    kill_all_tcs.new_effect.kill_object(
        source_player=player.player_id,
        object_list_unit_id=BuildingInfo.TOWN_CENTER.ID,
        **entire_map(scenario)
    )


def no_relics(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm = scenario.trigger_manager

    trigger = tm.add_trigger(f"[p{player.player_id}] Drop relic from monk", looping=True)
    trigger.new_condition.own_objects(
        quantity=1,
        object_list=UnitInfo.MONK_WITH_RELIC.ID,
        source_player=player.player_id
    )
    trigger.new_effect.send_chat(
        source_player=player.player_id,
        message=f"<RED>"
                f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "
                f"You are not allowed to get relics "
                f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "
    )
    trigger.new_effect.task_object(
        object_list_unit_id=UnitInfo.MONK_WITH_RELIC.ID,
        action_type=ActionType.DROP_RELIC,
        **entire_map(scenario)
    )
    trigger = tm.add_trigger(f"[p{player.player_id}] Remove monk with relic movement speed")
    trigger.new_effect.modify_attribute(
        quantity=0,
        object_list_unit_id=UnitInfo.MONK_WITH_RELIC.ID,
        source_player=player.player_id,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.MOVEMENT_SPEED
    )
    trigger = tm.add_trigger(f"[p{player.player_id}] Eject relics every 10 seconds")
    trigger.new_condition.timer(5)
    trigger.new_condition.own_objects(
        quantity=1,
        object_list=BuildingInfo.MONASTERY.ID,
        source_player=player.player_id
    )
    trigger.new_effect.task_object(
        object_list_unit_id=BuildingInfo.MONASTERY.ID,
        source_player=player.player_id,
        action_type=ActionType.UNLOAD,
        **entire_map(scenario)
    )


def kill_vills_when_housed(scenario: AoE2DEScenario, player: Player, **kwargs):
    tm, mm = scenario.trigger_manager, scenario.map_manager
    pop_cap = deep_get(kwargs, ['dependencies', 'max_pop', 'selectedOption'])

    if pop_cap is not None:
        pop_cap = int(pop_cap)
    else:
        pop_cap = 200 if player.civilization != Civilization.GOTHS else 210

    teleport_vills_when_housed = tm.add_trigger(
        f"[p{player.player_id}] kill vills when housed", enabled=False, looping=True
    )
    teleport_vills_when_housed.new_condition.accumulate_attribute(
        quantity=1,
        attribute=Attribute.POPULATION_CAP,
        source_player=player.player_id,
        inverted=True
    )
    teleport_vills_when_housed.new_condition.accumulate_attribute(
        quantity=-30,
        attribute=Attribute.POPULATION_CAP,
        source_player=player.player_id,
    )
    teleport_vills_when_housed.new_condition.accumulate_attribute(
        quantity=pop_cap,
        attribute=Attribute.CURRENT_POPULATION,
        source_player=player.player_id,
        inverted=True
    )
    teleport_vills_when_housed.new_condition.accumulate_attribute(
        quantity=1,
        attribute=Attribute.QUEUED_COUNT,
        source_player=player.player_id,
    )
    for i in range(5):
        teleport_vills_when_housed.new_effect.teleport_object(
            object_group=ObjectClass.CIVILIAN,
            source_player=player.player_id,
            location_x=1, location_y=1,
            area_x1=0,
            area_y1=0,
            area_x2=mm.map_size - 1,
            area_y2=mm.map_size - 1
        )
        teleport_vills_when_housed.new_effect.remove_object(
            source_player=player.player_id,
            area_x1=0, area_y1=0, area_x2=1, area_y2=1
        )
        teleport_vills_when_housed.new_effect.send_chat(
            source_player=player.player_id,
            message=f"R.I.P. Villager {i + 1}... You're housed btw!",
        )

    no_houses = tm.add_trigger(f"[p{player.player_id}] No houses", enabled=False, looping=True)
    no_houses.new_condition.own_fewer_objects(
        quantity=0,
        object_list=BuildingInfo.HOUSE.ID,
        source_player=player.player_id,
    )

    wait_for_headroom = tm.add_trigger(f"[p{player.player_id}] Wait for headroom", enabled=False, looping=True)
    wait_for_headroom.new_condition.accumulate_attribute(
        quantity=1,
        attribute=Attribute.POPULATION_CAP,
        source_player=player.player_id,
    )

    game_start_delay = tm.add_trigger(f"[p{player.player_id}] Game start delay")
    game_start_delay.new_condition.timer(timer=90)
    game_start_delay.new_effect.activate_trigger(teleport_vills_when_housed.trigger_id)
    game_start_delay.new_effect.activate_trigger(no_houses.trigger_id)

    teleport_vills_when_housed.new_effect.activate_trigger(wait_for_headroom.trigger_id)
    teleport_vills_when_housed.new_effect.deactivate_trigger(teleport_vills_when_housed.trigger_id)

    no_houses.new_effect.activate_trigger(wait_for_headroom.trigger_id)
    no_houses.new_effect.deactivate_trigger(teleport_vills_when_housed.trigger_id)

    wait_for_headroom.new_effect.activate_trigger(teleport_vills_when_housed.trigger_id)
    wait_for_headroom.new_effect.deactivate_trigger(wait_for_headroom.trigger_id)
