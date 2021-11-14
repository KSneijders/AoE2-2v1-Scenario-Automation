from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.disable_structure import Disables
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.objects.data_objects.player import Player
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

blacksmith_feudal_techs = [TechInfo.FLETCHING.ID, TechInfo.FORGING.ID, TechInfo.PADDED_ARCHER_ARMOR.ID,
                           TechInfo.SCALE_BARDING_ARMOR.ID, TechInfo.SCALE_MAIL_ARMOR.ID]
blacksmith_castle_techs = [TechInfo.BODKIN_ARROW.ID, TechInfo.IRON_CASTING.ID, TechInfo.LEATHER_ARCHER_ARMOR.ID,
                           TechInfo.CHAIN_BARDING_ARMOR.ID, TechInfo.CHAIN_MAIL_ARMOR.ID]
blacksmith_imp_techs = [TechInfo.BRACER.ID, TechInfo.BLAST_FURNACE.ID, TechInfo.RING_ARCHER_ARMOR.ID,
                        TechInfo.PLATE_BARDING_ARMOR.ID, TechInfo.PLATE_MAIL_ARMOR.ID]


def get_all_blacksmith_techs(scenario: AoE2DEScenario, player: Player, **kwargs):
    feudal_trigger = Trigger(f"[p{player.player_id}] Get all BS Feudal techs")
    for tech in blacksmith_feudal_techs:
        feudal_trigger.new_condition.research_technology(
            source_player=player.player_id,
            technology=tech
        )
    castle_trigger = Trigger(f"[p{player.player_id}] Get all BS Castle techs")
    for tech in blacksmith_castle_techs:
        castle_trigger.new_condition.research_technology(
            source_player=player.player_id,
            technology=tech
        )
    Disables.get_instance().add_trigger(player.player_id, feudal_trigger, age_requirement="feudal")
    Disables.get_instance().add_trigger(player.player_id, castle_trigger, age_requirement="castle")


def no_current_age_blacksmith_techs(scenario: AoE2DEScenario, player: Player, **kwargs):
    castle_trigger = Trigger(f"[p{player.player_id}] Enable feudal BS techs in Castle")
    castle_trigger.new_condition.research_technology(
        source_player=player.player_id,
        technology=TechInfo.CASTLE_AGE.ID
    )
    for tech in blacksmith_feudal_techs:
        castle_trigger.new_effect.enable_disable_technology(
            source_player=player.player_id,
            technology=tech,
            enabled=True
        )

    imp_trigger = Trigger(f"[p{player.player_id}] Enable feudal BS techs in Castle")
    imp_trigger.new_condition.research_technology(
        source_player=player.player_id,
        technology=TechInfo.IMPERIAL_AGE.ID
    )
    for tech in blacksmith_castle_techs:
        imp_trigger.new_effect.enable_disable_technology(
            source_player=player.player_id,
            technology=tech,
            enabled=True
        )

    Disables.get_instance().add_other_disables(
        blacksmith_feudal_techs + blacksmith_castle_techs + blacksmith_imp_techs,
        player.player_id, 'techs'
    )
    Disables.get_instance().add_trigger(player.player_id, castle_trigger)
    Disables.get_instance().add_trigger(player.player_id, imp_trigger)
