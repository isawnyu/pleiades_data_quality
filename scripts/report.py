#
# This file is part of pleiades_data_quality
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Report on problems in Pleiades data
"""

from airtight.cli import configure_commandline
import json
import logging
import os
from place import PleiadesPlace
from pathlib import Path
from pprint import pprint

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    [
        "-l",
        "--loglevel",
        "NOTSET",
        "desired logging level ("
        + "case-insensitive string: DEBUG, INFO, WARNING, or ERROR",
        False,
    ],
    ["-v", "--verbose", False, "verbose output (logging level == INFO)", False],
    [
        "-w",
        "--veryverbose",
        False,
        "very verbose output (logging level == DEBUG)",
        False,
    ],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
    ["srcdir", str, "directory tree to crawl for Pleiades JSON data"],
    ["destdir", str, "directory where report data are to be written"],
]

ACCURACY_THRESHOLD = 1000.0
issues = {
    "rough_not_unlocated": set(),
    "poor_accuracy": set(),
    "missing_accuracy": set(),
    "bad_osm_way": set(),
    "bad_place_type": set(),
}
accuracy_details = dict()
DEPRECATED_PLACE_TYPES = {
    "wall",
    "mine",
    "church",
    "temple",
    "fort",
    "province",
    "plaza",
}
place_type_details = dict()


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def evaluate(p):
    global issues
    global accuracy_details
    global place_type_details

    if p.rough and not p.unlocated:
        issues["rough_not_unlocated"].add(p.id)
    if p.precise:
        try:
            if p.accuracy_min >= ACCURACY_THRESHOLD:
                issues["poor_accuracy"].add(p.id)
                accuracy_details[p.id] = p.accuracy_min
        except TypeError:
            issues["missing_accuracy"].add(p.id)
        if p.bad_osm_ways:
            issues["bad_osm_way"].add(p.id)
    bad_place_types = DEPRECATED_PLACE_TYPES.intersection(p.place_types)
    if bad_place_types:
        issues["bad_place_type"].add(p.id)
        place_type_details[p.id] = list(bad_place_types)


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    src_path = Path(kwargs["srcdir"]).expanduser().resolve()
    logger.info("Crawling for Pleiades JSON: {src_path}")
    for (root, dirs, files) in os.walk(src_path):
        for f in files:
            if f.endswith(".json"):
                p = PleiadesPlace(Path(root) / f)
                evaluate(p)
    for k, v in issues.items():
        print(f"{k}: {len(v)}")
    dest_path = Path(kwargs["destdir"]).expanduser().resolve()
    dest_path.mkdir(parents=True, exist_ok=True)
    with open(dest_path / "issues.json", "w", encoding="utf-8") as fp:
        json.dump(issues, fp, default=set_default, indent=4, ensure_ascii=False)
    del fp
    print(f"Wrote report data to {dest_path}.")


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
