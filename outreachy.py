import os
from osm_fieldwork.basemapper import create_basemap_file,BaseMapper
from osm_fieldwork.utils import read_bytes_geojson

GEOJSON_FILEPATH = "tests/testdata/Rollinsville.geojson"
boundary = read_bytes_geojson(GEOJSON_FILEPATH)

create_basemap_file(
    verbose=True,
    boundary=boundary,
    outfile="outreachy.mbtiles",
    zooms="12-15",
    source="esri",
)