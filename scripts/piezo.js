const axios = require('axios');
const {Command} = require('commander');
const program = new Command();

async function main(options) {
  console.log(options.code);
  const res = await axios.get(
    '/api/v1/niveaux_nappes/stations',
    {
      baseURL: 'https://hubeau.eaufrance.fr',
      params: {
        code_bss: options.code,
        date_recherche: '2023-04-30',
        fields: 'code_bss,x,y,date_debut_mesure,date_fin_mesure',
        page: 1,
        size: 10
      }
    }
  );
  console.log(res.data);
}

program
  .requiredOption('-c, --code <bss_code>', 'bss code')
  .action(main);

program.parse();