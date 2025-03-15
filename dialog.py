#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-15 22:47:44 krylon>
#
# /data/code/python/rpg/dialog.py
# created on 15. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.dialog

(c) 2025 Benjamin Walkenhorst

In this file, we attempt to model dialogue between the player and various beings they encounter.
"""


from enum import Enum, auto


class Attitude(Enum):
    """Attitude expresses how an NPC perceives the player

The values speak for themselves, I hope.
"Champion" is the attitude that Athena has towards Odysseus in the Odysee. That is,
actively interested in the player's success.
"""

    Friendly = auto()
    Hostile = auto()
    Horny = auto()
    Manipulative = auto()
    Champion = auto()
    Nemesis = auto()

# Local Variables: #
# python-indent: 4 #
# End: #
