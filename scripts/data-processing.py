from datetime import datetime
from itertools import groupby
import json
import statistics
import numpy

def build_date_stat(min_value, width, item):
  percents = [build_percent(width, min_value, value) for value in item["values"]]
  median = statistics.median(percents)
  gap_to_median = [abs(percent - median) for percent in percents]
  percentile50 = numpy.percentile(gap_to_median, 50)
  percentile75 = numpy.percentile(gap_to_median, 75)
  percentile90 = numpy.percentile(gap_to_median, 90)
  return {
    "values": item["values"],
    "percents": percents,
    "median": median,
    "percentile50": percentile50,
    "percentile75": percentile75,
    "percentile90": percentile90,
  }

def get_extremes(past_years):
  values = [value for sublist in past_years for value in sublist["values"]]
  min_value = numpy.percentile(values, 1)
  max_value = numpy.percentile(values, 99)
  return min_value, max_value

def build_batch(past_years):
  min_value, max_value = get_extremes(past_years)
  width = max_value - min_value
  return {
    "past_years": [build_date_stat(min_value, width, item) for item in past_years],
    "min_value": min_value,
    "width": width
  }

def build_percent(width, min_value, value):
  if value < min_value:
    return 0
  if value > min_value + width:
    return 100
  return (value - min_value) / width


def build_current_year_item(width, min_value, raw_item):
  value = raw_item["niveau_nappe_eau"]

  return {
    **raw_item,
    "value": value,
    "percent": build_percent(width, min_value, value)
  }

def build_date(full_data_by_year, index):
  date = None
  values = []
  for year in full_data_by_year.keys():
    try:
      item = full_data_by_year[year][index]
    except Exception as err:
      print(err)
    if not date:
      date = item["date"]
    values.append(item["niveau_nappe_eau"])
  return {
    "date": date,
    "values": values
  }

def build_past_years(full_data_by_past_year):
  past_years = []
  for index in range(365):
    past_years.append(build_date(full_data_by_past_year, index))
  return past_years

def build_interpolated_dates(measure1, measure2):
  start_date = measure1["date"].toordinal()
  end_date = measure2["date"].toordinal()
  gap_length = end_date - start_date
  interpolated_dates = []
  for index in range(1, gap_length):
    date = datetime.fromordinal(
      measure1["date"].toordinal() + index
    )
    if date.year != measure2["year"]:
      continue
    value = (measure2["niveau_nappe_eau"] - measure1["niveau_nappe_eau"]) / gap_length * index + measure1["niveau_nappe_eau"]
    interpolated_dates.append({
      "year": date.year,
      "date": date,
      "niveau_nappe_eau": value
    })
  return interpolated_dates

def fill_measures(first_measure, last_measure, items):
  all_measures = []
  previous_measure = first_measure
  for item in items:
    interpolated_dates = build_interpolated_dates(previous_measure, item)
    all_measures.extend(interpolated_dates)
    all_measures.append(item)
    previous_measure = item
  if last_measure:
    interpolated_dates = build_interpolated_dates(items[-1], last_measure)
    all_measures.extend(interpolated_dates)
  return all_measures

def build_full_data_by_year(data_by_year):
  min_year = min(data_by_year.keys())
  full_data_by_year = {}
  for year in data_by_year.keys():
    if year == min_year:
      continue
    last_measure_in_previous_year = data_by_year[year - 1][-1]
    first_measure_in_following_year = data_by_year[year + 1][-1] if (year + 1) in data_by_year else None
    full_data_by_year[year] = fill_measures(
      last_measure_in_previous_year,
      first_measure_in_following_year,
      data_by_year[year]
    )
  return full_data_by_year

def group_by_year(data):
  data_by_year_iterator = groupby(data, lambda item: item["year"])
  data_by_year = {}
  for year, data_in_year_iterator in data_by_year_iterator:
    data_by_year[year] = list(data_in_year_iterator)
  return data_by_year

def build_stats(data):
  data_by_year = group_by_year(data)
  max_year = max(data_by_year.keys())
  full_data_by_year = build_full_data_by_year(data_by_year)
  full_data_by_past_year = {
    year: full_data_by_year[year]
      for year in full_data_by_year
      if year != max_year
  }
  past_years = build_past_years(full_data_by_past_year)
  batch = build_batch(past_years)
  min_value = batch["min_value"]
  width = batch["width"]
  current_year = [build_current_year_item(width, min_value, item) for item in full_data_by_year[max_year]]
  return {
    "stats": batch["past_years"],
    "current_year": current_year
  }

def parse_date(str):
  return datetime.fromisoformat(str)

def augment_item(item):
  date = parse_date(item["date_mesure"])
  return {
    "date": date,
    "year": date.year,
    **item
  }

def serializeJson(obj):
  if isinstance(obj, datetime):
    return json.dumps({
      "$date": obj.isoformat()
    })

def process_measures(station_measures):
  augmented_data = [augment_item(item) for item in station_measures]
  return build_stats(augmented_data)

def read_measures(file_path):
  with open(file_path, "r") as file_as_str:
    return json.load(file_as_str)["data"]

def process_station_data(file_path):
  measures = read_measures(file_path)
  stats = process_measures(measures)
  output_path = f"{file_path}_processed"
  with open(output_path, "w") as output_file:
    json.dump(stats, fp=output_file, default=serializeJson)

if __name__ == "__main__":
  measures = read_measures("data/03423X0056_100.json")
  stats = process_measures(measures)
  print(stats)
  with open("data/03423X0056_100_processed.json", "w") as output_file:
    json.dump(stats, fp=output_file, default=serializeJson)
