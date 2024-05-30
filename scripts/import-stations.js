const fs = require('fs');

const _ = require('lodash');
const axios = require('axios');
const config = require('config');
const luxon = require('luxon');

const MIN_DATE = config.get('minDate');
const MIN_LATEST_DATE = luxon.DateTime.fromISO(config.get('minLatestDate'));

async function fetchStations() {
  const res = await axios.get(
    '/api/v1/niveaux_nappes/stations',
    {
      baseURL: 'https://hubeau.eaufrance.fr',
      params: {
        date_recherche: MIN_DATE,
        bbox: '-0.62,44.82,4.28,47.70',
        fields: 'code_bss,nom_commune,x,y,date_debut_mesure,date_fin_mesure'
        // page: 1,
        // size: 10
      }
    }
  );

  return res.data.data
}

async function main() {
  const stations = await fetchStations();

  const activeStations = _.filter(
    stations,
    station => {
      const endMeasureDate = luxon.DateTime.fromISO(station.date_fin_mesure);

      return endMeasureDate >= MIN_LATEST_DATE;
    }
  );

  fs.writeFileSync('data/sites/bbox.json', JSON.stringify(activeStations));
}

main();