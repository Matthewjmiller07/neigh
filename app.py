from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_neighborhood(lat, lon, username):
    base_url = "http://api.geonames.org/neighbourhoodJSON?"
    params = {
        "lat": lat,
        "lng": lon,
        "username": username
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get('neighbourhood', {}).get('name', "Not available")

@app.route('/get_neighborhood', methods=['GET'])
def get_neighborhood_from_geonames():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        username = "matthewjmiller07"  # Your GeoNames username
        
        # Try original coordinates first
        neighborhood = get_neighborhood(lat, lon, username)
        if neighborhood != "Not available":
            return jsonify({"neighborhood": neighborhood})
        
        # Buffer zone approach
        delta = 0.001  # Adjust as needed
        for dlat in [0, delta, -delta]:
            for dlon in [0, delta, -delta]:
                neighborhood = get_neighborhood(lat + dlat, lon + dlon, username)
                if neighborhood != "Not available":
                    return jsonify({"neighborhood": neighborhood})
        
        return jsonify({"neighborhood": "Not available"})
        
    except requests.RequestException as e:
        return jsonify({"Error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
