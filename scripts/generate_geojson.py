import geojson
import json
import turfpy.measurement
import turfpy.transformation

def check_is_in_metropolitan(france, point):
  return turfpy.measurement.boolean_point_in_polygon(
    point,
    france["convex_hull"]
  )

def get_sites(france):
  with open("data/stations.json", "r") as stations_handle:
    sites = []
    for raw_site in json.load(stations_handle)["data"]:
      seq = [raw_site["x"], raw_site["y"]]
      point = geojson.Point(seq)
      if not check_is_in_metropolitan(france, point):
        continue
      site = {
        **raw_site,
        "seq": seq,
        "point": point
      }
      sites.append(site)
      point["properties"] = {"site": {**site, "point": None}}
    return sites

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

def check_point_in_bbox(bbox, point):
  return bbox[0] <= point[0] and bbox[2] > point[0] and bbox[1] <= point[1] and bbox[3] > point[1]

def is_seq(data):
  return isinstance(data, list)

def check_is_polygon_coordinates(coordinates):
  if not coordinates:
    return False
  return is_seq(coordinates) and is_seq(coordinates[0]) and is_seq(coordinates[0][0])

def find_area_site_point(sites, intersection):
  bbox = turfpy.measurement.bbox(intersection)
  candidates = [site["point"] for site in sites if check_point_in_bbox(bbox, site["point"]["coordinates"])]
  if len(candidates) == 1:
    return candidates[0]

  if len(candidates) > 1:
    site_points = geojson.FeatureCollection(candidates)
  else:
    site_points = geojson.FeatureCollection([site["point"] for site in sites])

  res_features = turfpy.measurement.points_within_polygon(site_points, intersection)
  found_site_points = res_features["features"]
  if len(found_site_points) == 0:
    return
  return found_site_points[0]

def get_intersection(france, coordinates):
  intersection = turfpy.transformation.intersect([
    geojson.Polygon(coordinates),
    france["polygon"]
  ])
  if not intersection:
    return
  if intersection["geometry"]["type"] == "Polygon":
    return intersection
  if intersection["geometry"]["type"] == "MultiPolygon":
    return intersection
  return

def main():
  france = get_france()
  sites = get_sites(france)
  voronoi = turfpy.transformation.voronoi(
    [site["seq"] for site in sites],
    france["bounding_box"]
  )
  features = []
  sites_to_assign = sites

  for index, coordinates in enumerate(voronoi["geometry"]["coordinates"]):
    print(index)
    intersection = get_intersection(france, coordinates)
    if not intersection:
      continue
    found_site_point = find_area_site_point(sites_to_assign, intersection)
    if not found_site_point:
      continue
    intersection["properties"] = {
      "site": found_site_point
    }
    features.append(intersection)
    sites_to_assign = [site for site in sites_to_assign if site["code_bss"] != found_site_point["properties"]["site"]["code_bss"]]
  result = geojson.FeatureCollection(features)
  with open("data/voronoi.geojson", "w") as output_handle:
    json.dump(result, fp=output_handle)

main()