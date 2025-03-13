#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-13 21:21:08 krylon>
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

        self.engine.start(char, world)

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
                           if x.startswith(text)
                           ]
        return completions

    def do_look(self, arg):  # pylint: disable-msg=W0613
        """Take a look at your surroundings."""
        print("You take a look around. However, there is nothing to see, yet.")

    def do_go(self, arg):  # pylint: disable-msg=W0613
        """Go to another place."""
        print("You might be all dressed up, but you still have nowhere to go.")

    def complete_go(self, text, line, begidx, endidx):  # pylint: disable-msg=W0613
        """Complete me."""
        here = self.engine.here()
        completions = []
        if not text:
            destinations = [self.world.locations[x] for x in here.links]
            completions = [x.name for x in destinations]
        else:
            destinations = [self.world.locations[x].name for x in here.links]
            completions = [x.name for x in destinations if x.name.startswith(text)]
        return completions

    def do_quit(self, arg):  # pylint: disable-msg=W0613
        """Exit the game."""
        print("So long, and thanks for all the fish.")
        return True


if __name__ == '__main__':
    print("IMPLEMENT ME!")
    # sh = Shell()
    # sh.cmdloop()
