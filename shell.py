#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-13 15:14:00 krylon>
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

import cmd
import readline


class Shell(cmd.Cmd):
    """Shell is my first attempt at a text-based interface."""

    def __init__(self):
        super().__init__()
        self.prompt = ">>>  "
        readline.set_auto_history(2000)

    def do_look(self, arg):
        print("You take a look around. However, there is nothing to see, yet.")

    def do_go(self, arg):
        print("You might be all dressed up, but you still have nowhere to go.")

    def do_quit(self, arg):
        print("So long, and thanks for all the fish.")
        return True


if __name__ == '__main__':
    sh = Shell()
    sh.cmdloop()
