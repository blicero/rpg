#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-14 12:58:19 krylon>
#
# /data/code/python/rpg/shell.py
# created on 13. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.shell

(c) 2025 Benjamin Walkenhorst
"""

import atexit
import cmd
import readline

from rpg import common
from rpg.data import BattleOutcome, Character, World
from rpg.engine import Engine


class Shell(cmd.Cmd):
    """Shell is my first attempt at a text-based interface."""

    __slots__ = [
        "world",
        "player",
        "engine",
    ]

    world: World
    player: Character
    engine: Engine

    def __init__(self, world, char):
        super().__init__()
        self.prompt = ">>>  "
        self.world = world
        self.char = char
        self.engine = Engine(player=char, world=world)  # pylint: disable-msg=E1125
        try:
            readline.read_history_file(common.path.histfile())
            readline.set_history_length(2000)
        except FileNotFoundError:
            pass
        finally:
            atexit.register(readline.write_history_file, common.path.histfile())

    def postcmd(self, stop, line) -> bool:
        """Display the player's status and location."""
        if not stop:
            player = self.engine.player
            here = self.engine.here()
            print(f"""HP: {player.hp}/{player.hp_max}
XP: {player.xp}
You are at {here.name}""")
        return stop

    def do_attack(self, arg):
        """Attack another Entity."""
        if arg not in self.world.locations[self.engine.cur_loc].characters:
            print(f"There is no {arg} here to fight.")
            return False

        opp = self.world.locations[self.engine.cur_loc].characters[arg]
        res = self.engine.fight_round(opp)
        match res:
            case BattleOutcome.Victory:
                print(f"You have slain {arg}, gained {opp.xp} XP.")
            case BattleOutcome.Defeat:
                print("You are dead. Sorry.")
                return True
            case BattleOutcome.Neither:
                print("And round and round it goes...")

    def complete_attack(self, text, line, begidx, endidx):  # pylint: disable-msg=W0613
        """Complete me."""
        here = self.engine.here()
        if not text:
            completions = here.characters.keys()
        else:
            completions = [x for x in here.characters.keys()
                           if x.lower().startswith(text.lower)
                           ]
        return completions

    def do_look(self, arg):  # pylint: disable-msg=W0613
        """Take a look at your surroundings."""
        here = self.engine.here()
        print(f"You are at {here.name}.\n{here.description}")
        if len(here.items) > 0:
            print("You see the following Items:")
            for i in sorted(here.items.keys()):
                print(f"\t{i}")
        if len(here.characters) > 0:
            print("You see the following people and/or monsters:")
            for c in sorted(here.characters.keys()):
                print(f"\t{c}")

    def do_go(self, arg):  # pylint: disable-msg=W0613
        """Go to another place."""
        here = self.engine.here()
        loc = 0
        for i in here.links:
            place = self.world.locations[i]
            if place.name == arg:
                loc = i
                break
        if loc == 0:
            print("Yeah, you're not going anywere.")
        else:
            self.engine.cur_loc = loc
            print(f"Going to {self.engine.here().name}")

    def complete_go(self, text, line, begidx, endidx):  # pylint: disable-msg=W0613
        """Complete me."""
        here = self.engine.here()
        completions = []
        if not text:
            destinations = [self.world.locations[x] for x in here.links]
            completions = [x.name for x in destinations]
        else:
            destinations = [self.world.locations[x].name for x in here.links]
            completions = [x for x in destinations if x.lower().startswith(text.lower())]
        return completions

    def do_me(self, _):
        """Display the Player's vital stats and inventory."""
        player = self.engine.player
        print(f"""Name: {player.name}
HP: {player.hp}/{player.hp_max}
XP: {player.xp}
Attack: {player.attack} / Evade: {player.evade}
Armor: {player.armor} / Damage: {player.damage}
Initiative: {player.initiative}
Inventory:""")
        for i in sorted(player.inventory):
            print(f"\t{i.name}")

    def do_quit(self, arg):  # pylint: disable-msg=W0613
        """Exit the game."""
        print("So long, and thanks for all the fish.")
        return True

    def do_EOF(self, _):
        """Handle EOF (by quitting)"""
        print("Bye bye")
        return True
