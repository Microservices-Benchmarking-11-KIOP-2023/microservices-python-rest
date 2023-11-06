import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

PROFILE_SERVICE_PORT = 5002

current_dir = os.path.dirname(os.path.abspath(__file__))
json_filepath = os.path.join(current_dir, 'data', 'hotels.json')


def load_profiles(hotel_ids, file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return "The file was not found."
    except json.JSONDecodeError:
        return "Error parsing the JSON file."

    matching_profiles = [hotel_profile for hotel_profile in data if hotel_profile['id'] in hotel_ids]
    return matching_profiles if matching_profiles else []


@app.route('/profile', methods=['GET'])
def get_profiles():
    hotel_ids = [hotel_id for hotel_id in request.args.getlist('hotelIds')]
    hotel_profiles = load_profiles(hotel_ids, json_filepath)

    response_data = []
    for profile in hotel_profiles:
        hotel_data = {
            'id': profile['id'],
            'name': profile['name'],
            'phoneNumber': profile['phoneNumber'],
            'description': profile['description'],
            'address': {
                'streetNumber': profile['address']['streetNumber'],
                'streetName': profile['address']['streetName'],
                'city': profile['address']['city'],
                'state': profile['address']['state'],
                'country': profile['address']['country'],
                'postalCode': profile['address']['postalCode'],
                'lat': profile['address']['lat'],
                'lon': profile['address']['lon']
            }
        }
        response_data.append(hotel_data)

    return jsonify(response_data)


def serve():
    app.run(host='0.0.0.0', port=PROFILE_SERVICE_PORT, debug=True)
