from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SEARCH_SERVICE_PORT = 5001
GEO_SERVICE_ADDRESS = 'http://localhost:5003/geo'
RATE_SERVICE_ADDRESS = 'http://localhost:5004/rate'


@app.route('/search', methods=['GET'])
def search_nearby():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    in_date = request.args.get('inDate')
    out_date = request.args.get('outDate')

    geo_response = requests.get(GEO_SERVICE_ADDRESS, params={"lat": lat, "lon": lon}).json()

    rate_response = requests.post(
        RATE_SERVICE_ADDRESS,
        json={
            "hotelIds": geo_response["hotelIds"],
            "inDate": in_date,
            "outDate": out_date
        }
    ).json()

    available_hotel_ids = [rate_plan["hotelId"] for rate_plan in rate_response]

    return jsonify({"hotelIds": available_hotel_ids})


def serve():
    app.run(port=SEARCH_SERVICE_PORT, debug=True)