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
    def accuracies(self) -> set:
        return {l["accuracy_value"] for l in self.data["locations"]}

    @property
    def accuracy_max(self) -> float:
        return max([l["accuracy_value"] for l in self.data["locations"]])

    @property
    def accuracy_min(self) -> float:
        try:
            return min([l["accuracy_value"] for l in self.data["locations"]])
        except ValueError:
            logger.error(f"bad or missing accuracy values for {self.data['id']}")
            return 0.0

    @property
    def bad_osm_ways(self) -> bool:
        return 0 < len(
            [
                l
                for l in self.data["locations"]
                if l["provenance"].startswith("OpenStreetMap (Way")
                and l["geometry"]["type"] == "Point"
            ]
        )

    @property
    def feature_count(self) -> int:
        return len([f for f in self.data["features"]])

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def names(self) -> list:
        return self.data["names"]

    @property
    def names_romanized_only(self) -> list:
        return [n for n in self.data["names"] if n["attested"]]

    @property
    def name_count(self) -> int:
        return len(self.data["names"])

    @property
    def names_modern(self) -> list:
        modnames = list()
        for n in self.data["names"]:
            if n["start"] is not None:
                if n["start"] >= 1500:
                    modnames.append(n)
        return modnames

    @property
    def place_types(self) -> set:
        return set(self.data["placeTypes"])

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
