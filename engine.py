#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-14 18:57:09 krylon>
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


import logging
import random
from dataclasses import dataclass, field
from typing import Final, Union

from rpg import common
from rpg.data import BattleOutcome, Character, Entity, Location, Range, World


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
    cur_loc: int = 0
    player: Character
    log: logging.Logger = field(repr=False, default_factory=lambda: common.get_logger("engine"))

    def __post_init__(self) -> None:
        self.cur_loc = self.world.start_loc

    def here(self) -> Location:
        """Return the current location."""
        return self.world.locations[self.cur_loc]

    def fight_round(self, opponent: Entity) -> BattleOutcome:
        """Fight an opponent for one round."""
        ini_pl: int = 0
        ini_opp: int = 0

        self.log.debug("Fight! Fight! Fight! Me against %s", opponent.name)

        while ini_pl == ini_opp:
            ini_pl = roll(self.player.initiative)
            ini_opp = roll(opponent.initiative)

        if ini_pl > ini_opp:
            attack = roll(self.player.attack)
            defend = roll(opponent.evade)

            if attack > defend:
                self.log.debug("You hit (Attack %d vs Defense %d)!",
                               attack,
                               defend)
                dmg = roll(self.player.dmg())
                dmg -= opponent.armor
                if dmg > 0:
                    opponent.hp -= dmg
                self.log.debug("You cause %d damage", max(dmg, 0))
                if opponent.hp <= 0:
                    # The monster has been slain.
                    self.log.debug("You kill %s", opponent.name)
                    self.player.xp += opponent.xp
                    return BattleOutcome.Victory
            else:
                self.log.debug("You miss (Attack %d vs Defense %d)",
                               attack,
                               defend)
        else:
            self.log.debug("%s attacks", opponent.name)
            attack = roll(opponent.attack)
            defend = roll(self.player.evade)

            if attack > defend:
                self.log.debug("%s hits (Attack %d vs Defense %d)",
                               opponent.name,
                               attack,
                               defend)
                dmg = roll(opponent.dmg())
                dmg -= self.player.armor
                if dmg > 0:
                    self.player.hp -= dmg
                self.log.debug("%s causes %d damage",
                               opponent.name,
                               max(dmg, 0))
                if self.player.hp <= 0:
                    self.log.debug("You die. *sad emoji*")
                    # The player has died.
                    return BattleOutcome.Defeat
            else:
                self.log.debug("%s misses (Attack %d vs Defense %d)",
                               opponent.name,
                               attack,
                               defend)

        return BattleOutcome.Neither


# Local Variables: #
# python-indent: 4 #
# End: #
