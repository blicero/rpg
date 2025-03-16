#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-16 16:50:12 krylon>
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
import os
import pickle
import re
import readline
import traceback
from re import Pattern
from typing import Final

from rpg import common
from rpg.data import BattleOutcome, Character, Monster, World
from rpg.engine import Engine
from rpg.dialog import yes_or_no

yes_no: Final[Pattern] = re.compile("(?:y(?:es)?|n(?:o)?)", re.I)


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

    def do_attack(self, arg: str) -> bool:
        """Attack another Entity."""
        if arg not in self.world.locations[self.engine.cur_loc].characters:
            print(f"There is no {arg} here to fight.")
            return False

        opp = self.engine.here().characters[arg]

        if not isinstance(opp, Monster) or not opp.hostile:
            # FIXED This should work nicely now.
            # question = Question(f"{opp.name} is not your adversary. Do you really want to fight?",
            #                     "Yes",
            #                     "No")
            # answer: str = question.ask()
            # if answer.lower().startswith("n"):
            #     return False
            response = yes_or_no(f"{opp.name} is not your adversary. Do you really want to fight?")
            if not response:
                return False

        res = self.engine.fight_round(opp)
        match res:
            case BattleOutcome.Victory:
                print(f"You have defeated {arg}, gained {opp.xp} XP.")
                del self.engine.here().characters[arg]
            case BattleOutcome.Defeat:
                print("You are dead. Sorry.")
                return True
            case BattleOutcome.Neither:
                print("And round and round it goes...")

        return False

    def complete_attack(self, text, _line, _begidx, _endidx) -> list[str]:
        """Complete me."""
        here = self.engine.here()
        completions: list[str] = list(here.characters.keys())
        if text:
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

    def do_take(self, arg) -> bool:
        """Take an Item."""
        here = self.engine.here()
        if arg not in here.items:
            print(f"There is no {arg} here.")
        elif not here.items[arg].portable:
            print(f"{arg} is not portable.")
        else:
            item = here.items[arg]
            del here.items[arg]
            self.engine.player.inventory[item.name] = item
        return False

    def complete_take(self, text, _line, _beg, _end) -> list[str]:
        """Suggest Items to take."""
        here = self.engine.here()
        items = sorted([k.name for k in here.items.values() if k.portable])

        if text:
            items = [x for x in items if x.lower().startswith(text.lower())]
        return items

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
        for i in sorted(player.inventory.keys()):
            print(f"\t{i}")

    def do_quit(self, _) -> bool:
        """Exit the game."""
        print("So long, and thanks for all the fish.")
        return True

    def do_EOF(self, _) -> bool:
        """Handle EOF (by quitting)"""
        print("Bye bye")
        return True

    def do_save(self, arg) -> bool:
        """Save the current state of the game."""
        full_path = os.path.join(common.path.save(), arg)
        with open(full_path, "wb") as fh:
            pickle.dump(self.engine, fh)
        return False

    def complete_save(self, text, _line, _begidx, _endidx) -> list[str]:
        """Suggest possible completions for save files."""
        completions: list[str] = os.listdir(common.path.save())
        if text:
            completions = [x for x in completions if x.lower().startswith(text.lower())]

        return completions

    def do_load(self, arg) -> bool:
        """Attempt to load a saved game."""
        full_path = os.path.join(common.path.save(), arg)
        if not os.path.isfile(full_path):
            print(f"{arg} does not exist!")
        else:
            with open(full_path, "rb") as fh:
                try:
                    eng = pickle.load(fh)
                except Exception as err:  # pylint: disable-msg=W0718
                    print(f"{err.__class__} while trying to load saved game {arg}: {traceback.format_exception(err)}")
                else:
                    self.engine = eng
        return False

    def complete_load(self, text, _line, _begidx, _endidx) -> list[str]:
        """Suggest completions for loading a saved game."""
        games: list[str] = os.listdir(common.path.save())
        if text:
            games = [x for x in games if x.lower().startswith(text.lower())]
        return games
