#
# This file is part of pleiades_data_quality
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Test the pleiades_data_quality.place module
"""
import logging
from pathlib import Path
from place import PleiadesPlace

logger = logging.getLogger(__name__)


class TestPleiadesPlace:
    def test_init(self):
        PleiadesPlace()

    def test_load_from_file(self):
        fn = "753612858.json"
        filepath = Path(f"tests/data/{fn}").resolve()
        p = PleiadesPlace(filepath)
        assert p.title == "Porta Vesuvio"
