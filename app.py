from flask import Flask, render_template
from flask_socketio import SocketIO
from data_fetcher import fetch_data, parse_data
import time
from threading import Thread # <-- Import the Thread class

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def background_task():
    """Fetches, parses, and broadcasts data in a continuous loop."""
    print("Background task started.")
    while True:
        print("Fetching new data...")
        raw_data = fetch_data()
        
        if raw_data:
            vehicle_positions = parse_data(raw_data)
            socketio.emit('vehicle_update', {'vehicles': vehicle_positions})
            print(f"Broadcasted data for {len(vehicle_positions)} vehicles.")
        
        # Use a standard time.sleep() now
        time.sleep(15)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    print("Starting background thread...")
    # --- This is the new, more reliable method ---
    task = Thread(target=background_task)
    task.daemon = True # Allows main program to exit even if thread is running
    task.start()
    # -----------------------------------------
    
    print("Starting server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)