# worker.py

import redis
import time
import json
from data_fetcher import fetch_data, parse_data

r = redis.Redis(decode_responses=True)
print("Worker started...")

while True:
    try:
        raw_data = fetch_data()
        
        if raw_data:
            vehicle_positions = parse_data(raw_data)
            
            # --- DEBUGGING STEP ---
            # Print the total number of vehicles found before saving.
            print(f"DEBUG: Parsed {len(vehicle_positions)} vehicles from API.")
            
            # This is the data we're about to save.
            json_data = json.dumps(vehicle_positions)
            
            # Save to Redis
            r.set('latest_vehicles', json_data)
            
            print(f"SUCCESS: Saved data for {len(vehicle_positions)} vehicles to Redis.")
        else:
            print("FAIL: Could not fetch data.")

    except Exception as e:
        print(f"An error occurred in worker: {e}")

    time.sleep(10)