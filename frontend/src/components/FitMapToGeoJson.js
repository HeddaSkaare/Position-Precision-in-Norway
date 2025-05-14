import { useMap } from 'react-leaflet';
import { useEffect } from 'react';
import L from 'leaflet';

const FitMapToGeoJson = ({ geoJsonData }) => {
  const map = useMap();

  useEffect(() => {
    if (!geoJsonData || geoJsonData.length === 0) return;

    try {
      // Kombiner alle geojson-deler i én feature collection
      const allFeatures = {
        type: "FeatureCollection",
        features: geoJsonData.flatMap(g => g.features || []),
      };

      const layer = L.geoJSON(allFeatures);
      const bounds = layer.getBounds();

      map.fitBounds(bounds, {
        padding: [50, 50],
        maxZoom: 15,
        animate: true,
      });
    } catch (err) {
      console.error("Failed to fit map to geoJson:", err);
    }

  }, [geoJsonData, map]);

  return null;
};
export default FitMapToGeoJson;