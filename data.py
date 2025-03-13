#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-14 00:09:43 krylon>
#
# /data/code/python/rpg/game.py
# created on 12. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.data

(c) 2025 Benjamin Walkenhorst
"""

import random
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass(slots=True)
class Range:
    """Range defines a range of numbers."""

    lo: int
    hi: int

    __match_args__ = ("lo", "hi")

    def random(self) -> int:
        """Return a random number from the Range (i.e. [lo; hi])"""
        return random.randint(self.lo, self.hi)


class BattleOutcome(Enum):
    """The result of a fight."""

    Victory = auto()
    Defeat = auto()
    Neither = auto()


@dataclass(slots=True, kw_only=True)
class Entity(ABC):
    """Base class for Characters, monsters, and... possibly other living creatures."""

    name: str
    species: str
    hp_max: int
    hp: int
    xp: int
    inventory: set
    attack: int
    evade: int
    armor: int
    damage: Range
    initiative: Range


@dataclass(slots=True, kw_only=True)
class Monster(Entity):
    """Monster is a non-player character."""

    mon_id: int
    hostile: bool


@dataclass(slots=True, kw_only=True)
class Character(Entity):
    """Character is an entity within the game, controlled by the player or by the game engine."""

    char_id: int
    lvl: int
    attributes: dict[str, int]
    skills: dict[str, int]


@dataclass(slots=True, kw_only=True)
class Item:
    """Item is an object the player can pick up and use."""

    item_id: int
    name: str
    description: str
    weight: int
    properties: dict = field(default_factory=dict)
    portable: bool = True

    def __hash__(self):
        return hash(self.item_id)


@dataclass(slots=True, kw_only=True)
class Location:
    """Location is a place the player can visit."""

    loc_id: int
    name: str
    description: str
    items: dict[str, Item]
    links: list[int]
    characters: dict[str, Entity]


@dataclass(slots=True, kw_only=True)
class World:
    """World is the totality of Locations the player can travel to."""

    locations: dict[int, Location]
    start_loc: int


# Local Variables: #
# python-indent: 4 #
# End: #
