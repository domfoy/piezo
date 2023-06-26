"use client"

import {useEffect} from 'react';
import L from 'leaflet';
import {MapContainer, TileLayer, useMap} from 'react-leaflet';

import 'leaflet/dist/leaflet.css';
import geoJson from './data/metropole-et-outre-mer.geojson';

function MyComponent() {
  const map = useMap();

  useEffect(() => {
    L.geoJSON(geoJson).addTo(map);
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