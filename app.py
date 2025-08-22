# app.py

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)

# Connect to your local Redis server
r = redis.Redis(decode_responses=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/vehicle_positions')
def get_vehicle_positions():
    """
    This endpoint now reads data from the Redis cache.
    It no longer calls fetch_data() or parse_data().
    """
    print("API request received, fetching from Redis cache...")
    
    # 1. Get the JSON string from Redis using our key
    json_data = r.get('latest_vehicles')
    
    if json_data:
        # 2. If data exists, parse the JSON string back into a Python object
        vehicle_positions = json.loads(json_data)
        
        # 3. Return the data using jsonify
        return jsonify(vehicle_positions)
    else:
        # This will happen if the worker hasn't run yet or there was an error
        return jsonify({"error": "No data available in cache. Please wait."}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)