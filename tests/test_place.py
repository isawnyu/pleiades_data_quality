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

fn = "753612858.json"
filepath = Path(f"tests/data/{fn}").resolve()
logger = logging.getLogger(__name__)


class TestPleiadesPlaceInit:
    def test_init(self):
        PleiadesPlace()

    def test_load_from_file(self):
        p = PleiadesPlace(filepath)
        assert p.title == "Porta Vesuvio"


class TestPleiadesPlaceMetrics:
    p = PleiadesPlace(filepath)

    def test_accuracies(self):
        assert {20.0} == self.p.accuracies

    def test_accuracy_max(self):
        assert 20.0 == self.p.accuracy_max

    def test_accuracy_min(self):
        assert 20.0 == self.p.accuracy_min

    def test_bad_osm_ways(self):
        assert not (self.p.bad_osm_ways)

    def test_feature_count(self):
        assert 1 == self.p.feature_count

    def test_precise(self):
        assert self.p.precise

    def test_references(self):
        assert len(self.p.references) == 7

    def test_references_with_zotero(self):
        zotrefs = self.p.references_with_zotero
        assert len(zotrefs) == 6

    def test_references_without_zotero(self):
        no_zotrefs = self.p.references_without_zotero
        assert len(no_zotrefs) == 1
        ref = no_zotrefs[0][1]
        assert ref["bibliographicURI"] == ""
        assert ref["accessURI"] == "http://www.openstreetmap.org/browse/node/317736807"

    def test_rough(self):
        assert not (self.p.rough)

    def test_unlocated(self):
        assert not (self.p.unlocated)
