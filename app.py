from flask import Flask, render_template
from flask_socketio import SocketIO
from data_fetcher import fetch_data, parse_data

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """
    This function is now the main engine.
    It runs ONCE when a client connects.
    """
    print('Client connected. Fetching data for the first time...')
    
    raw_data = fetch_data()
    if raw_data:
        vehicle_positions = parse_data(raw_data)
        # We emit the data directly from here
        socketio.emit('vehicle_update', {'vehicles': vehicle_positions})
        print(f"Broadcasted data for {len(vehicle_positions)} vehicles.")
    else:
        print("Failed to fetch data on connect.")

if __name__ == '__main__':
    print("Starting server...")
    # We have removed the background task for this test
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)