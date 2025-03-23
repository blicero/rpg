#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-23 15:57:02 krylon>
#
# /data/code/python/rpg/generator.py
# created on 21. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.generator

(c) 2025 Benjamin Walkenhorst
"""


import random
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from krylib import Counter

from rpg.data import Entity, Item, Location, Monster, Range

site_types: Final[Sequence[str]] = (
    "village",
    "forest",
    "lake",
    "castle",
    "sewers",
    "dungeon",
    "mountains",
    "cave",
)

loc_per_site: Final[Range] = Range(4, 32)

location_types: Final[dict[str, Sequence[str]]] = {
    "village": (
        "harbor",
        "tavern",
        "market",
        "alley",
    ),
    "forest": (
        "clearing",
        "path",
        "creek",
        "spring",
    ),
    "lake": (
        "shore",
    ),
    "castle": (
        "armory",
        "courtyard",
        "kitchen",
        "cellar",
    ),
    "sewers": (
        "entrance",
        "corridor",
        "hall",
    ),
    "dungeon": (
        "corridor",
        "cell",
        "entrance",
        "torture chamber",
    ),
    "mountains": (
        "mountain pass",
    ),
}


@dataclass(slots=True, kw_only=True)
class MonsterStats:
    """MonsterStats defines the parameters for generating a Monster."""

    xp: int
    hp: Range
    attack: Range
    evade: Range
    initiative: Range


monster_stats: dict[str, MonsterStats] = {
    "Orc": MonsterStats(
        xp=100,
        hp=Range(50, 100),
        attack=Range(5, 12),
        evade=Range(1, 8),
        initiative=Range(1, 10),
    ),
    "Skeleton": MonsterStats(
        xp=50,
        hp=Range(20, 80),
        attack=Range(2, 8),
        evade=Range(1, 6),
        initiative=Range(2, 6),
    ),
}


class WorldGenerator:  # pylint: disable-msg=R0903
    """WorldGenerator generates new Worlds pseudo-randomly."""

    __slots__ = [
        "idcnt",
        "locations",
        "monsters",
        "items",
        "characters",
    ]

    idcnt: Counter
    locations: dict[int, Location]
    monsters: dict[int, Monster]
    items: dict[int, Item]
    characters: dict[int, Entity]

    def __init__(self) -> None:
        self.idcnt = Counter()
        self.locations = {}
        self.monsters = {}
        self.items = {}
        self.characters = {}

    def make_site(self) -> None:
        """Create a site"""
        site_type: Final[str] = random.choice(site_types)
        loc_cnt: int = loc_per_site.random()

        locations: list[Location] = []

        for _ in loc_cnt:
            pass

# Local Variables: #
# python-indent: 4 #
# End: #
