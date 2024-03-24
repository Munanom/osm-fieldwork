#!/usr/bin/python3

# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of osm_fieldwork.
#
#     Underpass is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Underpass is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with osm_fieldwork.  If not, see <https:#www.gnu.org/licenses/>.
#
"""Test functionalty of basemapper.py."""

import logging
import os
import shutil
import pytest

from osm_fieldwork.basemapper import BaseMapper,create_basemap_file
from osm_fieldwork.sqlite import DataFile

log = logging.getLogger(__name__)
ROOTDIR = os.path.dirname(os.path.abspath(__file__))

class TestBaseMap:

    def setup_method(self):
        self.outfile = f"{ROOTDIR}/testdata/rollinsville.mbtiles"
        self.boundary= f"{ROOTDIR}/testdata/Rollinsville.geojson"
        self.base = "./tiles"
    def teardown_method(self):
        pass

    def create_basemap(self, base= "./tiles", source= "topo", xy=False):
        return BaseMapper(self.boundary, base, source, xy)

    def test_reading_geojson_and_loading_boundary(self):
        """
        Test reading GeoJSON and loading boundary.

        This function tests the reading of GeoJSON and the loading of boundary using the BaseMapper class.
        It verifies if the boundary is correctly loaded from the GeoJSON file and stored as a tuple.

        Test Cases:
        - Test if the GeoJSON file is read and boundary is loaded.
        - Test if the loaded boundary is stored as a tuple.

        """
        basemap = self.create_basemap()
        assert isinstance(basemap.bbox, tuple)

    def test_create_basemap_and_tiles(self):
        """See if the file got loaded."""
        hits = 0
        tiles = list()
        basemap = self.create_basemap()
        for level in [8, 9, 10, 11, 12]:
            basemap.getTiles(level)
            tiles +=basemap.tiles

        if len(tiles) == 5:
            hits += 1

        if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
            hits += 1

        outf = DataFile(self.outfile, basemap.getFormat())
        outf.writeTiles(tiles, self.base)

        os.remove(self.outfile)
        shutil.rmtree(self.base)

        assert hits == 2
        
    def test_load_boundary_with_bbox(self):
        """
        Test loading boundary with BBOX string and with space.

        This function tests the loading of boundary with BBOX string that contains coordinates separated by commas
        and with coordinates separated by spaces.

        Test Cases:
        - Test loading boundary with BBOX string separated by commas.
        - Test loading boundary with BBOX string separated by spaces.

        """
        comma_bbox_str="-209.519, 35.909, -209.504, 37.925"
        basemap = BaseMapper(comma_bbox_str, self.base, "topo", False)
        assert isinstance(basemap.bbox, tuple)

        space_bbox_str="-209.519 35.909 -209.504 37.925"
        basemap = BaseMapper(space_bbox_str, self.base, "topo", False)
        assert isinstance(basemap.bbox, tuple)

    def test_invalid_boundaries(self):
        """
        Test invalid boundary inputs.

        This function tests various invalid inputs for boundary parameter initialization
        in the BaseMapper class. It ensures that ValueError is raised for each invalid
        boundary input.

        Raises:
        - ValueError: If an invalid boundary is provided during initialization.
        """
        invalid_boundaries = [
            None, 
            "",  
            "invalid_bbox_string",
            "1,2,3,A",
            "3,5,b",
            " 1,2,3",
            123,  
            [1, 2, 3, 4, 5],
        ]

        for boundary_value in invalid_boundaries:
            with pytest.raises(ValueError):
                # Attempt to initialize BaseMapper with invalid boundary
                BaseMapper(boundary_value, "base_dir", "source", xy=False)

    def test_custom_tilemap_service(self):
        """
        Test custom tilemap service.

        This function tests the customization of tilemap service using customTMS method in the BaseMapper class.
        It verifies if the custom tilemap service URL is correctly set and if the source is updated accordingly.

        Test Cases:
        - Test if the source is set to 'custom' after customizing the tilemap service.
        - Test if the custom tilemap service URL is correctly set in the sources dictionary.

        """
        basemap = self.create_basemap()
        basemap.customTMS("https://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}")
        assert basemap.source == "custom"

        tms = {'name': 'custom', 
               'url': 'https://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/tile/%s', 
               'suffix': 'jpg',
                'source': 'custom'}       
        assert basemap.sources["custom"] == tms

    def test_imagery_sources(self):
        """
        Test case for verifying the sources of imagery basemaps.

        This test function creates basemaps with different sources and asserts that
        the basemap source attribute matches the expected source.

        Args:
            self: The instance of the test class.

        Returns:
            None
        """

        basemap =self.create_basemap( source="bing")
        assert basemap.source == "bing"
        basemap = self.create_basemap(source= "esri")
        assert basemap.source == "esri"
        basemap = self.create_basemap( source="google")
        assert basemap.source == "google"
        basemap =self.create_basemap(  source="oam")
        assert basemap.source == "oam"
