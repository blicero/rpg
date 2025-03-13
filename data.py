#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-12 20:43:34 krylon>
#
# /data/code/python/rpg/game.py
# created on 12. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of the Wetterfrosch weather app. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.game

(c) 2025 Benjamin Walkenhorst
"""

from dataclasses import dataclass
from typing import Final


@dataclass(slots=True, kw_only=True)
class Character:
    """Character is an entity within the game, controlled by the player or by the game engine."""

    char_id: Final[int]
    name: Final[str]
    hp: int
    hp_max: int
    xp: int
    lvl: int
    inventory: set


@dataclass(slots=True, kw_only=True)
class Item:
    """Item is an object the player can pick up and use."""

    item_id: Final[int]
    name: Final[str]
    description: Final[str]
    weight: Final[int]


# Local Variables: #
# python-indent: 4 #
# End: #
