import io

def read_bytes_geojson(file_path):
    with open(file_path, "rb") as geojson_file:
        geojson_bytes = geojson_file.read()  # read as a `bytes` object.
        geojson_bytes_io = io.BytesIO(geojson_bytes)  # add to a BytesIO wrapper

    return geojson_bytes_io