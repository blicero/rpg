#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-13 21:21:25 krylon>
#
# /data/code/python/rpg/engine.py
# created on 13. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.engine

(c) 2025 Benjamin Walkenhorst
"""


import random
from dataclasses import dataclass
from typing import Final, Union

from rpg.data import BattleOutcome, Character, Location, Monster, Range, World


def roll(rng: Union[Range, int]) -> int:
    """Roll the dice."""
    match rng:
        case int(x):
            return random.randint(1, x)
        case Range(lo, hi):
            return random.randint(lo, hi)


INITIATIVE: Final[Range] = Range(1, 10)


@dataclass(slots=True, kw_only=True)
class Engine:
    """Engine executes a game."""

    world: World
    cur_loc: int
    player: Character

    def start(self, player: Character, world: World) -> None:
        """Begin a new game."""
        self.world = world
        self.cur_loc = world.start_loc
        self.player = player

    def here(self) -> Location:
        """Return the current location."""
        return self.world.locations[self.cur_loc]

    def fight_round(self, opponent: Monster) -> BattleOutcome:
        """Fight an opponent for one round."""
        ini_pl: int = 0
        ini_opp: int = 0

        while ini_pl == ini_opp:
            ini_pl = roll(self.player.initiative)
            ini_opp = roll(opponent.initiative)

        if ini_pl > ini_opp:
            attack = roll(self.player.attack)
            defend = roll(opponent.evade)

            if attack > defend:
                dmg = roll(self.player.damage)
                dmg -= opponent.armor
                opponent.hp -= dmg
                if opponent.hp <= 0:
                    # The monster has been slain.
                    self.player.xp += opponent.xp
                    return BattleOutcome.Victory
        else:
            attack = roll(opponent.attack)
            defend = roll(self.player.evade)

            if attack > defend:
                dmg = roll(opponent.damage)
                dmg -= self.player.armor
                self.player.hp -= dmg
                if self.player.hp <= 0:
                    # The player has died.
                    return BattleOutcome.Defeat

        return BattleOutcome.Neither


# Local Variables: #
# python-indent: 4 #
# End: #
