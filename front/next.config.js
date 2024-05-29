/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (
    config
  ) => {
    const newConfig = {
      ...config,
      module: {
        ...config.module,
        rules: [
          ...config.module?.rules,
          {
            test: /\.geojson$/,
            type: 'json'
          }
        ]
      }
    };

    return newConfig
  }
};

module.exports = nextConfig
