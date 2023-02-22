#
# This file is part of pleiades_data_quality
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#
"""
Read and interrogate a Pleiades place
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PleiadesPlace:
    def __init__(self, file_path: Path = None):
        if isinstance(file_path, Path):
            self.load_from_file(file_path)

    def load_from_file(self, file_path: Path):
        """Load place data from a Pleiades JSON file on the filesystem"""
        with open(file_path, "r", encoding="utf-8") as fp:
            self.data = json.load(fp)
        del fp

    @property
    def feature_count(self) -> int:
        return len([f for f in self.data["features"]])

    @property
    def precise(self) -> bool:
        vals = {f["properties"]["location_precision"] for f in self.data["features"]}
        return vals == {"precise"}

    @property
    def rough(self) -> bool:
        vals = {f["properties"]["location_precision"] for f in self.data["features"]}
        return vals == {"rough"}

    @property
    def title(self):
        return self.data["title"]

    @property
    def unlocated(self):
        return "unlocated" in self.data["placeTypes"]
