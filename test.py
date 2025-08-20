import time
from threading import Thread
import requests
from google.transit import gtfs_realtime_pb2
from flask import Flask
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

# --- All the code is now in one file ---

# 1. DATA FETCHER LOGIC
# Replace with your actual URL and API Key

load_dotenv()

# 1. The main domain of the API website.
BASE_URL = "https://otd.delhi.gov.in/" 

# 2. Your private API key.
API_KEY = os.getenv("TRANSIT_API_KEY")
ENDPOINT_PATH = "/api/realtime/VehiclePositions.pb"
FULL_API_URL = BASE_URL + ENDPOINT_PATH

def fetch_data():
    params = {'key': API_KEY}
    try:
        response = requests.get(FULL_API_URL, params=params)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_data(raw_data):
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(raw_data)
    vehicles = []
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            vehicles.append({
                'id': entity.id,
                'lat': entity.vehicle.position.latitude,
                'lon': entity.vehicle.position.longitude
            })
    return vehicles

# 2. FLASK & SOCKETIO SETUP
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 3. BACKGROUND TASK
def background_task():
    print("Background task started.")
    while True:
        print("Fetching new data...")
        raw_data = fetch_data()
        if raw_data:
            vehicle_positions = parse_data(raw_data)
            socketio.emit('vehicle_update', {'vehicles': vehicle_positions})
            print(f"Broadcasted data for {len(vehicle_positions)} vehicles.")
        time.sleep(15)

# 4. HTML & JAVASCRIPT
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Delhi Transit Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style> #map { height: 100vh; } body { padding: 0; margin: 0; } </style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([28.6139, 77.2090], 11);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        let vehicleMarkers = {};
        const socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('connect', () => {
            console.log('Successfully connected to the backend server!');
        });

        socket.on('vehicle_update', (data) => {
            const vehicles = data.vehicles;
            console.log(`Received update for ${vehicles.length} vehicles.`);
            
            vehicles.forEach(vehicle => {
                const vehicleId = vehicle.id;
                const position = [vehicle.lat, vehicle.lon];

                if (vehicleMarkers[vehicleId]) {
                    vehicleMarkers[vehicleId].setLatLng(position);
                } else {
                    vehicleMarkers[vehicleId] = L.marker(position).addTo(map)
                        .bindPopup(`Vehicle ID: ${vehicleId}`);
                }
            });
        });
    </script>
</body>
</html>
"""

# 5. THE MAIN ROUTE
@app.route('/')
def index():
    return HTML

# 6. START THE SERVER AND BACKGROUND TASK
if __name__ == '__main__':
    print("Starting background thread...")
    task = Thread(target=background_task)
    task.daemon = True
    task.start()
    
    print("Starting server...")
    socketio.run(app, host='0.0.0.0', port=5000)