from flask import Flask, request, jsonify
import requests
# import wikipediaapi
import logging

logging.basicConfig(level=logging.INFO)

# wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='my_application')

app = Flask(__name__)

@app.route('/get_neighborhood', methods=['GET'])
def get_neighborhood_from_geonames():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        username = "matthewjmiller07"  # Your GeoNames username

        logging.info(f"Received request for lat: {lat}, lon: {lon}")

        # Initialize Wikipedia API
        # wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='my_application')

        # First API call for neighbourhood information
        base_url = "http://api.geonames.org/neighbourhoodJSON?"
        params = {
            "lat": lat,
            "lng": lon,
            "username": username
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        logging.info(f"GeoNames API full response: {data}")

        search_term = None

        if 'neighbourhood' in data:
            search_term = data['neighbourhood'].get('name', "Not available")
        elif 'city' in data:
            search_term = data.get('city', "Not available")
        else:
            # Fallback API call for place name information
            fallback_url = "http://api.geonames.org/findNearbyPlaceNameJSON?"
            fallback_params = {
                "lat": lat,
                "lng": lon,
                "username": username
            }
            
            fallback_response = requests.get(fallback_url, params=fallback_params)
            fallback_response.raise_for_status()
            
            fallback_data = fallback_response.json()
            
            if 'geonames' in fallback_data and len(fallback_data['geonames']) > 0:
                search_term = fallback_data['geonames'][0].get('name', "Not available")

        # wikipedia_info = None

        # logging.info(f"Searching Wikipedia for: {search_term}")

        # if search_term:
        #     page = wiki_wiki.page(search_term)
        #     if page.exists():
        #         wikipedia_info = page.summary[:1000]
        #         logging.info(f"Wikipedia page found: {wikipedia_info[:100]}")
        #     else:
        #         logging.info("Wikipedia page does not exist.")

        return jsonify({"neighborhood": search_term})  # , "wikipedia_info": wikipedia_info})

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return jsonify({"Error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
