#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2025-03-14 15:51:16 krylon>
#
# /data/code/python/rpg/test_data.py
# created on 14. 03. 2025
# (c) 2025 Benjamin Walkenhorst
#
# This file is part of rpg. It is distributed
# under the terms of the GNU General Public License 3. See the file
# LICENSE for details or find a copy online at
# https://www.gnu.org/licenses/gpl-3.0

"""
rpg.test_data

(c) 2025 Benjamin Walkenhorst
"""


from unittest import TestCase

from rpg.data import Range


class TestData(TestCase):
    """Test the data types."""

    def test_range(self) -> None:
        """Test the Range type."""
        r1 = Range(1, 10)
        for _ in range(1000):
            n = r1.random()
            self.assertIn(n, r1)

        r2 = Range(0, 2)
        r3 = r1 + r2
        self.assertEqual(r3.lo, r1.lo + r2.lo)
        self.assertEqual(r3.hi, r1.hi + r2.hi)

# Local Variables: #
# python-indent: 4 #
# End: #
