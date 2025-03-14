#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-14 13:36:05 krylon>
#
# /data/code/python/rpg/demo.py
# created on 13. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.demo

(c) 2025 Benjamin Walkenhorst
"""


import sys
from typing import Optional

from krylib import Counter

from rpg.data import Character, Item, Location, Monster, Range, World
from rpg.shell import Shell

idcnt = Counter(cnt=1, inc=1)


def create_world() -> World:
    """Create a simple world."""
    locations = [
        Location(loc_id=1,
                 name="the castle",
                 description="""Sloth Castle is an ancient castle.
                 It once was the seat of kings, but now it is abandoned and empty.""",
                 items={},
                 characters={},
                 links=[2],
                 ),
        Location(loc_id=2,
                 name="the lake",
                 description="""The lake is tranquil and serene. Mosquitoes are hovering over the water,
occasionally a fish leaps out of the water.
                 """,
                 items={
                     "Axe": Item(item_id=3,
                                 name="Axe",
                                 description="A sharp axe. Can be used to cut down trees and enemies.",
                                 weight=5,
                                 properties={"damage": Range(5, 10)},
                                 ),
                 },
                 characters={},
                 links=[1, 4]
                 ),
        Location(loc_id=4,
                 name="forest",
                 description="""Deep inside the forest, there is a clearing.
Orcs live here.""",
                 items={},
                 characters={"Orc": Monster(name="Orc",
                                            species="Orc",
                                            hp_max=80,
                                            hp=80,
                                            xp=100,
                                            inventory={Item(item_id=100,
                                                            name="Gold",
                                                            description="""Sweet, sweet gold.""",
                                                            weight=1,
                                                            portable=True)},
                                            attack=10,
                                            evade=2,
                                            armor=1,
                                            damage=Range(1, 10),
                                            initiative=Range(1, 10),
                                            mon_id=5,
                                            hostile=True,
                                            )},
                 links=[2],
                 ),
        ]

    wrld: World = World(locations={x.loc_id: x for x in locations},
                        start_loc=1)
    return wrld


def create_character() -> Character:
    """Create a character for the player."""
    name = input("What is your name?  ")
    p = Character(
        name=name,
        species="Human",
        hp_max=100,
        hp=100,
        xp=0,
        lvl=1,
        inventory=set(),
        attack=12,
        evade=8,
        armor=2,
        damage=Range(2, 12),
        initiative=Range(2, 12),
        char_id=666,
        attributes={
            "strength": 5,
            "constitution": 4,
            "swiftness": 3,
            "intelligence": 3,
            "willpower": 3,
            "charisma": 4,
        },
        skills={
            "lockpicking": 4,
            "summoning": 2,
            "gambling": 3,
        },
    )

    return p


def play(load: Optional[str] = None) -> None:
    """Play a game."""
    w = create_world()
    c = create_character()
    sh = Shell(w, c)
    sh.cmdloop()


if __name__ == '__main__':
    try:
        play()
    except KeyboardInterrupt:
        print("\nBye bye.")
        sys.exit(0)

# Local Variables: #
# python-indent: 4 #
# End: #
