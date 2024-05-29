import json
import requests

OUTPUT_DIRECTORY = "data/measures"
HOSTNAME = "https://hubeau.eaufrance.fr/api/v1/niveaux_nappes"
CHRONICLE_BASE_URL = f"{HOSTNAME}/chroniques"

def get_measures(station_id, start_date):
  r = requests.get(
    CHRONICLE_BASE_URL,
    params={
      "code_bss": station_id,
      "date_debut_mesure": start_date,
      "fields": "date_mesure,niveau_nappe_eau"
    }
  )
  response = json.load(r.json())
  full_response = {
    **response,
    "station_id": station_id,
    "start_date": start_date
  }
  output_path = f"{OUTPUT_DIRECTORY}"
  with open()
