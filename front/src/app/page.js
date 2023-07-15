"use client"

import {useEffect} from 'react';
import L from 'leaflet';
import {MapContainer, TileLayer, useMap} from 'react-leaflet';

import 'leaflet/dist/leaflet.css';
import geoJson from './data/metropole-et-outre-mer.geojson';
import voronoi from './data/voronoi.geojson';
import stations from './data/station.geojson';

function getSiteLong(feature) {
  return feature.properties.site.coordinates[0];
}

function toHexaString(float) {
  const int = Math.floor(float * 255);

  return Number(int).toString(16).padStart(2, '0');
}

function MyComponent() {
  const map = useMap();

  useEffect(() => {
    const sitesLong = voronoi.features.map(feature => getSiteLong(feature));
    const minLong = Math.min(...sitesLong);
    const maxLong = Math.max(...sitesLong);

    const markerIcon = L.icon({
      iconUrl: '/marker.svg',
      iconSize: [25, 25 ]
    });
    // L.geoJSON(geoJson).addTo(map);
    L.geoJSON(
      voronoi,
      {
        onEachFeature: (feature, layer) => {
          const siteInfo = feature.properties.site.properties.site;

          layer.bindPopup(`<b>${siteInfo.nom_commune}</b><br>${siteInfo.date_debut_mesure} - ${siteInfo.date_fin_mesure}<br>${siteInfo.code_bss}`);

          let marker;

          layer.on('mouseover', () => {
            if (marker) {
              return;
            }
            const coord = feature.properties.site.coordinates;

            marker = L.marker(
              {
                lng: coord[0],
                lat: coord[1]
              },
              {
                icon: markerIcon
              }
            );

            marker.addTo(map);
            console.log('created marker')
          })
          layer.on('mouseleave', () => {
            if (!marker) {
              return;
            }
            marker.remove();
            console.log('removed marker')
          })
        },
        style: feature => {
          const t = (getSiteLong(feature) - minLong) / (maxLong - minLong);
          const redComp = 1 - t;
          const blueComp = t;

          return {
            // color: `#${toHexaString(redComp)}00${toHexaString(blueComp)}`,
            // stroke: false
          };
        }
      }
    ).addTo(map);
    // L.geoJSON(
    //   stations
    // ).addTo(map);
  }, [map])
  return null;
}

export default function Home() {
  return <MapContainer
    center={[45, 0]}
    zoom={13}
    style={{
      height: '100vh',
      width: '100%'
    }}
  >
    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
    <MyComponent></MyComponent>
  </MapContainer>;
}