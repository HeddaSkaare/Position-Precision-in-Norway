import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { API_URL } from '../states/states'; // Adjust the import path as necessary

const PollingComponent = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to check if data is ready
  const pollData = () => {
    axios.get(`${API_URL}/satellites`)
      .then(response => {
        if (response.data && response.data.data) {
          setData(response.data.data);  
          setLoading(false); 
        }
      })
      .catch(error => {
        setError('Error fetching data');
        setLoading(false);
      });
  };

 
  useEffect(() => {
    const intervalId = setInterval(pollData, 3000);  // Poll every 3 seconds

    // Cleanup function to stop polling when component unmounts
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return <p>Loading data...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h2>Data Received</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default PollingComponent;
