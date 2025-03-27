import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import '../css/lineplot.css';

// Register the necessary components for line charts
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);
function formatSatTypes(satTypes) {
  if (satTypes.length === 0) {
    return '';
  } else if (satTypes.length === 1) {
    return satTypes[0];
  } else if (satTypes.length === 2) {
    return `${satTypes[0]} and ${satTypes[1]}`;
  } else {
    const lastTwo = satTypes.slice(-2);
    const others = satTypes.slice(0, -2);
    return `${others.join(', ')}, ${lastTwo[0]} and ${lastTwo[1]}`;
  }
}

export const LineChart = ({ data, labels, satellites }) => {
  const GDOP = data.map((array) => array[0]);
  const PDOP = data.map((array) => array[1]);
  const TDOP = data.map((array) => array[2]);
  const HDOP = data.map((array) => array[3]);
  const VDOP = data.map((array) => array[4]);
  let satTypes = [];
  console.log('satellites',satellites)
  satellites[0].forEach((satelliteGroup) => {
    satTypes.push(satelliteGroup.type);
  });
  // Single chart configuration with multiple datasets
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: 'GDOP',
        data: GDOP,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        pointBorderColor: 'rgba(75, 192, 192, 1)',
        pointBackgroundColor: '#fff',
        pointHoverBackgroundColor: 'rgba(75, 192, 192, 1)',
        pointHoverBorderColor: 'rgba(220, 220, 220, 1)'
      },
      {
        label: 'PDOP',
        data: PDOP,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        pointBorderColor: 'rgba(255, 99, 132, 1)',
        pointBackgroundColor: '#fff',
        pointHoverBackgroundColor: 'rgba(255, 99, 132, 1)',
        pointHoverBorderColor: 'rgba(220, 220, 220, 1)'
      },
      {
        label: 'TDOP',
        data: TDOP,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        pointBorderColor: 'rgba(54, 162, 235, 1)',
        pointBackgroundColor: '#fff',
        pointHoverBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointHoverBorderColor: 'rgba(220, 220, 220, 1)'
      },
      {
        label: 'HDOP',
        data: HDOP,
        borderColor: 'rgba(54, 162, 0, 1)',
        backgroundColor: 'rgba(54, 162, 0, 0.2)',
        pointBorderColor: 'rgba(54, 162, 0, 1)',
        pointBackgroundColor: '#fff',
        pointHoverBackgroundColor: 'rgba(54, 162, 0, 1)',
        pointHoverBorderColor: 'rgba(220, 220, 220, 1)'
      },
      {
        label: 'VDOP',
        data: VDOP,
        borderColor: 'rgba(54, 0, 235, 1)',
        backgroundColor: 'rgba(54, 0, 235, 0.2)',
        pointBorderColor: 'rgba(54, 0, 235, 1)',
        pointBackgroundColor: '#fff',
        pointHoverBackgroundColor: 'rgba(54, 0, 235, 1)',
        pointHoverBorderColor: 'rgba(220, 220, 220, 1)'
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 14,           // 🔠 Størrelse på legend-tekst
            weight: 'bold'      // evt: 'normal', '500', etc.
          },
          color: '#003344'          // 🎨 Farge på legend-tekst
        }
      },
      title: {
        display: true,
        text: 'DOP Values Line Chart for {formatSatTypes(satTypes)}',
        font: {
          size: 18,             // 🔠 Størrelse på tittel
          weight: 'bold'
        },
        color: '#222'           // 🎨 Tittelfarge
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Epoch Times',
          font: {
            size: 14
          },
          color: '#333'
        },
        ticks: {
          color: '#333',
          font: {
            size: 12
          }
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'DOP Value',
          font: {
            size: 14
          },
          color: '#333'
        },
        ticks: {
          color: '#333',
          font: {
            size: 12
          }
        }
      }
    }
  };

  return (
    <div className="line-chart-container">
      <Line data={chartData} options={options} /> {/* Use the 'Line' component here */}
    </div>
  );
};
