from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_neighborhood', methods=['GET'])
def get_neighborhood_from_geonames():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        username = "matthewjmiller07"  # Your GeoNames username
        
        base_url = "http://api.geonames.org/neighbourhoodJSON?"
        params = {
            "lat": lat,
            "lng": lon,
            "username": username
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        data = response.json()  # Parse JSON
        
        if 'neighbourhood' in data:
            neighborhood_info = data['neighbourhood']
            return jsonify({"neighborhood": neighborhood_info.get('name', "Not available")})
        else:
            return jsonify({"neighborhood": "Not available"})
    except requests.RequestException as e:
        return jsonify({"Error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
