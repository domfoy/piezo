import datetime
import json
import psycopg

def map_for_db(station):
  return {
    "station_id": station["code_bss"],
    "name": station["nom_commune"],
    "x": station["x"],
    "y": station["y"],
    "first_measure": datetime.date.fromisoformat(station["date_debut_mesure"]),
    "latest_measure": datetime.date.fromisoformat(station["date_fin_mesure"])
  }

with open("data/stations.json", "r") as file_as_str:
  rawData = json.load(file_as_str)["data"]
  db_payload = [map_for_db(station) for station in rawData]
  with psycopg.connect(host="localhost", dbname="dev", user="postgres", password="admin") as conn:
    with conn.cursor() as cursor:
      for row in db_payload:
        cursor.execute(
          """
          INSERT INTO stations (
            first_measure,
            latest_measure,
            name,
            station_id,
            x,
            y
          )
          VALUES (
              %(first_measure)s,
              %(latest_measure)s,
              %(name)s,
              %(station_id)s,
              %(x)s,
              %(y)s
          )
          ON CONFLICT ON CONSTRAINT station_pk
          DO
            UPDATE SET latest_measure = EXCLUDED.latest_measure
          """,
          # {
          #   "first_measure": datetime.date.fromisoformat("2023-01-01"),
          #   "latest_measure": datetime.date.fromisoformat("2023-12-01"),
          #   "name": "name_coucou",
          #   "station_id": "coucou",
          #   "x": 1.3,
          #   "y": 1.4
          # }
          row
        )
      conn.commit()
