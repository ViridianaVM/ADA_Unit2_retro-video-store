from app import db
import requests
from flask import request, Blueprint, make_response
from flask import jsonify
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from dotenv import load_dotenv
from datetime import datetime
import os


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

"""
CRUD for Customer
"""

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    if len(request_body) == 3:
        new_customer = Customer(name = request_body["name"], postal_code = request_body["postal_code"], phone = request_body["phone"])
        
        db.session.add(new_customer)
        db.session.commit()

        response = {
            "id" : new_customer.customer_id
        }
        return make_response(jsonify(response),201)

    elif ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body) or ("videos_checked_out_count" not in request_body):
        response = {
            "details" : "Invalid data"
        }
        return make_response(response,400)


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers_response = []

    customers = Customer.query.all()

    for customer in customers:
        customers_response.append(customer.to_json())
    return jsonify(customers_response), 200


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):

    customer = Customer.query.get(customer_id)
    if customer:
        response = customer.to_json()

        return make_response(response, 200)

    return make_response("",404)


@customers_bp.route("/<customer_id>",methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    updates_body = request.get_json()
    if customer_id is None or updates_body == {}:
        return make_response(jsonify(""),400)

    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("",404)

    customer.name = updates_body["name"]
    customer.postal_code = int(updates_body["postal_code"])
    customer.phone = updates_body["phone"]

    db.session.commit()
    return make_response(customer.to_json(),200)



@customers_bp.route("/<customer_id>",methods=["DELETE"], strict_slashes=False)
def delete_task(customer_id):

    
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("",404)

    db.session.delete(customer)
    db.session.commit()

    response = {"id": int(customer_id)}
    return make_response(response,200)



"""
CRUD for Video
"""

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    if len(request_body) == 3:
        new_video = Video(title = request_body["title"], release_date = request_body["release_date"], total_inventory = request_body["total_inventory"] )
        
        db.session.add(new_video)
        db.session.commit()

        response = {
            "id" : new_video.video_id
        }
        return make_response(jsonify(response),201)

    elif ("title" not in request_body) or ("release_date" not in request_body) or ("total_inventory" not in request_body):
        response = {
            "details" : "Invalid data"
        }
        return make_response(response,400)


@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():
    videos_response = []

    videos = Video.query.all()

    for video in videos:
        videos_response.append(video.to_json())
    return jsonify(videos_response), 200


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if video:
        response = video.to_json()

        return make_response(jsonify(response), 200)

    return make_response("",404)


@videos_bp.route("/<video_id>",methods=["PUT"], strict_slashes=False)
def update_video(video_id):

    updates_body = request.get_json()
    if video_id is None or updates_body == {}:
        return make_response(jsonify(""),400)

    video = Video.query.get(video_id)
    if video is None:
        return make_response("",404)

    video.title = updates_body["title"]
    video.release_date = updates_body["release_date"]
    video.total_inventory = updates_body["total_inventory"]

    db.session.commit()
    return make_response(video.to_json(),200)



@videos_bp.route("/<video_id>",methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    
    video = Video.query.get(video_id)
    if video is None:
        return make_response("",404)

    db.session.delete(video)
    db.session.commit()

    response = {"id": int(video_id)}
    return make_response(response,200)

