pip install pywin32 pyserial

python serial_port_service.py install
python serial_port_service.py start
python serial_port_service.py stop
python serial_port_service.py remove

pip install pymongo

{
    "port_name": "COM3",
    "real_port": "COM1",
    "baud_rate": 9600,
    "data_bits": 8,
    "parity": "N",
    "stop_bits": 1,
    "flow_control": "None",
    "enabled": True
}


pip install Flask pymongo

/serial_port_webapp
    ├── app.py
    ├── templates
    │   ├── index.html
    │   └── form.html
    └── static
        └── style.css


Step 4: Create a Distribution Package
Use the setuptools package to create a distribution package. Run the following commands from the root of your project directory:

bash
Copy code
python setup.py sdist bdist_wheel
This command will generate distribution archives (source distribution and wheel distribution) in a dist/ directory.

Step 5: Test the Package Locally
Before deploying, test the package installation locally to ensure it works as expected:

Install the Package Locally:

bash
Copy code
pip install dist/SerialPortService-1.0.0-py3-none-any.whl
Run the Service:

Since this is a Windows service, you should follow the installation process previously discussed to install and run the service.



app.py

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection details
client = MongoClient("mongodb://localhost:27017/")
db = client["serial_port_db"]
collection = db["virtual_ports"]

@app.route('/')
def index():
    configs = list(collection.find())
    return render_template('index.html', configs=configs)

@app.route('/add', methods=['GET', 'POST'])
def add_config():
    if request.method == 'POST':
        config = {
            "port_name": request.form['port_name'],
            "real_port": request.form['real_port'],
            "baud_rate": int(request.form['baud_rate']),
            "data_bits": int(request.form['data_bits']),
            "parity": request.form['parity'],
            "stop_bits": int(request.form['stop_bits']),
            "flow_control": request.form['flow_control'],
            "enabled": request.form.get('enabled') == 'on'
        }
        collection.insert_one(config)
        return redirect(url_for('index'))
    return render_template('form.html', action='add')

@app.route('/edit/<port_name>', methods=['GET', 'POST'])
def edit_config(port_name):
    config = collection.find_one({"port_name": port_name})
    if request.method == 'POST':
        updated_config = {
            "port_name": request.form['port_name'],
            "real_port": request.form['real_port'],
            "baud_rate": int(request.form['baud_rate']),
            "data_bits": int(request.form['data_bits']),
            "parity": request.form['parity'],
            "stop_bits": int(request.form['stop_bits']),
            "flow_control": request.form['flow_control'],
            "enabled": request.form.get('enabled') == 'on'
        }
        collection.update_one({"port_name": port_name}, {"$set": updated_config})
        return redirect(url_for('index'))
    return render_template('form.html', action='edit', config=config)

@app.route('/delete/<port_name>')
def delete_config(port_name):
    collection.delete_one({"port_name": port_name})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

templates/index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Virtual Serial Ports</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>Virtual Serial Ports</h1>
    <a href="{{ url_for('add_config') }}">Add New Configuration</a>
    <table>
        <thead>
            <tr>
                <th>Port Name</th>
                <th>Real Port</th>
                <th>Baud Rate</th>
                <th>Data Bits</th>
                <th>Parity</th>
                <th>Stop Bits</th>
                <th>Flow Control</th>
                <th>Enabled</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for config in configs %}
            <tr>
                <td>{{ config.port_name }}</td>
                <td>{{ config.real_port }}</td>
                <td>{{ config.baud_rate }}</td>
                <td>{{ config.data_bits }}</td>
                <td>{{ config.parity }}</td>
                <td>{{ config.stop_bits }}</td>
                <td>{{ config.flow_control }}</td>
                <td>{{ 'Yes' if config.enabled else 'No' }}</td>
                <td>
                    <a href="{{ url_for('edit_config', port_name=config.port_name) }}">Edit</a>
                    <a href="{{ url_for('delete_config', port_name=config.port_name) }}" onclick="return confirm('Are you sure?')">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>

templates/form.html


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ 'Add' if action == 'add' else 'Edit' }} Configuration</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <h1>{{ 'Add' if action == 'add' else 'Edit' }} Configuration</h1>
    <form method="post">
        <label for="port_name">Port Name:</label>
        <input type="text" id="port_name" name="port_name" value="{{ config.port_name if action == 'edit' }}" required><br>
        <label for="real_port">Real Port:</label>
        <input type="text" id="real_port" name="real_port" value="{{ config.real_port if action == 'edit' }}" required><br>
        <label for="baud_rate">Baud Rate:</label>
        <input type="number" id="baud_rate" name="baud_rate" value="{{ config.baud_rate if action == 'edit' }}" required><br>
        <label for="data_bits">Data Bits:</label>
        <input type="number" id="data_bits" name="data_bits" value="{{ config.data_bits if action == 'edit' }}" required><br>
        <label for="parity">Parity:</label>
        <select id="parity" name="parity">
            <option value="N" {{ 'selected' if (config.parity == 'N') and action == 'edit' }}>None</option>
            <option value="E" {{ 'selected' if (config.parity == 'E') and action == 'edit' }}>Even</option>
            <option value="O" {{ 'selected' if (config.parity == 'O') and action == 'edit' }}>Odd</option>
        </select><br>
        <label for="stop_bits">Stop Bits:</label>
        <input type="number" id="stop_bits" name="stop_bits" value="{{ config.stop_bits if action == 'edit' }}" required><br>
        <label for="flow_control">Flow Control:</label>
        <select id="flow_control" name="flow_control">
            <option value="None" {{ 'selected' if (config.flow_control == 'None') and action == 'edit' }}>None</option>
            <option value="XonXoff" {{ 'selected' if (config.flow_control == 'XonXoff') and action == 'edit' }}>Xon/Xoff</option>
            <option value="RtsCts" {{ 'selected' if (config.flow_control == 'RtsCts') and action == 'edit' }}>RTS/CTS</option>
        </select><br>
        <label for="enabled">Enabled:</label>
        <input type="checkbox" id="enabled" name="enabled" {{ 'checked' if (config.enabled if action == 'edit') else '' }}><br>
        <button type="submit">{{ 'Add' if action == 'add' else 'Update' }}</button>
    </form>
    <a href="{{ url_for('index') }}">Back to list</a>
</body>
</html>

static/style.css

body {
    font-family: Arial, sans-serif;
}

h1 {
    text-align: center;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

table, th, td {
    border: 1px solid #ddd;
}

th, td {
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
}

a {
    text-decoration: none;
    color: #007bff;
}

a:hover {
    text-decoration: underline;
}


python app.py

