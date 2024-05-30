const axios = require('axios');
const {Command} = require('commander');
const program = new Command();

async function main(options) {
  const results = [];
  const res = await axios.get(
    '/api/v1/niveaux_nappes/chroniques',
    {
      baseURL: 'https://hubeau.eaufrance.fr',
      params: {
        code_bss: options.code,
        date_debut_mesure: '2020-01-01',
        fields: 'date_mesure,niveau_nappe_eau',
        // page: 1,
        // size: 10
      }
    }
  );
  results.push(...res.data.data);
  console.log(JSON.stringify(res.data.data));
}

program
  .requiredOption('-c, --code <bss_code>', 'bss code')
  .action(main);

program.parse();