import React from 'react';

function DeviceList({ devices, onDeleteDevice }) {
  return (
    <div>
      <h2>Devices</h2>
      <p>devices</p>
      <ul>
        {devices.map((device) => (
          <li key={device._id}>
            {device.name}
            <button onClick={() => onDeleteDevice(device._id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DeviceList;
