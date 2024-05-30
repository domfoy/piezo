const axios = require('axios');
const config = require('config');

async function fetchStationChronicles({
  code,
  page = 1
}) {
  const results = [];
  const {data} = await axios.get(
    '/api/v1/niveaux_nappes/chroniques',
    {
      baseURL: 'https://hubeau.eaufrance.fr',
      params: {
        code_bss: code,
        date_debut_mesure: config.get('minDate'),
        fields: 'date_mesure,niveau_nappe_eau',
        page
      }
    }
  );
  results.push(...data.data);
  if (!data.next) {
    return results;
  }
  return await fetchStationChronicles({
    code,
    page: page + 1
  });
}

module.exports = {
  fetchStationChronicles
};