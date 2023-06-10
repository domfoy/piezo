"use client"

import h337 from 'heatmap.js';
import {useEffect, useRef} from 'react';

const points = [...Array(10).keys()]
  .map((v, index) => ({
    x: 100 + 500 * index / 10,
    y: 200,
    value: index % 2
      ? 100
      : 50
  }));

const testData = {
  max: 100,
  min: 0,
  data: points
};


export default function Home() {
  const containerRef = useRef(null);

  useEffect(() => {
    const heatMapConfig = {
      container: containerRef.current
    };
    const instance = h337.create(heatMapConfig);

    instance.setData(testData);
  });

  return <div ref={containerRef}>
    <canvas width="800" height="600"></canvas>
  </div>
}