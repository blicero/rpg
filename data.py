#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-13 19:23:30 krylon>
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
from dataclasses import dataclass
from typing import Final, NamedTuple


class Range(NamedTuple):
    """Range defines a range of numbers."""

    lo: int
    hi: int

    def random(self) -> int:
        """Return a random number from the Range (i.e. [lo; hi])"""
        return random.randint(self.lo, self.hi)


@dataclass(slots=True, kw_only=True)
class Entity(ABC):
    """Base class for Characters, monsters, and... possibly other living creatures."""

    name: Final[str]
    species: Final[str]
    hp_max: int
    hp: int
    xp: int
    inventory: set


@dataclass(slots=True, kw_only=True)
class Monster(Entity):
    """Monster is a non-player character."""

    mon_id: Final[int]
    hostile: bool
    attack: Final[Range]


@dataclass(slots=True, kw_only=True)
class Character(Entity):
    """Character is an entity within the game, controlled by the player or by the game engine."""

    char_id: Final[int]
    lvl: int
    attributes: dict[str, int]
    skills: dict[str, int]


@dataclass(slots=True, kw_only=True)
class Item:
    """Item is an object the player can pick up and use."""

    item_id: Final[int]
    name: Final[str]
    description: Final[str]
    weight: Final[int]
    properties: dict
    portable: Final[bool]


@dataclass(slots=True, kw_only=True)
class Location:
    """Location is a place the player can visit."""

    loc_id: Final[int]
    name: Final[str]
    description: Final[str]
    items: dict[str, Item]
    links: list[int]
    characters: list[Character]


@dataclass(slots=True, kw_only=True)
class World:
    """World is the totality of Locations the player can travel to."""

    locations: dict[int, Location]
    start_loc: Final[int]


# Local Variables: #
# python-indent: 4 #
# End: #
