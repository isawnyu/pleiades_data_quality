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
from pprint import pformat
import re

logger = logging.getLogger(__name__)
# https://www.zotero.org/groups/2533/items/HQBKCQEW
# https://www.zotero.org/groups/2533/pleiades/items/itemKey/UMFZH98D
rx_zot_valid = re.compile(
    r"^https://www\.zotero\.org/groups/(2533|pleiades|2533/pleiades)/(items|items/itemKey)/[A-Z0-9]{8}/?$"
)


class PleiadesPlace:
    """
    Stores information about a Pleiades place resource, loaded from a JSON file.
    Provides methods to interrogate the data for various quality issues.
    """

    def __init__(self, file_path: Path = None):
        """Initialize the PleiadesPlace object, loading data from the specified JSON file"""
        if isinstance(file_path, Path):
            self.load_from_file(file_path)

    def load_from_file(self, file_path: Path):
        """Load place data from a Pleiades JSON file on the filesystem"""
        with open(file_path, "r", encoding="utf-8") as fp:
            self.data = json.load(fp)
        del fp

    @property
    def accuracies(self) -> set:
        """Return a set of all accuracy values for the place's locations"""
        return {l["accuracy_value"] for l in self.data["locations"]}

    @property
    def accuracy_max(self) -> float:
        """Return the maximum accuracy value for the place's locations"""
        return max([l["accuracy_value"] for l in self.data["locations"]])

    @property
    def accuracy_min(self) -> float:
        """Return the minimum accuracy value for the place's locations"""
        try:
            return min([l["accuracy_value"] for l in self.data["locations"]])
        except ValueError:
            logger.error(f"bad or missing accuracy values for {self.data['id']}")
            return 0.0

    @property
    def bad_osm_ways(self) -> bool:
        """Return True if any location is from an OSM way but has Point geometry"""
        return 0 < len(
            [
                l
                for l in self.data["locations"]
                if l["provenance"].startswith("OpenStreetMap (Way")
                and l["geometry"]["type"] == "Point"
            ]
        )

    def get_bad_osm_way_ids(self):
        """Return a list of OSM way IDs that have Point geometry"""
        return [
            l["id"]
            for l in self.data["locations"]
            if l["provenance"].startswith("OpenStreetMap (Way")
            and l["geometry"]["type"] == "Point"
        ]

    @property
    def feature_count(self) -> int:
        """Return the number of GEOJSON features for the place"""
        return len([f for f in self.data["features"]])

    @property
    def id(self) -> str:
        """Return the Pleiades ID for the place"""
        return self.data["id"]

    @property
    def names(self) -> list:
        """Return the list of names for the place"""
        return self.data["names"]

    @property
    def name_count(self) -> int:
        """Return the number of names for the place"""
        return len(self.data["names"])

    @property
    def names_modern(self) -> list:
        """Return a list of modern names for the place (starting year >= 1500)"""
        modnames = list()
        for n in self.data["names"]:
            if n["start"] is not None:
                if n["start"] >= 1500:
                    modnames.append(n)
        return modnames

    @property
    def names_romanized_only(self) -> list:
        """Return a list of names that are only in romanized form (i.e., not attested)"""
        return [n for n in self.data["names"] if not n["attested"]]

    @property
    def place_types(self) -> set:
        """Return a set of all place types for the place"""
        return set(self.data["placeTypes"])

    @property
    def precise(self) -> bool:
        """Return True if all features have 'precise' location precision"""
        vals = {f["properties"]["location_precision"] for f in self.data["features"]}
        return vals == {"precise"}

    @property
    def references(self) -> list:
        """Return the list of references for the place and its subordinate objects"""
        pid = self.id
        refs = [(pid, ref) for ref in self.data.get("references", [])]
        for loc in self.data.get("locations", []):
            refs.extend(
                [(f"{pid}:loc:{loc['id']}", ref) for ref in loc.get("references", [])]
            )
        for name in self.data.get("names", []):
            refs.extend(
                [
                    (f"{pid}:name:{name['id']}", ref)
                    for ref in name.get("references", [])
                ]
            )
        for conn in self.data.get("connections", []):
            refs.extend(
                [
                    (f"{pid}:conn:{conn['id']}", ref)
                    for ref in conn.get("references", [])
                ]
            )
        return refs

    @property
    def references_with_zotero(self) -> list:
        """Return a list of references that do have a Zotero URI in the bibliographicURI field"""
        return [
            (obj_id, ref)
            for obj_id, ref in self.references
            if ref["bibliographicURI"].startswith("https://www.zotero.org/")
        ]

    @property
    def references_without_zotero(self) -> list:
        """Return a list of references that do not have a Zotero URI in the bibliographicURI field"""
        return [
            (obj_id, ref)
            for obj_id, ref in self.references
            if not ref["bibliographicURI"].startswith("https://www.zotero.org/")
        ]

    @property
    def references_with_invalid_zotero(self) -> list:
        """Return a list of references that have an invalid Zotero URI in the bibliographicURI field"""
        zotrefs = self.references_with_zotero
        invalid = [
            (obj_id, ref)
            for obj_id, ref in zotrefs
            if rx_zot_valid.match(ref["bibliographicURI"]) is None
        ]
        return invalid

    @property
    def rough(self) -> bool:
        """Return True if all features have 'rough' location precision (i.e., none are precise)"""
        vals = {f["properties"]["location_precision"] for f in self.data["features"]}
        return vals == {"rough"}

    @property
    def title(self):
        """Return the title of the place"""
        return self.data["title"]

    @property
    def unlocated(self):
        """Return True if the place is marked as unlocated"""
        return "unlocated" in self.data["placeTypes"]
