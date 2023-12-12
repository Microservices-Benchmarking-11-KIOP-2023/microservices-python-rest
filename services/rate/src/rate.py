from dataclasses import dataclass
from typing import List

from flask import Flask, jsonify, request

from data.data_load_module import load_data, build_inventory_index, inventory_index

app = Flask(__name__)

global_data = None
RATE_SERVICE_PORT = 8080


@dataclass
class RoomType:
    bookableRate: float
    code: str
    description: str
    totalRate: float
    totalRateInclusive: float


@dataclass
class RatePlan:
    hotelId: str
    code: str
    inDate: str
    outDate: str
    roomType: RoomType


@dataclass
class Result:
    ratePlans: List[RatePlan]


def get_rates(hotel_ids, in_date, out_date):
    rate_plans = []
    for hotel_id in hotel_ids:
        rate_info = inventory_index.get(hotel_id, {}).get(in_date, {}).get(out_date)
        if rate_info:
            rate_plan_data = {
                'hotelId': hotel_id,
                'code': rate_info["code"],
                'inDate': in_date,
                'outDate': out_date,
                'roomType': rate_info["roomType"]
            }
            rate_plans.append(rate_plan_data)

    return rate_plans


@app.route('/rate', methods=['POST'])
def get_rates_endpoint():
    data = request.json
    hotel_ids = data['hotelIds']
    in_date = data['inDate']
    out_date = data['outDate']

    rate_plans = get_rates(hotel_ids, in_date, out_date)
    return jsonify(rate_plans)


def serve():
    load_data()
    build_inventory_index()
    app.run(host='0.0.0.0', port=8080)
