
import React, { useEffect, useState } from 'react';
import { useAtom, useAtomValue } from 'jotai'
import {elevationState, updateDataState,timeState, gnssState, epochState, pointsState, API_URL, chosenPointState,epochFrequencyState} from '../states/states';
import { SatelliteMap } from './SkyPlot';
import '../css/visualization.css';
import { BarChartGraph } from './BoxPlot';
import { LineChart } from './LinePlot';
import proj4 from 'proj4';

// Define WGS84 (latitude/longitude) and UTM Zone 33 (Easting/Northing)
proj4.defs("EPSG:4326", "+proj=longlat +datum=WGS84 +no_defs");
proj4.defs("EPSG:32633", "+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs");



const gps = {
  G: 'GPS',
  R: 'GLONASS',
  E: 'Galileo',
  C: 'BeiDou',
  J: 'QZSS',
  I: 'IRNSS',
  S: 'SBAS',
};
const colors = {
  G: '#32CD32',  
  R: '#FFD700',  
  E: '#1E90FF',  
  C: '#FF1493',  
  J: '#4B0082',  
  I: '#FF8C00',  
  S: '#FF6347',  
};



function fixData(data) {
  return data.map((satellites) => {
    const finalArray = [];
    satellites.forEach((satellite, index) => {
      const satNumbers = Object.keys(satellite.Satelitenumber);
      const label = satellite.Satelitenumber[satNumbers[0]];
      const typeLabel = gps[label[0]]
      const color = colors[label[0]];
      const satellitesData = [];
      
      satNumbers.forEach((key) => {
        const satName = satellite.Satelitenumber[key];
        const satCoord = [satellite.X[key], satellite.Y[key], satellite.Z[key]];
        const time = satellite.time[key];
        const azimuth = satellite.azimuth[key];
        const zenith = satellite.zenith[key];
        satellitesData.push({
          'satName': satName,
          'satCoord': satCoord,
          'time': time,
          'azimuth': azimuth,
          'zenith': zenith
        });
      });

      finalArray.push({
        'type': typeLabel,
        'color': color,
        'satellitesData': satellitesData
      });
    });

    return finalArray;
  });
}

// Main visualization component
const Visualization = () => {
    const [satellites,setSatellites] = useState([])
    // eslint-disable-next-line no-unused-vars  
    const [error, setError] = useState('')
    const [updateData,setUpdateData] = useAtom(updateDataState);
    const gnssNames = useAtomValue(gnssState);
    const elevationAngle = useAtomValue(elevationState);
    const epochFrequency = useAtomValue(epochFrequencyState);
    const time =useAtomValue(timeState);
    const epoch = useAtomValue(epochState);
    const points = useAtomValue(pointsState);
    const cosenPoint = useAtomValue(chosenPointState);

    const labels = Array.from({ length: 2 * epoch +1}, (_, i) => 
      new Date(time.getTime() + i * epochFrequency * 60 * 1000).toISOString().slice(11, 16)
    );
    const [DOP, setDOP] = useState([[0,0,0]]);
    const [elevation_masks, setElevationMasks] = useState([]);

    useEffect(() => {
      if (!updateData) return;
    
      const filteredGNSS = Object.keys(gnssNames).filter((key) => gnssNames[key]);
      const searchPoint = points[cosenPoint].geometry.coordinates;
    
      fetch(`${API_URL}/satellites`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
          time: time.toISOString(),
          elevationAngle: elevationAngle.toString(),
          epoch: epoch.toString(),
          epochFrequency: epochFrequency.toString(),
          GNSS: filteredGNSS,
          point: searchPoint,
        }),
        mode: 'cors'
      })
      .then(res => res.json())
      .then(({ job_id }) => {
        // Start polling for result
        const interval = setInterval(() => {
          fetch(`${API_URL}/job-status/${job_id}`)
            .then(res => res.json())
            .then(statusData => {
              if (statusData.status === "done") {
                clearInterval(interval);
    
                // Get actual result
                fetch(`${API_URL}/job-result/${job_id}`)
                  .then(res => res.json())
                  .then(result => {
                    console.log("RESULT:", result);
                    setSatellites(fixData(result.list));
                    setElevationMasks(result.elevation_cutoffs);
                    setDOP(result.DOP);
                    setUpdateData(false);
                  });
              } else if (statusData.status === "error") {
                clearInterval(interval);
                console.error("Server returned error for job:", job_id);
                setUpdateData(false);
              }
            })
            .catch(err => {
              console.error("Polling error:", err);
              clearInterval(interval);
              setUpdateData(false);
            });
        }, 3000); // Poll hvert 5. sekund
      });
    }, [updateData, time, elevationAngle, epoch, gnssNames, setUpdateData, points, epochFrequency, cosenPoint]);
  
  if (updateData) {
    return <div className="loading_tekst">    
      <p>
        Loading data...<br />
        This can take some time, depending on the calculation interval and length of epoch.
      </p>
    </div>;
  }

  if (error) {
    return <p>{error}</p>;
  }
  return (
    !satellites || satellites.length === 0 ? (
      <div className="loading_tekst">
        <p>Click on the blue button to fetch data</p>
      </div>
    ) : (
      <>
      {/* Skyplot and Table Row */}
      <div className="skyplot-table-container">
        {/* Skyplot Container */}
        <div className='skyplot'>
          <SatelliteMap satellites={satellites} cutOffElevation={elevationAngle} terrainCutOff = {elevation_masks} />
        </div>
      {/* Satellite Table */}
        <div className="satellite-table">
          {satellites[0].map((satelliteGroup, index) => {
            const satType = satelliteGroup.type;
            const color = satelliteGroup.color;
            return (
              <div key={index} className="satellite-column">
                <div className="satellite-name" style={{ backgroundColor: color, fontSize: '18px' }}>
                  {satType}
                </div>
                {satelliteGroup.satellitesData.map((satellite, satIndex) => {
                  const satName = satellite.satName;
                  return (
                    <div key={satName}  className="satellite-number">
                      <p style={{ fontSize: '16px' }}>{satName}</p>
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>

      {/* Chart Row: Bar Chart and Line Chart */}
      <div className="chart-row">
        <div className="chart-box">
          <BarChartGraph data={satellites} labels={labels} />
        </div>

        <div className="chart-box">
          <LineChart data={DOP} labels={labels} satellites={satellites} />
        </div>
      </div>
    </>
    )
  );
  
};

export default Visualization;
