#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-13 19:25:40 krylon>
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


from dataclasses import dataclass

from rpg.data import Character, World


@dataclass(slots=True, kw_only=True)
class Engine:
    """Engine executes a game."""

    world: World
    cur_loc: int
    char: Character

    def start(self, player: Character, world: World) -> None:
        """Begin a new game."""
        self.world = world
        self.cur_loc = world.start_loc


# Local Variables: #
# python-indent: 4 #
# End: #
