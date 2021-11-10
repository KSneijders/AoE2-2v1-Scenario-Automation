from typing import List, Dict, Union

from AoE2ScenarioParser.AoE2_2v1_Scenario_Automation.AoE2_2v1_Automation.disable_structure import Disables
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player import Player


def handle_simple_disables(player: Player, ids: Dict[str, Dict]):
    disables = Disables.get_instance()

    for id_ in ids.keys():
        if id_ in simple_disables.keys():
            for type_, list_or_item in simple_disables[id_].items():
                disables.add_initial_disables(list_or_item, player.player_id, type_)


simple_disables: Dict[str, Dict[str, Union[List[int], int]]] = {
    'no_mining_camps': {
        'buildings': BuildingInfo.MINING_CAMP.ID,
        'techs': [
            TechInfo.GOLD_MINING.ID,
            TechInfo.STONE_MINING.ID,
            TechInfo.GOLD_SHAFT_MINING.ID,
            TechInfo.STONE_SHAFT_MINING.ID,
        ]
    },
    'no_lumber_camps': {
        'buildings': BuildingInfo.LUMBER_CAMP.ID,
        'techs': [
            TechInfo.DOUBLE_BIT_AXE.ID,
            TechInfo.BOW_SAW.ID,
            TechInfo.TWO_MAN_SAW.ID,
        ]
    },
    'no_mining_upgrades': {
        'techs': [
            TechInfo.GOLD_MINING.ID,
            TechInfo.STONE_MINING.ID,
            TechInfo.GOLD_SHAFT_MINING.ID,
            TechInfo.STONE_SHAFT_MINING.ID,
        ]
    },
    'no_lumber_upgrades': {
        'techs': [
            TechInfo.DOUBLE_BIT_AXE.ID,
            TechInfo.BOW_SAW.ID,
            TechInfo.TWO_MAN_SAW.ID,
        ]
    },
    'no_mill_upgrades': {
        'techs': [
            TechInfo.HORSE_COLLAR.ID,
            TechInfo.HEAVY_PLOW.ID,
            TechInfo.CROP_ROTATION.ID,
        ]
    },
    'no_wheelbarrow_line': {
        'techs': [
            TechInfo.WHEELBARROW.ID,
            TechInfo.HAND_CART.ID,
        ]
    },
    'no_eco_upgrades': {
        'techs': [
            TechInfo.DOUBLE_BIT_AXE.ID,
            TechInfo.BOW_SAW.ID,
            TechInfo.TWO_MAN_SAW.ID,
            TechInfo.GOLD_MINING.ID,
            TechInfo.STONE_MINING.ID,
            TechInfo.GOLD_SHAFT_MINING.ID,
            TechInfo.STONE_SHAFT_MINING.ID,
            TechInfo.HORSE_COLLAR.ID,
            TechInfo.HEAVY_PLOW.ID,
            TechInfo.CROP_ROTATION.ID,
            TechInfo.WHEELBARROW.ID,
            TechInfo.HAND_CART.ID,
        ]
    },
    'no_gold_units': {
        # Todo: Add triggers for this trigger ID.
        #  malay: 2 handed swordsman become trash after unique tech researched
        #  magyars: Magyar huszar become trash after unique tech researched
        #  bohemians: Monks become trash after unique tech researched
        #  persians: crossbowman become trash after unique tech researched
        #  !!!!! REMEMBER TO ALSO UNLOCK ALL RELATED UNITE UPGRADES (ELITE AND NORMAL) !!!!!
        'units':
            [
                UnitInfo.MILITIA.ID,
                UnitInfo.MAN_AT_ARMS.ID,
                UnitInfo.LONG_SWORDSMAN.ID,
                UnitInfo.TWO_HANDED_SWORDSMAN.ID,
                UnitInfo.CHAMPION.ID,
                UnitInfo.EAGLE_SCOUT.ID,
                UnitInfo.EAGLE_WARRIOR.ID,
                UnitInfo.ELITE_EAGLE_WARRIOR.ID,

                UnitInfo.ARCHER.ID,
                UnitInfo.CROSSBOWMAN.ID,
                UnitInfo.ARBALESTER.ID,
                UnitInfo.HAND_CANNONEER.ID,
                UnitInfo.CAVALRY_ARCHER.ID,
                UnitInfo.HEAVY_CAVALRY_ARCHER.ID,

                UnitInfo.KNIGHT.ID,
                UnitInfo.CAVALIER.ID,
                UnitInfo.PALADIN.ID,
                UnitInfo.CAMEL_RIDER.ID,
                UnitInfo.HEAVY_CAMEL_RIDER.ID,
                UnitInfo.IMPERIAL_CAMEL_RIDER.ID,
                UnitInfo.BATTLE_ELEPHANT.ID,
                UnitInfo.ELITE_BATTLE_ELEPHANT.ID,
                UnitInfo.STEPPE_LANCER.ID,
                UnitInfo.ELITE_STEPPE_LANCER.ID,
                UnitInfo.XOLOTL_WARRIOR.ID,

                UnitInfo.MONK.ID,
                UnitInfo.MISSIONARY.ID,
            ] + [uu.ID for uu in UnitInfo.unique_units() if uu not in [UnitInfo.GENITOUR, UnitInfo.ELITE_GENITOUR]],
        'techs':
            [
                TechInfo.MAN_AT_ARMS.ID,
                TechInfo.LONG_SWORDSMAN.ID,
                TechInfo.TWO_HANDED_SWORDSMAN.ID,
                TechInfo.CHAMPION.ID,
                TechInfo.EAGLE_WARRIOR.ID,
                TechInfo.ELITE_EAGLE_WARRIOR.ID,

                TechInfo.CROSSBOWMAN.ID,
                TechInfo.ARBALESTER.ID,
                TechInfo.HEAVY_CAV_ARCHER.ID,

                TechInfo.CAVALIER.ID,
                TechInfo.PALADIN.ID,
                TechInfo.HEAVY_CAMEL_RIDER.ID,
                TechInfo.IMPERIAL_CAMEL_RIDER.ID,
                TechInfo.ELITE_BATTLE_ELEPHANT.ID,
                TechInfo.ELITE_STEPPE_LANCER.ID,
            ] + [uuu.ID for uuu in TechInfo.unique_unit_upgrades() if uuu != TechInfo.ELITE_GENITOUR]
    },
    'no_trash': {
        # Todo: Add triggers TO DISABLE these.
        #  malay: 2 handed swordsman become trash after unique tech researched
        #  magyars: Magyar huszar become trash after unique tech researched
        #  bohemians: Monks become trash after unique tech researched
        #  persians: crossbowman become trash after unique tech researched
        'units': [
            UnitInfo.SKIRMISHER.ID,
            UnitInfo.ELITE_SKIRMISHER.ID,
            UnitInfo.IMPERIAL_SKIRMISHER.ID,
            UnitInfo.GENITOUR.ID,
            UnitInfo.ELITE_GENITOUR.ID,

            UnitInfo.SPEARMAN.ID,
            UnitInfo.PIKEMAN.ID,
            UnitInfo.HALBERDIER.ID,

            UnitInfo.SCOUT_CAVALRY.ID,
            UnitInfo.LIGHT_CAVALRY.ID,
            UnitInfo.HUSSAR.ID,
            UnitInfo.WINGED_HUSSAR.ID,
        ],
        'techs': [
            TechInfo.ELITE_SKIRMISHER.ID,
            TechInfo.IMPERIAL_SKIRMISHER.ID,
            TechInfo.ELITE_GENITOUR.ID,

            TechInfo.PIKEMAN.ID,
            TechInfo.HALBERDIER.ID,

            TechInfo.LIGHT_CAVALRY.ID,
            TechInfo.HUSSAR.ID,
            TechInfo.WINGED_HUSSAR.ID,
        ]
    },
    'no_uu': {
        'units': [uu.ID for uu in UnitInfo.unique_units(exclude_non_castle_units=True)],
        'techs': [uuu.ID for uuu in TechInfo.unique_unit_upgrades(exclude_non_castle_techs=True)],
    },
    'disable_militia_line': {
        'units': [
            UnitInfo.MILITIA.ID,
            UnitInfo.MAN_AT_ARMS.ID,
            UnitInfo.LONG_SWORDSMAN.ID,
            UnitInfo.TWO_HANDED_SWORDSMAN.ID,
            UnitInfo.CHAMPION.ID,
        ],
        'techs': [
            TechInfo.MAN_AT_ARMS.ID,
            TechInfo.LONG_SWORDSMAN.ID,
            TechInfo.TWO_HANDED_SWORDSMAN.ID,
            TechInfo.CHAMPION.ID,
        ],
    },
    'disable_spearman_line': {
        'units': [
            UnitInfo.SPEARMAN.ID,
            UnitInfo.PIKEMAN.ID,
            UnitInfo.HALBERDIER.ID,
        ],
        'techs': [
            TechInfo.PIKEMAN.ID,
            TechInfo.HALBERDIER.ID,
        ],
    },
    'disable_scout_line': {
        'units': [
            UnitInfo.SCOUT_CAVALRY.ID,
            UnitInfo.LIGHT_CAVALRY.ID,
            UnitInfo.HUSSAR.ID,
            UnitInfo.WINGED_HUSSAR.ID,
        ],
        'techs': [
            TechInfo.LIGHT_CAVALRY.ID,
            TechInfo.HUSSAR.ID,
            TechInfo.WINGED_HUSSAR.ID,
        ],
    },
    'disable_eagle_line': {
        'units': [
            UnitInfo.EAGLE_SCOUT.ID,
            UnitInfo.EAGLE_WARRIOR.ID,
            UnitInfo.ELITE_EAGLE_WARRIOR.ID,
        ],
        'techs': [
            TechInfo.EAGLE_WARRIOR.ID,
            TechInfo.ELITE_EAGLE_WARRIOR.ID,
        ],
    },
    'disable_knight_line': {
        'units': [
            UnitInfo.KNIGHT.ID,
            UnitInfo.CAVALIER.ID,
            UnitInfo.PALADIN.ID,
        ],
        'techs': [
            TechInfo.CAVALIER.ID,
            TechInfo.PALADIN.ID,
        ],
    },
    'disable_camel_line': {
        'units': [
            UnitInfo.CAMEL_RIDER.ID,
            UnitInfo.HEAVY_CAMEL_RIDER.ID,
            UnitInfo.IMPERIAL_CAMEL_RIDER.ID,
        ],
        'techs': [
            TechInfo.HEAVY_CAMEL_RIDER.ID,
            TechInfo.IMPERIAL_CAMEL_RIDER.ID,
        ],
    },
    'disable_skirmisher_line': {
        'units': [
            UnitInfo.SKIRMISHER.ID,
            UnitInfo.ELITE_SKIRMISHER.ID,
            UnitInfo.IMPERIAL_SKIRMISHER.ID,
        ],
        'techs': [
            TechInfo.ELITE_SKIRMISHER.ID,
            TechInfo.IMPERIAL_SKIRMISHER.ID,
        ],
    },
    'disable_archer_line': {
        'units': [
            UnitInfo.ARCHER.ID,
            UnitInfo.CROSSBOWMAN.ID,
            UnitInfo.ARBALESTER.ID,
        ],
        'techs': [
            TechInfo.CROSSBOWMAN.ID,
            TechInfo.ARBALESTER.ID,
        ],
    },
    'disable_ram_line': {
        'units': [
            UnitInfo.BATTERING_RAM.ID,
            UnitInfo.CAPPED_RAM.ID,
            UnitInfo.SIEGE_RAM.ID,
        ],
        'techs': [
            TechInfo.CAPPED_RAM.ID,
            TechInfo.SIEGE_RAM.ID,
        ],
    },
    'disable_mangonal_line': {
        'units': [
            UnitInfo.MANGONEL.ID,
            UnitInfo.ONAGER.ID,
            UnitInfo.SIEGE_ONAGER.ID,
        ],
        'techs': [
            TechInfo.ONAGER.ID,
            TechInfo.SIEGE_ONAGER.ID,
        ],
    },
    'no_walls': {
        'buildings': [
            BuildingInfo.PALISADE_WALL.ID,
            BuildingInfo.PALISADE_GATE.ID,
            BuildingInfo.STONE_WALL.ID,
            BuildingInfo.GATE.ID,
        ]
    },
    'no_palisade_walls': {
        'buildings': [
            BuildingInfo.PALISADE_WALL.ID,
            BuildingInfo.PALISADE_GATE.ID,
        ]
    },
    'no_stone_walls': {
        'buildings': [
            BuildingInfo.STONE_WALL.ID,
            BuildingInfo.GATE.ID,
        ]
    },
    'no_towers': {
        'buildings': [
            BuildingInfo.WATCH_TOWER.ID,
            BuildingInfo.GUARD_TOWER.ID,
            BuildingInfo.KEEP.ID,
            BuildingInfo.BOMBARD_TOWER.ID,
        ]
    },
    'no_donjons': {'buildings': BuildingInfo.DONJON.ID},
    'no_university': {'buildings': BuildingInfo.UNIVERSITY.ID},
    'no_monastery': {'buildings': BuildingInfo.MONASTERY.ID},
    'no_kreposts': {'buildings': BuildingInfo.KREPOST.ID},
    'no_castle': {'buildings': BuildingInfo.CASTLE.ID},
    'no_market': {'buildings': BuildingInfo.MARKET.ID},
    'no_blacksmith_techs': {
        'techs': [
            TechInfo.FLETCHING.ID,
            TechInfo.BODKIN_ARROW.ID,
            TechInfo.BRACER.ID,

            TechInfo.FORGING.ID,
            TechInfo.IRON_CASTING.ID,
            TechInfo.BLAST_FURNACE.ID,

            TechInfo.PADDED_ARCHER_ARMOR.ID,
            TechInfo.LEATHER_ARCHER_ARMOR.ID,
            TechInfo.RING_ARCHER_ARMOR.ID,

            TechInfo.SCALE_BARDING_ARMOR.ID,
            TechInfo.CHAIN_BARDING_ARMOR.ID,
            TechInfo.PLATE_BARDING_ARMOR.ID,

            TechInfo.SCALE_MAIL_ARMOR.ID,
            TechInfo.CHAIN_MAIL_ARMOR.ID,
            TechInfo.PLATE_MAIL_ARMOR.ID,
        ]
    },
    'no_archer_attack': {
        'techs': [
            TechInfo.FLETCHING.ID,
            TechInfo.BODKIN_ARROW.ID,
            TechInfo.BRACER.ID,
        ]
    },
    'no_archer_defence': {
        'techs': [
            TechInfo.PADDED_ARCHER_ARMOR.ID,
            TechInfo.LEATHER_ARCHER_ARMOR.ID,
            TechInfo.RING_ARCHER_ARMOR.ID,
        ]
    },
    'no_melee_attack': {
        'techs': [
            TechInfo.FORGING.ID,
            TechInfo.IRON_CASTING.ID,
            TechInfo.BLAST_FURNACE.ID,
        ]
    },
    'no_infantry_defence': {
        'techs': [
            TechInfo.SCALE_MAIL_ARMOR.ID,
            TechInfo.CHAIN_MAIL_ARMOR.ID,
            TechInfo.PLATE_MAIL_ARMOR.ID,
        ]
    },
    'no_cavalry_defence': {
        'techs': [
            TechInfo.SCALE_BARDING_ARMOR.ID,
            TechInfo.CHAIN_BARDING_ARMOR.ID,
            TechInfo.PLATE_BARDING_ARMOR.ID,
        ]
    },
    'no_unique_techs': {
        'techs': [ut.ID for ut in TechInfo.unique_techs()]
    },
    'no_bloodlines': {'techs': TechInfo.BLOODLINES.ID},
    'no_ballistics': {'techs': TechInfo.BALLISTICS.ID},
    'no_loom': {'techs': TechInfo.LOOM.ID},
}
# no_mills
# no_extra_tcs
# no_selling_buying
# no_good_civ_units
# no_current_age_blacksmith_techs
