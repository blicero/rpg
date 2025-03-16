#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-16 15:35:46 krylon>
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
from functools import total_ordering
from typing import Optional

from krylib import Counter

idcnt: Counter = Counter(1, 1)


@total_ordering
@dataclass(slots=True)
class Range:
    """Range defines a range of numbers."""

    lo: int
    hi: int

    __match_args__ = ("lo", "hi")

    def __lt__(self, other):
        match other:
            case Range(_, hi):
                return self.hi < hi
            case _:
                raise TypeError(f"Cannot compare Range and {other.__class__}")

    def __eq__(self, other):
        match other:
            case Range(lo, hi):
                return self.lo == lo and self.hi == hi
            case _ if isinstance(other, range):
                return self.lo == other.start and self.hi == other.stop
            case _:
                return False

    def __contains__(self, x) -> bool:
        match x:
            case int(n):
                return self.lo <= n <= self.hi
            case _:
                raise TypeError(f"Argument must be an int, not a {x.__class__}")

    def __add__(self, other: 'Range') -> 'Range':
        """Add another Range."""
        return Range(self.lo + other.lo, self.hi + other.hi)

    def random(self) -> int:
        """Return a random number from the Range (i.e. [lo; hi])"""
        return random.randint(self.lo, self.hi)


class BattleOutcome(Enum):
    """The result of a fight."""

    Victory = auto()
    Defeat = auto()
    Neither = auto()


class Attitude(Enum):
    """Attitude expresses how an NPC perceives the player

    The values speak for themselves, I hope.
    "Champion" is the attitude that Athena has towards Odysseus in the Odysee. That is,
    actively interested in the player's success.
    """

    Friendly = auto()
    Hostile = auto()
    Horny = auto()
    Manipulative = auto()
    Champion = auto()
    Nemesis = auto()


@dataclass(slots=True)
class Flag:
    """Flag is kind of like a flag to mark if a certain event has already happened."""

    key: int
    name: str
    description: Optional[str]
    __flag: bool = False

    def __repr__(self) -> str:
        return f"""Flag<{self.name} {"|" if self.__flag else "_"}>"""

    def __bool__(self) -> bool:
        return self.__flag

    def mark_set(self) -> None:
        """Raise the flag, so to speak."""
        self.__flag = True


@dataclass(slots=True, kw_only=True)
class Item:
    """Item is an object the player can pick up and use."""

    item_id: int = field(default_factory=idcnt.count)
    name: str
    description: str
    weight: int
    properties: dict = field(default_factory=dict)
    portable: bool = True
    charges: int = 1

    def __hash__(self):
        return hash(self.item_id)


@dataclass(slots=True, kw_only=True)
class Entity(ABC):
    """Base class for Characters, monsters, and... possibly other living creatures."""

    name: str
    species: str
    hp_max: int
    hp: int
    xp: int
    inventory: dict[str, Item]
    attack: int
    evade: int
    armor: int
    damage: Range
    initiative: Range

    def dmg(self) -> Range:
        """Return the effective damage the Entity can cause, taking into account any weapons."""
        base: Range = self.damage
        weapon = self.weapon()

        if weapon is not None:
            return base + weapon.properties["damage"]
        return base

    def weapon(self) -> Optional[Item]:
        """Return the creature's most formidable weapon, if it has any."""
        weapon: Optional[Item] = None
        for i in self.inventory.values():
            if "damage" in i.properties:
                if weapon is None or weapon.properties["damage"] < i.properties["damage"]:
                    weapon = i
        return weapon


@dataclass(slots=True, kw_only=True)
class Monster(Entity):
    """Monster is a non-player character."""

    mon_id: int = field(default_factory=idcnt.count)
    hostile: bool


@dataclass(slots=True, kw_only=True)
class Character(Entity):
    """Character is an entity within the game, controlled by the player or by the game engine."""

    char_id: int = field(default_factory=idcnt.count)
    lvl: int
    attributes: dict[str, int]
    skills: dict[str, int]


@dataclass(slots=True, kw_only=True)
class Location:
    """Location is a place the player can visit."""

    loc_id: int = field(default_factory=idcnt.count)
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
    state: dict[int, Flag] = field(default_factory=dict)


# Local Variables: #
# python-indent: 4 #
# End: #
