import geojson
import json
import turfpy.measurement
import turfpy.transformation

def check_is_in_metropolitan(france, point):
  return turfpy.measurement.boolean_point_in_polygon(
    point,
    france["convex_hull"]
  )

def get_france():
  with open("data/metropole-et-outre-mer.geojson", "r") as country_geojson_handle:
    whole_france = json.load(country_geojson_handle)
    coordinates = whole_france["geometry"]["coordinates"][0][0]
    polygon = geojson.Polygon([coordinates])
    bounding_box = turfpy.measurement.bbox(polygon)
    return {
      "bounding_box": bounding_box,
      "polygon": polygon,
      "convex_hull": turfpy.transformation.convex(geojson.Feature(geometry=polygon))
    }

with open("data/stations.json", "r") as stations_handle:
  france = get_france()
  points = []
  for raw_site in json.load(stations_handle)["data"]:
    seq = [raw_site["x"], raw_site["y"]]
    point = geojson.Point(seq)
    if not check_is_in_metropolitan(france, point):
      continue
    point["properties"] = {"site": raw_site}
    points.append(point)
  features = geojson.FeatureCollection(points)
  with open("data/station.geojson", "w") as stations_geo_handle:
    json.dump(features, fp=stations_geo_handle)