from __future__ import annotations

from typing import List, Dict, Union

from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class Disables:
    instance = None

    @classmethod
    def get_instance(cls) -> Disables:
        if Disables.instance is None:
            Disables.instance = cls()
        return Disables.instance

    def __init__(self) -> None:
        super().__init__()

        self.initial_disables: Dict[int, Dict[str, List[int]]] = get_disables_dict()
        self.other_disables: Dict[int, Dict[str, List[int]]] = get_disables_dict()
        self.triggers: List[Trigger] = []
        self.variable_generator = variable_nums()
        self.age_requirements: Dict[str, Dict[int, List[Trigger]]] = {}

    def next_var_id(self):
        return next(self.variable_generator)

    def add_initial_disables(self, disables: Union[int, List[int]], player: int, type_: str):
        if isinstance(disables, list):
            self.initial_disables[player][type_].extend(disables)
        else:
            self.initial_disables[player][type_].append(disables)

    def add_other_disables(self, disables: Union[int, List[int]], player: int, type_: str):
        if isinstance(disables, list):
            disables = [
                disable for disable in disables
                if disable not in self.initial_disables[player][type_] and disable != -1
            ]
            self.other_disables[player][type_].extend(disables)
        else:
            if disables not in self.initial_disables[player][type_] and disables != -1:
                self.other_disables[player][type_].append(disables)

    def add_trigger(self, player: int, trigger: Trigger, age_requirement=""):
        enable_effects = [
            (index, effect) for (index, effect) in enumerate(trigger.effects)
            if effect.effect_type in [
                EffectId.ENABLE_DISABLE_OBJECT, EffectId.ENABLE_DISABLE_TECHNOLOGY
            ] and effect.enabled == 1
        ]

        to_be_removed = []
        for type_ in ['units', 'buildings', 'techs']:
            for (index, effect) in enable_effects:
                if type_ != "techs" and effect.object_list_unit_id in self.initial_disables[player][type_]:
                    to_be_removed.append(index)
                elif type_ == "techs" and effect.technology in self.initial_disables[player][type_]:
                    to_be_removed.append(index)

        trigger.effects = [
            effect for (index, effect) in enumerate(trigger.effects) if index not in to_be_removed
        ]
        self.triggers.append(trigger)

        if age_requirement != "":
            self.age_requirements.setdefault(age_requirement, {}).setdefault(player, []).append(trigger)

    def combine_age_requirements(self, scenario: AoE2DEScenario):
        xm, tm, pm = scenario.xs_manager, scenario.trigger_manager, scenario.player_manager

        xs_list = []
        for age, player_dict in self.age_requirements.items():
            for p_id, trigger_list in player_dict.items():
                if len(trigger_list) == 0:
                    continue
                age_tech = TechInfo[f"{age.upper()}_AGE"].ID
                pm.players[p_id].disabled_techs.append(age_tech)

                for index, trigger in enumerate(trigger_list):
                    xs_list.append(f"bool {age}{index}p{p_id} = false;")
                    trigger.new_effect.script_call(
                        message=construct_enable_requirement_function(
                            age, p_id, index
                        )
                    )

                conditions = [f"{age}{i}p{p_id}" for i in range(len(trigger_list))]
                xs_list.append(
                    get_age_requirement_xs_function(
                        age, p_id, ' && '.join(conditions)
                    )
                )

                unlock_trigger = tm.add_trigger(f"[p{p_id}] {age.capitalize()} Requirements - unlock age")
                unlock_trigger.new_condition.script_call(xs_function=f"{age}p{str(int(p_id))}Requirements")
                unlock_trigger.new_effect.enable_disable_technology(
                    source_player=p_id,
                    technology=age_tech
                )
        xm.add_script(xs_string='\n'.join(xs_list))


def get_disables_dict():
    return {
        p: {k: [] for k in ['units', 'buildings', 'techs']} for p in range(1, 9)
    }


def variable_nums():
    for x in range(256):
        yield x


def get_age_requirement_xs_function(age: str, player_id: int, condition: str):
    return '\n'.join([
        f'bool {age}p{player_id}Requirements() {{',
        f'    if ({condition}) {{',
        f'        return (true);',
        f'    }}',
        f'    return (false);',
        f'}}'
    ])


def construct_enable_requirement_function(age: str, player_id: int, index: int):
    return '\n'.join([
        f'void p{player_id}Enable{age.capitalize()}{index}() {{',
        f'    {age}{index}p{player_id} = true;',
        f'}}',
    ])


_xs_enable_requirement_function = f"""
"""
