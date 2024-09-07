pip freeze > requirements.txt
pip install -r requirements.txt


flask_restful_api/
│
├── app/
│   ├── __init__.py        # Initialize the Flask app and register Blueprints
│   ├── models.py          # Define the data models (optional, if using ORM)
│   ├── routes.py          # Define all the API routes (endpoints)
│   ├── controllers.py     # Logic for handling requests
│   └── utils.py           # Utility functions (e.g., helper functions)
│
├── tests/
│   ├── test_api.py        # Unit tests for your API
│   └── __init__.py        # Init file for tests
│
├── config.py              # Configuration settings
├── run.py                 # Script to run the Flask application
└── requirements.txt       # Python dependencies

Create Output Job:
curl -X POST http://localhost:5000/api/output_job -H "Content-Type: application/json" -d '{
  "machineid": "123",
  "sessionid": "abc",
  "userinfo": "user1",
  "ticket_id": "T123",
  "type_of_job": "receipt",
  "job_mode": "synchronous",
  "date": "2023-08-23"
}'

Delete Output Job:
curl -X DELETE http://localhost:5000/api/output_job -H "Content-Type: application/json" -d '{
  "machineid": "123",
  "sessionid": "abc",
  "userinfo": "user1",
  "ticket_id": "T123",
  "job_id": "your_job_id"
}'

List Output Jobs:
curl -X GET http://localhost:5000/api/output_jobs -H "Content-Type: application/json" -d '{
  "machineid": "123",
  "sessionid": "abc"
}'

Get Event Channel:
curl -X POST http://localhost:5000/api/event_channel -H "Content-Type: application/json" -d '{
  "machineid": "123",
  "sessionid": "abc"
}'

List All Devices:
curl http://localhost:5000/api/devices

Create Input Job:
curl -X POST http://localhost:5000/api/input_job -H "Content-Type: application/json" -d '{
  "machineid": "123",
  "sessionid": "abc",
  "input_type": "scale",
  "value": "200",
  "unit": "grams"
}'

