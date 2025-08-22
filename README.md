# Delhi Live Transit Tracker

A real-time web application to visualize and track public transport vehicles (buses) in Delhi using GTFS-realtime data, Redis caching, and interactive mapping with clustering.

## Features

- **Live Bus Tracking:** Displays the current positions of buses in Delhi on an interactive map.
- **Marker Clustering:** Uses Leaflet's MarkerCluster plugin to group nearby buses for better visualization and performance.
- **Animated Marker Movement:** Bus markers smoothly slide to new positions as updates arrive.
- **Efficient Data Handling:** Vehicle positions are fetched from a public API, parsed, and cached in Redis for fast access.
- **Separation of Concerns:** A background worker fetches and parses data, while the web server serves cached data to clients.

## Technologies Used

- **Python**
  - Flask: Web server and API endpoints
  - Redis: In-memory cache for fast data retrieval
  - requests: For fetching GTFS-realtime protobuf data
  - google.transit.gtfs_realtime_pb2: For parsing GTFS-realtime data
- **JavaScript**
  - Leaflet: Interactive map rendering
  - Leaflet.markercluster: Efficient clustering of bus markers
  - Leaflet.Marker.SlideTo: Smooth marker movement animation
- **HTML/CSS**
  - Responsive design for map and controls

## Architecture

- **worker.py:**
  - Periodically fetches GTFS-realtime vehicle positions from the Delhi government API.
  - Parses protobuf data and stores the latest vehicle positions in Redis as JSON.
- **app.py:**
  - Serves the frontend and provides an API endpoint (`/api/vehicle_positions`) that reads cached data from Redis.
- **index.html:**
  - Fetches vehicle positions from the API every 10 seconds.
  - Displays buses on a Leaflet map, using clustering and smooth movement for a clear, real-time experience.
- **index.html:**
  - Contains the address to get the data from
  - Contains the functions to call and parse the response provided by the api

## Techniques Explained

### Marker Clustering

- **Why?**
  - When many buses are close together, individual markers overlap and clutter the map.
  - Clustering groups nearby markers into a single cluster icon, which expands as you zoom in.
- **How?**
  - Uses `leaflet.markercluster` to automatically group and manage bus markers.

### Animated Marker Movement

- **Why?**
  - Sudden jumps of markers can be visually jarring.
  - Smooth sliding helps users track bus movement naturally.
- **How?**
  - Uses `Leaflet.Marker.SlideTo` to animate marker position changes.

### Redis Caching

- **Why?**
  - Reduces API calls and parsing overhead for every web request.
  - Ensures fast, scalable data access for multiple users.
- **How?**
  - Worker saves parsed vehicle positions to Redis.
  - Web server reads from Redis and serves cached data to clients.

## Setup Instructions

1. **Install dependencies:**
   - Python packages: `flask`, `flask_cors`, `redis`, `requests`, `python-dotenv`, `protobuf`, `google-transit-gtfs-realtime`
   - Redis server (local or remote)
2. **Set your API key:**
   - Create a `.env` file with `TRANSIT_API_KEY=your_key_here`
3. **Run Redis server:**
   - `redis-server`
4. **Start the worker:**
   - `python3 worker.py`
5. **Start the web server:**
   - `python3 app.py`
6. **Open the app:**
   - Visit `http://localhost:5001` in your browser

## File Structure

- `app.py` — Flask web server and API
- `worker.py` — Background worker for fetching and caching data
- `data_fetcher.py` — GTFS-realtime data fetch and parse logic
- `templates/index.html` — Frontend map UI

## License

MIT

## Credits

- Delhi Government Open Transit Data
- Leaflet, MarkerCluster, SlideTo plugins
