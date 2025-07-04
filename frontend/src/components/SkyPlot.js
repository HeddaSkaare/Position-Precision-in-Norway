import React from 'react';
import { Canvas } from '@react-three/fiber';
import { Line, Text } from '@react-three/drei';
import { Satellite, colors } from './Satellite';
import {Vector3 } from 'three';
import '../css/skyplot.css';

function sphericalToCartesian2D(r, azimuth, zenith, center) {
  // Convert to radians
  azimuth = ((90-azimuth) * Math.PI) / 180 ;
  zenith = (zenith * Math.PI) / 180 ;

  // Calculate X and Y based on 2D plane
  const x = r * Math.sin(zenith) * Math.cos(azimuth) + center[0];
  const y = r * Math.sin(zenith) * Math.sin(azimuth) + center[1];
  return [x, y];
}

const SatelliteRoute = ({ points, color }) => {
  return (
    <Line
      points={points}
      color={color}
      lineWidth={2}
      dashed={false}
    />
  );
};

const CircleOutline = ({ radius,angles, factor, position, color, lineWidth, text, font }) => {
    const points = [];
    const textPoints = [];

    // Create points along the circumference of a circle
    for (let i = 0; i <= 100; i++) {
      const angle = (i / 100) * Math.PI * 2;
      points.push([Math.cos(angle) * radius, Math.sin(angle) * radius, 0]);
      textPoints.push([Math.cos(angle) * (radius*factor), Math.sin(angle+angles) * (radius*factor), 0]);
    }

    return (
    <>
      <mesh
        position={position}
        rotation={[0, 0, 0]}
      >
        {/* Create the circular geometry */}
        <ringGeometry args={[radius - 0.05, radius, 64]} />
        <meshBasicMaterial color="white" side={1} />
      </mesh>
      <Line
        points={points} 
        color={color}
        lineWidth={lineWidth} 
        position={position}
        rotation={[0, 0, 0]} />
      <Text
        position={[textPoints[0][0],textPoints[0][1], textPoints[0][2]]} // Position of the Y-axis label
        fontSize={0.25}
        fontWeight={font}
        color="black"
      >
        {text}
      </Text>
    </>
    
  );
};
const Axes = ({ radius = 4.1, color = 'white', lineWidth = 2 }) => {
  // X-axis points
  const xAxisPoints = [
    [-radius, 0, 0], 
    [radius, 0, 0],
  ];

  // Y-axis points
  const yAxisPoints = [
    [0, -radius, 0], 
    [0, radius, 0],
  ];

  return (
    <>
      {/* X-axis */}
      <Line
        points={xAxisPoints} // Array of [x, y, z] points
        color="grey" // X axis color
        lineWidth={lineWidth} // Optional: Adjust line thickness
      />
      <Text
        position={[radius + 0.25, 0, 0]} // Position of the X-axis label
        fontSize={0.3}
        color="black"
      >
        90°
      </Text>
      <Text
        position={[-radius - 0.3, 0, 0]} // Position of the X-axis label
        fontSize={0.3}
        color="black"
      >
        270°
      </Text>
      {/* Y-axis */}
      <Line
        points={yAxisPoints} // Array of [x, y, z] points
        color="grey" // Y axis color
        lineWidth={lineWidth} // Optional: Adjust line thickness
      />
      <Text
        position={[0, radius + 0.1, 0]} // Position of the Y-axis label
        fontSize={0.3}
        color="black"
      >
        0°
      </Text>
      <Text
        position={[0, -radius - 0.1, 0]} // Position of the Y-axis label
        fontSize={0.3}
        color="black"
      >
        180°
      </Text>
    </>
  );
};

const TerrainCutoffLine = ({ points }) => {
  return (
    <Line
      points={points}
      color="blue"
      lineWidth={2}
      dashed={false}
    />
  );
};

export const SatelliteMap = ({satellites, cutOffElevation, terrainCutOff}) => {
  const center = [0, 0];
  const radius = 4;
  const cutOffRad = radius * Math.cos((cutOffElevation * Math.PI) / 180);
  const elevations = [0, 20, 40, 60]; // Example: 0°, 40°, 70° elevation circles
  const radii = elevations.map((elevation) => radius * Math.cos((elevation * Math.PI) / 180)); 
  let satelllitesRoutes = {};
  let satellitesNames = {};

  // eslint-disable-next-line
  satellites.forEach((satellitesBefore) =>
    satellitesBefore.forEach((satellites) => {
      satellites.satellitesData.forEach((satellite) => {
        const color = colors[satellite.satName[0]];
        const { azimuth, zenith } = satellite;
        const coords = sphericalToCartesian2D(radius, azimuth, zenith, center);
        if (!satelllitesRoutes[satellite.satName]) {
          satelllitesRoutes[satellite.satName] = [[coords[0], coords[1], color]];
        }else{
          satelllitesRoutes[satellite.satName].push([coords[0], coords[1], color]);
        }
      });
      
    }))
  // eslint-disable-next-line
  satellites.forEach((satellitesAll) =>{
    satellitesAll.forEach((satelliteType) => {
        satelliteType.satellitesData.forEach((satellite) => {
          const coords = sphericalToCartesian2D(radius, satellite.azimuth, satellite.zenith, center);
          satellitesNames[satellite.satName] = coords;
        });
      })
  });
  console.log("satellitesNames:", satellitesNames);
  console.log("satelllitesRoutes:", satelllitesRoutes);
  const tcf = terrainCutOff.map((elevation, index) => { 
    const zenith = 90-elevation;
    const coords = sphericalToCartesian2D(radius, index, zenith, center);
    return new Vector3(coords[0], coords[1], 0); 
  });
  return (
    <div className="skyplot-container">
      <Canvas className="skyplot-canvas" camera={{ position: [0, 0, 10], fov: 50 }}>
        <Axes/>
        <CircleOutline key = {4} radius={cutOffRad} angles={20} factor={0.78} position={[0, 0, 0]} color={'black'}lineWidth={2} text = {cutOffElevation.toString() + '°' } font={'bold'}  />
        {radii.map((radius, index) => (
          <CircleOutline key={index} radius={radius} angles={45} factor={0.7} position={[0, 0, 0]} color={'grey'} lineWidth={1} text = {elevations[index] !== 0? (elevations[index].toString() + '°') : ''} font={'light'} />
        ))}
        
        {Object.keys(satelllitesRoutes).map((satName) => {
          let color = "white"
          const routePoints = satelllitesRoutes[satName].map((satellite) => {
            color = satellite[2]
            return new Vector3(satellite[0], satellite[1], 0);
          })

          return (
            <SatelliteRoute
              key={satName}
              points={routePoints}
              color={color}
            />
          );
        })}
      {Object.keys(satellitesNames).map((satName) => {
          const sat = satellitesNames[satName];
          return <Satellite key={sat[0]} position={[sat[0], sat[1], 0]} label={satName} />;
        })}
        <TerrainCutoffLine points={tcf} />
      </Canvas>
    </div>
  );
};

