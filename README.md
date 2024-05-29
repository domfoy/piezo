# Inspiration

https://www.brgm.fr/fr/actualite/communique-presse/nappes-eau-souterraine-au-1er-avril-2024

# Objectives

## Country-wise

1. What is the current picture?
2. What was the picture last year? and in a different previous date?
3. I want to compare the current and previous pictures side by side and with a slider.
4. What percentages are increasing/stagnating/decreasing?
5. Among those, what is the distribution of the current levels compared to the historic median?

## Station-wise

1. On a rolling year, what is the current year evolution, compared the historic median/75th/90th?
2. On hovering, what is the exact value? the indices of current/median?

# Design plan

- For one old station, output into a file:
  - the measures of the current rolling year
  - the median
  - the 75th percentile
  - the 90th percentile
-
- one station, all raw measures to file
- augment measures to files
- visualise station graph
- visualise polygon
- save to db
- scale to all stations

# Sources

raw data (did not find files) https://ades.eaufrance.fr/Recherche

API doc https://hubeau.eaufrance.fr/page/api-piezometrie#console

Visualize historic measures https://hubeau.eaufrance.fr/sites/default/files/api/demo/piezo/piezo.htm?code_dpt=01&code_bss=06256X0188%2FPZ

GeoJson: https://github.com/gregoiredavid/france-geojson
