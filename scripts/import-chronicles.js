const fs = require('fs');

const axios = require('axios');
const config = require('config');

function labeliseFloatString(floatString) {
  return `${floatString}`
    .replace('.', '__')
    .replace('-', '_');
}

function buildStationRef(station) {
  return `${labeliseFloatString(station.x)}___${labeliseFloatString(station.y)}`;
}

async function fetchStationChronicles(stationCode) {
  const res = await axios.get(
    '/api/v1/niveaux_nappes/chroniques',
    {
      baseURL: 'https://hubeau.eaufrance.fr',
      params: {
        code_bss: stationCode,
        date_debut_mesure: config.get('minDate'),
        fields: 'date_mesure,niveau_nappe_eau',
        // page: 1,
        // size: 10
      }
    }
  );
  return res.data.data;
}

async function importStationChronicles(station) {
  const chronicles = await fetchStationChronicles(station.code_bss);
  const stationRef = buildStationRef(station);
  const stationChroniclesOutputFilename = `data/sites/${stationRef}.json`;
  const content = {
    station,
    chronicles
  };

  fs.writeFileSync(stationChroniclesOutputFilename, JSON.stringify(content));
}

async function main() {
  const rawStations = fs.readFileSync('data/sites/bbox.json', 'utf8');
  const stations = JSON.parse(rawStations);
  const total = stations.length;
  let current  = 1;

  for (const station of stations) {
    console.log(`${current} / ${total}`);
    await importStationChronicles(station);
    current++;
  }
}

main();