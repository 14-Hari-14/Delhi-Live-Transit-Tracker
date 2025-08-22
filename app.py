# app.py

from flask import Flask, jsonify, render_template
from data_fetcher import fetch_data, parse_data
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow your frontend 
# to fetch data from this backend, even if they run on different ports.
CORS(app)


@app.route('/')
def index():
    """
    This route will serve the main HTML page for the map.
    We will create the 'index.html' file in the next step.
    """
    return render_template('index.html')


@app.route('/api/vehicle_positions')
def get_vehicle_positions():
    """
    This is the API endpoint that your frontend will call.
    It fetches, parses, and returns the live vehicle data.
    """
    print("Fetching new data from the GTFS API...")
    
    # 1. Fetch raw data using your existing function
    raw_data = fetch_data()
    
    if raw_data:
        # 2. Parse the data if fetching was successful
        vehicle_positions = parse_data(raw_data)
        print(f"Successfully parsed {len(vehicle_positions)} vehicles.")
        
        # 3. Return the data as a JSON response
        return jsonify(vehicle_positions)
    else:
        # If fetching fails, return an error message
        print("Failed to fetch data from the API.")
        return jsonify({"error": "Failed to fetch data from the API"}), 500

if __name__ == '__main__':
    # Run the app in debug mode, which provides helpful error messages
    # and automatically reloads the server when you make changes.
    app.run(debug=True, port=5001)