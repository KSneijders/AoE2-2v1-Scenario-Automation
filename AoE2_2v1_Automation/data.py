from typing import Dict

from AoE2ScenarioParser.datasets.players import PlayerId

colour_to_player_id: Dict = {
    'blue': PlayerId.ONE,
    'red': PlayerId.TWO,
    'green': PlayerId.THREE,
    'yellow': PlayerId.FOUR,
    'cyan': PlayerId.FIVE,
    'purple': PlayerId.SIX,
    'grey': PlayerId.SEVEN,
    'orange': PlayerId.EIGHT,
}
