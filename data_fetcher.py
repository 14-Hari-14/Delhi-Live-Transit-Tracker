import requests
from google.transit import gtfs_realtime_pb2

import os
from dotenv import load_dotenv

# 1. The main domain of the API website.
BASE_URL = "https://otd.delhi.gov.in/" 


load_dotenv()

# 2. Your private API key.
API_KEY = os.getenv("TRANSIT_API_KEY")



# The endpoint path provided in the documentation
ENDPOINT_PATH = "/api/realtime/VehiclePositions.pb"
FULL_API_URL = BASE_URL + ENDPOINT_PATH


def fetch_data():
    """Fetches raw GTFS data from the API using a key as a query parameter."""
    
    # The `requests` library will automatically format this into the correct URL:
    # .../VehiclePositions.pb?key=YOUR_PRIVATE_KEY
    params = {
        'key': API_KEY
    }
    
    try:
        # Pass the params dictionary with your request
        response = requests.get(FULL_API_URL, params=params)
        response.raise_for_status() # Raises an exception for bad status codes (like 401 Unauthorized)
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_data(raw_data):
    """Parses the raw GTFS data and extracts vehicle positions."""
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(raw_data)
    
    vehicles = []
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            vehicle_data = {
                'id': entity.id,
                'lat': entity.vehicle.position.latitude,
                'lon': entity.vehicle.position.longitude
            }
            vehicles.append(vehicle_data)
    return vehicles

if __name__ == "__main__":
    """A test block to ensure the script is working correctly."""
    raw_data = fetch_data()
    if raw_data:
        vehicle_positions = parse_data(raw_data)
        print(f"Successfully parsed {len(vehicle_positions)} vehicles.")
        # Print the first 5 vehicles to check
        for vehicle in vehicle_positions[:20]:
            print(vehicle)