import React, { useState } from 'react';

function DeviceForm({ onAddDevice }) {
  const [formData, setFormData] = useState({
    name: '',
    jobtype: '',
    responseType: '',
    dataFormat: '',
    autoStart: false,
    dataEnconding: '',
    serialPort: {
      port: '',
      baud_rate: 9600,
      byte_size: 8,
      parity: 2,
      stop_bits: 1
    },
    url: {
      url: '',
      port: '',
      autentication: ''
    },
    nave: {
      assembly: '',
      method: '',
      parameters: {
        params: '',
        params2: ''
      }
    }
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddDevice(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Device Name"
        required
      />
      <input
        type="text"
        name="jobtype"
        value={formData.jobtype}
        onChange={handleChange}
        placeholder="Job Type"
        required
      />
      <input
        type="text"
        name="responseType"
        value={formData.responseType}
        onChange={handleChange}
        placeholder="Response Type"
        required
      />
      {/* Add more form fields for the rest of the data */}
      <button type="submit">Add Device</button>
    </form>
  );
}

export default DeviceForm;
