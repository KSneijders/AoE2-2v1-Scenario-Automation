from __future__ import annotations

from typing import List, Dict, Union

from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger


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
        for type_ in ['units', 'buildings']:
            for (index, effect) in enable_effects:
                if effect.object_list_unit_id in self.initial_disables[player][type_]:
                    to_be_removed.append(index)

        trigger.effects = [
            effect for (index, effect) in enumerate(trigger.effects) if index not in to_be_removed
        ]
        self.triggers.append(trigger)


def get_disables_dict():
    return {
        p: {k: [] for k in ['units', 'buildings', 'techs']} for p in range(1, 9)
    }


def variable_nums():
    for x in range(256):
        yield x
