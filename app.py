from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/get_neighborhood', methods=['GET'])
def get_neighborhood_from_geonames():
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
    
    if response.status_code != 200:
        return jsonify({"Error": response.status_code})
    
    data = json.loads(response.text)
    
    if 'neighbourhood' in data:
        neighborhood_info = data['neighbourhood']
        return jsonify({"neighborhood": neighborhood_info.get('name', "Not available")})
    else:
        return jsonify({"neighborhood": "Not available"})

if __name__ == '__main__':
    app.run()
