import React, { useState, useEffect } from "react";
import axios from "axios";
import DeviceList from "./components/DeviceList";
import DeviceForm from "./components/DeviceForm";

function App() {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    // const response = await axios.get('http://127.0.0.1:5000/api/list_config'); // Fetching devices from new endpoint
    await axios
      .get("http://127.0.0.1:5000/api/config")
      .then((response) => {
        console.log(response.data.devices);

        setDevices(response.data.devices)
      })
      .catch((error) => console.error("Error:", error));
  };

  const handleAddDevice = async (device) => {
    // await axios.post("http://127.0.0.1:5000/api/add_config", device); // Adding device through new endpoint
    const device_teste = {
      "name": "New Device",
      "jobtype": 'Label',
      "responseType": 'Sync',
      "dataFormat": 'PDF',
      "autoStart": false,
      "serialPort": {
        "port": 'COM9',
        "baud_rate": 9600,
        "byte_size": 8,
        "parity": 2,
        "stop_bits": 1
      },
      "url": {
        "url": '',
        "port": '',
        "autentication": ''
      }
    };

    console.log(device_teste);

    await axios
    .post("http://127.0.0.1:5000/api/config", device_teste, {
      headers: {
        'Content-Type': 'application/json'  // Properly separated headers
        }
    })
    .then((response) => {
        console.log(response.data)

        fetchDevices();
      })
    .catch((error) => {
      console.error("Error:", error)
    });
  };

  const handleDeleteDevice = async (deviceId) => {
    //await axios.delete(`http://127.0.0.1:5000/api/delete_config/${deviceId}`); // Deleting device via new endpoint
    // fetchDevices();
    await axios
    .delete(`http://127.0.0.1:5000/api/config/${deviceId}`)
    .then((response) => 
      {
        console.log(response.data)

        fetchDevices();
      })
    .catch((error) => console.error("Error:", error));
  };

  return (
    <div>
      <h1>Device Manager</h1>
      <DeviceForm onAddDevice={handleAddDevice} />
      <DeviceList devices={devices} onDeleteDevice={handleDeleteDevice} />
    </div>
  );
}

export default App;
