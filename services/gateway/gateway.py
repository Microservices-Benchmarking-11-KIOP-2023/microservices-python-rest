from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SEARCH_SERVICE_URL = 'http://search:8080/search'
PROFILE_SERVICE_URL = 'http://profile:8080/profile'


@app.route('/hotels', methods=['GET'])
def get_hotels():
    # Parse the HTTP request
    in_date = request.args.get('inDate')
    out_date = request.args.get('outDate')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    # Call the search service
    search_payload = {
        "lat": lat,
        "lon": lon,
        "inDate": in_date,
        "outDate": out_date
    }
    search_response = requests.get(SEARCH_SERVICE_URL, params=search_payload).json()
    hotel_ids = search_response['hotelIds']

    # Call the profile service
    profile_payload = {
        "hotelIds": hotel_ids
    }
    profile_response = requests.get(PROFILE_SERVICE_URL, params=profile_payload).json()

    # Convert the REST API response to a desired JSON format
    hotels = [{
        'type': 'Feature', 'id': hotel['id'],
        'properties': {'name': hotel['name'], 'phone_number': hotel['phoneNumber']},
        'geometry': {'type': 'Point', 'coordinates': [hotel['address']['lat'], hotel['address']['lon']]}} for hotel in
        profile_response]

    return jsonify(hotels)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
