# run.py

# flask_restful_api/run.py

print("Before from app import create_app")
from app import create_app

print("After from app import create_app")

print("Before from app.socketio_events import init_socketio, socketio")
from app.socketio_events import init_socketio, socketio

print("After from app.socketio_events import init_socketio, socketio")

# Initialize Flask app
app = create_app()

# Initialize SocketIO and register events/routes
init_socketio(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
