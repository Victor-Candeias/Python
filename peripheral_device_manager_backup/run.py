# /run.py
from flask import Flask
from app import create_app

# initialize Flask app
app = create_app()

if __name__ == '__main__':
    # Fixed app.run call
    app.run(host='0.0.0.0', port=5000, debug=True)
