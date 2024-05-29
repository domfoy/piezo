Scripts:
- download_measures: For a given station, GET the relevant info from the public API
- upsert_measures: Given the output of download_measures, upsert the data
- upsert_stations: Only stations still active after a certain date. Upserts the latest_measure.