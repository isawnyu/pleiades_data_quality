#
# This file is part of pleiades_data_quality
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Convert issues.json content to thematic CSVs
"""

from airtight.cli import configure_commandline
from copy import deepcopy
import csv
import json
import logging
from pathlib import Path
from pprint import pformat

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
    ["issuespath", str, "path to issues.json file"]
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    ipath = Path(kwargs["issuespath"]).expanduser().resolve()
    logger.debug(f"ipath: {ipath}")
    with open(ipath, "r", encoding="utf-8") as fp:
        issues = json.load(fp)
    del fp
    fieldnames = ["pid", "uri", "title"]
    for k, v in issues.items():
        if k in ["places", "summary"]:
            continue
        these_fieldnames = deepcopy(fieldnames)
        if k == "poor_accuracy":
            these_fieldnames.extend(["minimum", "maximum"])
        elif k in ["rough_not_unlocated", "bad_place_type"]:
            these_fieldnames.append("place_types")
        elif k == "names_romanized_only":
            these_fieldnames.append("names")
        elif k == "bad_osm_way":
            these_fieldnames.append("osm_way_ids")
        elif k == "references_without_zotero":
            these_fieldnames.append("without_zotero")
        elif k == "references_with_invalid_zotero":
            these_fieldnames.append("invalid_zotero")
        elif k in ["empty_description", "inadequate_description"]:
            these_fieldnames.append("description")
        where = ipath.parent / f"{k}.csv"
        rows = list()
        for pid in v:
            rows.append(
                {
                    "pid": pid,
                    "uri": f"https://pleiades.stoa.org/places/{pid}",
                    "title": issues["places"][pid]["title"],
                }
            )
            if k == "poor_accuracy":
                rows[-1]["minimum"] = issues["places"][pid]["accuracy_min"]
                rows[-1]["maximum"] = issues["places"][pid]["accuracy_max"]
            elif k in ["rough_not_unlocated", "bad_place_type"]:
                rows[-1]["place_types"] = "|".join(issues["places"][pid]["place_types"])
            elif k == "names_romanized_only":
                rows[-1]["names"] = "|".join(
                    [
                        f"{n[0]}:{n[1]}:{'/'.join(n[2])}"
                        for n in issues["places"][pid]["names"]
                    ]
                )
            elif k == "bad_osm_way":
                rows[-1]["osm_way_ids"] = "|".join(issues["places"][pid]["osm_way_ids"])
            elif k == "references_without_zotero":
                rows[-1]["without_zotero"] = "|".join(
                    [
                        f"{r[0]}:{r[1]['accessURI']}>{r[1]['citationDetail']}>{r[1]['formattedCitation']}"
                        for r in issues["places"][pid]["references"]["without_zotero"]
                    ]
                )
            elif k == "references_with_invalid_zotero":
                rows[-1]["invalid_zotero"] = "|".join(
                    [
                        f"{r[0]}:{r[1]['bibliographicURI']}>{r[1]['shortTitle']}>{r[1]['formattedCitation']}"
                        for r in issues["places"][pid]["references"][
                            "with_invalid_zotero"
                        ]
                    ]
                )
            elif k in ["empty_description", "inadequate_description"]:
                # print("boop")
                # print(type(issues["places"][pid]["description"]))
                # print(f"'{issues["places"][pid]["description"]}'")
                # print("bop")
                # exit()
                rows[-1]["description"] = issues["places"][pid]["description"]

        rows = sorted(rows, key=lambda x: int(x["pid"]))
        with open(where, "w", newline="", encoding="utf-8") as fp:
            logger.debug(f"these_fieldnames: {pformat(these_fieldnames, indent=4)}")
            writer = csv.DictWriter(fp, fieldnames=these_fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        del fp
        print(f"Wrote {where}")


if __name__ == "__main__":
    try:
        main(
            **configure_commandline(
                OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
            )
        )
    except Exception as err:
        logger.fatal(err)
        exit(1)
