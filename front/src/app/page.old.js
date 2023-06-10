"use client"

import {useEffect, useRef} from 'react';
import styles from './page.module.css';
import Chart from 'chart.js/auto';

// import data from './data/09724X0023_P2_processed.json';
import data from './data/03423X0056_100_processed.json';

function clamp(min, max) {
  return value => {
    if (value < min) {
      return min;
    }
    if (value > max) {
      return max;
    }
    return value;
  };
}

const claimPercent = clamp(0, 100);

console.log('data', data)

const PERCENTILES = {
  '50': {
    name: 'percentile50',
    color: 'rgb(0, 100, 200)'
  },
  '75': {
    name: 'percentile75',
    color: 'rgb(0, 50, 220)'
  },
  // '90': 'percentile90'
};

export default function Home() {
  const canvasRef = useRef(null);

  const renderChart = () => {
    if (!canvasRef.current) {
      return;
    }
    const percentileDataSets = [];

    for (const percentileKey in PERCENTILES) {
      percentileDataSets.push({
        label: `high-${percentileKey}th percentile to median`,
        data: data.stats.map(row => claimPercent(100 * (row.median + row[PERCENTILES[percentileKey].name]))),
        borderColor: PERCENTILES[percentileKey].color
      });
      percentileDataSets.push({
        label: `low-${percentileKey}th percentile to median`,
        data: data.stats.map(row => claimPercent(100 * (row.median - row[PERCENTILES[percentileKey].name]))),
        borderColor: PERCENTILES[percentileKey].color
      });
    }
    const chartConfig = {
      type: 'line',
      data: {
        labels: data.stats.map((row, id) => id),
        datasets: [
          {
            label: 'Current year',
            data: data.current_year.map(row => row.percent * 100),
            borderColor: 'rgb(255, 0, 0)'
          },
          {
            label: 'Median',
            data: data.stats.map(row => row.median * 100),
            borderColor: 'rgb(0, 255, 255)'
          },
          ...percentileDataSets
        ]
      }
    };

    new Chart(canvasRef.current, chartConfig);
  };

  useEffect(() => {
    renderChart();

    return () => destroyChart();
  }, []);

  return (
    <main className={styles.main}>
      <canvas ref={canvasRef}></canvas>
    </main>
  )
}
