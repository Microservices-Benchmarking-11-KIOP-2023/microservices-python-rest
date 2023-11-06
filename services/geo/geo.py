import json
import math
import os
from dataclasses import dataclass
from flask import Flask, jsonify, request

app = Flask(__name__)

GEO_SERVICE_PORT = 5003
EARTH_RADIUS_KM = 6371.0
MAX_SEARCH_RADIUS_KM = 10  # limit to 10 km

current_dir = os.path.dirname(os.path.abspath(__file__))
json_filepath = os.path.join(current_dir, 'data', 'geo.json')


@dataclass
class Point:
    point_latitude: float
    point_longitude: float


def load_hotels(json_filepath):
    with open(json_filepath, 'r') as file:
        hotels = json.load(file)
    return hotels


def haversine_distance(coord1, coord2):
    lat1 = coord1.point_latitude
    lon1 = coord1.point_longitude
    lat2 = coord2.point_latitude
    lon2 = coord2.point_longitude

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def find_nearby_hotels(hotels, point, radius):
    nearby_hotels = []

    for hotel in hotels:
        hotel_coord = Point(point_latitude=hotel['lat'], point_longitude=hotel['lon'])
        distance = haversine_distance(point, hotel_coord)

        if distance <= radius:
            nearby_hotels.append(hotel['hotelId'])

    return nearby_hotels


@app.route('/geo', methods=['GET'])
def nearby_hotels():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    point = Point(point_latitude=lat, point_longitude=lon)

    hotels = load_hotels(json_filepath)
    nearby_hotel_ids = find_nearby_hotels(hotels, point, MAX_SEARCH_RADIUS_KM)

    return jsonify({"hotelIds": nearby_hotel_ids})


def serve():
    app.run(host='0.0.0.0', port=GEO_SERVICE_PORT, debug=True)
