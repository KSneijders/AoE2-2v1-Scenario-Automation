from __future__ import annotations

from typing import Dict, List

from AoE2ScenarioParser.objects.data_objects.condition import Condition

extra_instant_disables: Dict[int, List[ExtraInstantDisables]] = {}


class ExtraInstantDisables:
    def __init__(self, type_: str, disable_ids: List[int], conditions: List[Condition], player: int) -> None:
        super().__init__()
        self.type_ = type_
        self.disable_ids = disable_ids
        self.conditions = conditions
        self.player = player

        extra_instant_disables[player].append(self)
