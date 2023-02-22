#
# This file is part of pleiades_data_quality
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Test the pleiades_data_quality.place module
"""

from place import PleiadesPlace


class TestPleiadesPlace:
    def test_init(self):
        PleiadesPlace()
