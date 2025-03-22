#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-22 17:03:40 krylon>
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


from collections.abc import Sequence
from typing import Final

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


monster_stats = {
    "Orc": {
        "xp": 100,
        "hp": Range(50, 100),
        "attack": Range(5, 12),
        "evade": Range(1, 8),
        "initiative": Range(1, 10),
    },
    "Skeleton": {
        "xp": 50,
        "hp": Range(20, 80),
        "attack": Range(2, 8),
        "evade": Range(1, 6),
        "initiative": Range(2, 6),
    },
}


class WorldGenerator:  # pylint: disable-msg=R0903
    """WorldGenerator generates new Worlds pseudo-randomly."""

    __slots__ = [
        "locations",
        "monsters",
        "items",
        "characters",
    ]

    locations: dict[int, Location]
    monsters: dict[int, Monster]
    items: dict[int, Item]
    characters: dict[int, Entity]

    def __init__(self) -> None:
        self.locations = {}
        self.monsters = {}
        self.items = {}
        self.characters = {}


# Local Variables: #
# python-indent: 4 #
# End: #
